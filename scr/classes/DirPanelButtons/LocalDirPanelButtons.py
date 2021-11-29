import copy
import os
import threading
import traceback
from collections import OrderedDict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyxtension.streams import stream
import subprocess as sp

from scr.classes.DirExplorer.Local.LocalDirExplorer import LocalDirExplorer
from scr.classes.Session.SessionHandler import SessionHandler


class LocalDirPanelButtons:
    default_paths = [QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0],
                     QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)[0],
                     QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]]

    def __init__(self):
        self.local_dir_explorer = None
        self.push_button_parent_dir = None
        self.push_button_root_dir = None
        self.push_button_home_dir = None
        self.push_button_refresh = None
        self.push_button_go_back = None
        self.push_button_go_forward = None
        self.local_driver_chooser = None
        self.driver_chooser_triggered_by_click = True
        self.drivers_paths_map = OrderedDict()

    # ---------------------Driver Chooser------------------------------

    def set_driver_chooser(self, local_driver_chooser):
        self.local_driver_chooser: QComboBox = local_driver_chooser
        self.drivers_paths_map = self.generate_drives_dict()
        qFileIconProvider = QFileIconProvider()

        for file_name, file_path in self.drivers_paths_map.items():
            self.local_driver_chooser.addItem(qFileIconProvider.icon(QFileInfo(file_path)), file_name)

        self.local_driver_chooser.activated.connect(self.driver_selection_changed)

    def driver_selection_changed(self, i):
        self.local_dir_explorer.current_dir = QDir(list(self.drivers_paths_map.values())[i])
        self.local_dir_explorer.update_dir_data()

    def generate_drives_dict(self):
        result = OrderedDict()  # fileName:filepath

        for drive in LocalDirPanelButtons.default_paths:
            fileInfo: QFileInfo = QFileInfo(drive)
            result.update({fileInfo.fileName(): fileInfo.absoluteFilePath()})

        for drive in QDir.drives():
            drive_name = drive.absoluteFilePath()[0:2]
            result.update({drive_name: drive.absoluteFilePath()})

        return result

    def update_driver_chooser(self, current_dir: QDir):

        index_to_choose = -1
        if current_dir.absolutePath() in self.drivers_paths_map.values():

            index_to_choose = list(self.drivers_paths_map.values()).index(current_dir.absolutePath())
        else:
            drives = stream(QDir.drives()).map(lambda x: x.path()).toList()
            for drive in drives:
                if drive in current_dir.absolutePath():
                    index_to_choose = list(self.drivers_paths_map.values()).index(drive)

        self.local_driver_chooser.setCurrentIndex(index_to_choose)

    # ---------------------------------------------------
    def set_button_go_back(self, button):
        self.push_button_go_back = button
        self.push_button_go_back.clicked.connect(self.go_back_action)

    def set_button_go_forward(self, button):
        self.push_button_go_forward = button
        self.push_button_go_forward.clicked.connect(self.go_forward_action)

    def go_back_action(self):
     try:
        if self.local_dir_explorer.path_history_index > 0:
            self.local_dir_explorer.path_history_index = self.local_dir_explorer.path_history_index - 1
            self.local_dir_explorer.current_dir = QDir(self.local_dir_explorer.path_history[self.local_dir_explorer.path_history_index])
            self.local_dir_explorer.update_dir_data()
     except Exception:
         traceback.print_exc()

    def go_forward_action(self):
        try:
            if self.local_dir_explorer.path_history_index < len(self.local_dir_explorer.path_history) -1:
                self.local_dir_explorer.path_history_index = self.local_dir_explorer.path_history_index + 1
                self.local_dir_explorer.current_dir = QDir(self.local_dir_explorer.path_history[self.local_dir_explorer.path_history_index])
                self.local_dir_explorer.update_dir_data()
        except Exception:
            traceback.print_exc()



    def set_edit_button(self, edit_button):
        self.edit_button = edit_button
        self.edit_button.setDisabled(True)
        self.edit_button.clicked.connect(lambda :self.edit_button_action())

    def edit_button_action(self):
        try:
            if(len(self.local_dir_explorer.tree_view.selectionModel().selectedRows()) > 0):
                selected_row = self.local_dir_explorer.tree_view.selectionModel().selectedRows()[0]
                file_info: QFileInfo = self.local_dir_explorer.current_entry_info_list[selected_row.row()]
                if file_info.isFile():
                    programName = "notepad.exe"
                    fileName = file_info.absoluteFilePath()
                    sp.Popen([programName, fileName])
        except:
            traceback.print_exc()

    def set_dir_explorer(self, local_dir_explorer: LocalDirExplorer):
        self.local_dir_explorer = local_dir_explorer
        self.local_dir_explorer.tree_view.selectionModel().selectionChanged.connect(self.dir_explorer_selection_changed)
        self._filter = Filter(self.upload_button, self.edit_button)
       # self.local_dir_explorer.tree_view.installEventFilter(self._filter)

    def set_remote_dir_explorer(self, remote_dir_explorer):
        self.remote_dir_explorer = remote_dir_explorer

    def set_upload_button(self, upload_local):
        self.upload_button = upload_local
        self.upload_button.clicked.connect(self.upload_selected_files)
        self.upload_button.setDisabled(True)

    def start_upload_files_thread(self):
        thread = threading.Thread(target=self.upload_selected_files)
        thread.start()

    def upload_selected_files(self):
        error_occured_filename = ''
        try:
            QApplication.setOverrideCursor(Qt.BusyCursor)

            if(len(self.local_dir_explorer.tree_view.selectionModel().selectedRows()) > 0):
                for row in self.local_dir_explorer.tree_view.selectionModel().selectedRows():
                    selected_file_info: QFileInfo = self.local_dir_explorer.current_entry_info_list[row.row()]
                    src_file_name = selected_file_info.absoluteFilePath()
                    out_file_path = self.session_handler.remote_dir_explorer.sftp.getcwd()
                    error_occured_filename =  selected_file_info.fileName()

                    if selected_file_info.isDir():
                        self.upload_dir( selected_file_info.fileName() , src_file_name,out_file_path)
                    else:
                        self.upload_file(src_file_name, out_file_path)

                    self.session_handler.remote_dir_explorer.update_dir_data()

            QApplication.restoreOverrideCursor()
        except :
            traceback.print_exc()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error occurred while uploading file {error_occured_filename} to the SFTP server")
            msg.setWindowTitle("Error")
            msg.setWindowFlag(Qt.WindowStaysOnTopHint)
            msg.exec_()
        finally:
            QApplication.restoreOverrideCursor()

    def upload_file(self,src_file_name,out_file_path):

        self.session_handler.remote_dir_explorer.sftp.put(src_file_name, out_file_path)

    def upload_dir(self,src_dri_name,src_dir_path,out_dir_path):
        if os.path.isdir(src_dir_path):
            out_dir_path = '%s/%s' % (out_dir_path,src_dri_name)
            self.session_handler.remote_dir_explorer.sftp.mkdir(out_dir_path)
        for item in os.listdir(src_dir_path):
            if os.path.isfile(os.path.join(src_dir_path, item)):
                self.upload_file(os.path.join(src_dir_path, item),  '%s/%s' % (out_dir_path, item))
            else:

                self.session_handler.remote_dir_explorer.sftp.mkdir('%s/%s' % (out_dir_path, item))
                self.upload_dir(item,os.path.join(src_dir_path, item), '%s/%s' % (out_dir_path, item))


    def dir_explorer_focus_out(self, e):
        self.edit_button.setDisabled(True)
        self.upload_button.setDisabled(True)

    def set_session_handler(self, session_handler:SessionHandler):
        self.session_handler = session_handler

    def dir_explorer_selection_changed(self):

        if len(self.local_dir_explorer.tree_view.selectionModel().selectedRows()) > 1:
            self.edit_button.setDisabled(True)
            if SessionHandler.ONE_OR_MORE_CONNECTED_FLAG is True:
                self.upload_button.setDisabled(False)

        elif len(self.local_dir_explorer.tree_view.selectionModel().selectedRows()) == 1:
            if SessionHandler.ONE_OR_MORE_CONNECTED_FLAG is True:
                self.upload_button.setDisabled(False)
            selected_row = self.local_dir_explorer.tree_view.selectionModel().selectedRows()[0]
            selected_file_info: QFileInfo = self.local_dir_explorer.current_entry_info_list[selected_row.row()]
            if selected_file_info.isFile():
                self.edit_button.setDisabled(False)
        else:
            self.upload_button.setDisabled(True)

    def set_parent_dir_button(self, push_button_parent_dir):
        self.push_button_parent_dir = push_button_parent_dir
        self.push_button_parent_dir.clicked.connect(lambda: self.parent_dir_action())

    def set_root_dir_button(self, push_button_root_dir):

        self.push_button_root_dir = push_button_root_dir
        self.push_button_root_dir.clicked.connect(self.root_dir_action)

    def set_home_dir_button(self, push_button_home_dir):
        self.push_button_home_dir = push_button_home_dir
        self.push_button_home_dir.clicked.connect(lambda: self.set_explorer_path(QDir.homePath()))

    def set_refresh_button(self, push_button_refresh: QPushButton):
        self.push_button_refresh = push_button_refresh
        self.push_button_refresh.clicked.connect(lambda: self.local_dir_explorer.update_dir_data())

    def set_explorer_path(self, path):
        self.local_dir_explorer.set_current_dir(QDir(path), True)
        self.local_dir_explorer.update_dir_data()

    def root_dir_action(self):
        drive_name = str(self.local_dir_explorer.current_dir.absolutePath()[0:3])
        self.set_explorer_path(drive_name)

    def parent_dir_action(self):
        old_path = self.local_dir_explorer.current_dir.absolutePath()
        self.local_dir_explorer.current_dir.cdUp()
        new_path = self.local_dir_explorer.current_dir.absolutePath()
        self.local_dir_explorer.current_dir = QDir(old_path)
        self.set_explorer_path(new_path)

    def set_mainwindow(self, main_window):
        self.main_window = main_window


class Filter(QObject):
    def __init__(self, upload_button, edit_button):
        super().__init__()
        self.upload_button = upload_button
        self.edit_button = edit_button

    def eventFilter(self, widget, event):
        if event.type() == QEvent.FocusOut:
            self.upload_button.setDisabled(True)
            self.edit_button.setDisabled(True)

            return False
        else:
            return False
