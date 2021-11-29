import shutil
import threading
import traceback
import typing
from time import sleep
import os
import win32clipboard
from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QFileInfo, QDir, Qt, QCoreApplication, QIODevice
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QStyle, QAction, QApplication, QMessageBox, QInputDialog

from scr.classes.DirExplorer.ClipBoard import Clipboard
from scr.classes.DirExplorer.Local import LocalDirExplorer


class NoSelecetionContextMenu(QMenu):

    def __init__(self,local_dir: LocalDirExplorer):
       super(NoSelecetionContextMenu, self).__init__()
       self.dlg :QInputDialog = QInputDialog()
       self.local_dir = local_dir
       self.initialize()

    def initialize(self):
        style = self.style()
        go_to = self.addAction("Go to")
        self.addSeparator()
        new = self.addMenu("New")
        directory = new.addAction("Directory",self.create_dir_action)
        directory.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DirIcon)))
        file = new.addAction("File",self.create_file_action)
        file.setIcon(QIcon(self.style().standardIcon( QStyle.SP_FileIcon)))

        past = self.addAction("Past",self.past_files)
        past.setShortcut("Ctrl+V")
        self.local_dir.tree_view.addAction(past)
        self.addSeparator()
        refresh = self.addAction("&Refresh",self.refresh_action)
        refresh.setShortcut("Ctrl+R")
        self.local_dir.tree_view.addAction(refresh)
        upload = self.addAction("Filter")
        upload.setDisabled(True)


    def create_file_action(self):
        reply = self.show_input_dialog('Edit File',"Enter file name:")

        if reply == 1:
            target_file = self.local_dir.current_dir.absolutePath()+'/' + self.dlg.textValue()
            if not os.path.exists(target_file):
                try:
                    with open(target_file, 'w') as fp:
                        pass
                except Exception:
                    self.show_error_window(target_file, 'Failed to create file')
            else:
                self.show_error_window(target_file, 'Path already exist')
            self.local_dir.update_dir_data()




    def create_dir_action(self):
        reply = self.show_input_dialog('Edit Folder', "Enter folder name:")
        if reply == 1:
            target_fodler = self.local_dir.current_dir.absolutePath() + '/' + self.dlg.textValue()
            if not os.path.exists(target_fodler):
                try:
                    os.makedirs(target_fodler)
                except Exception:
                    self.show_error_window(target_fodler, 'Failed to create folder')
            else:
                self.show_error_window(target_fodler, 'Path already exist')
            self.local_dir.update_dir_data()


    def show_input_dialog(self,title,text):
        self.dlg = QInputDialog()
        self.dlg.setInputMode(QInputDialog.TextInput)
        self.dlg.setWindowTitle(title)
        self.dlg.setLabelText(text)
        self.dlg.resize(500, 100)
        reply = self.dlg.exec_()
        return reply

    def refresh_action(self):
        QApplication.setOverrideCursor(Qt.BusyCursor)
        sleep(0.1)
        self.local_dir.update_dir_data()
        QApplication.restoreOverrideCursor()

    def start_thread(self):
        thread = threading.Thread(target=self.past_files)
        thread.start()

    def past_files(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            QApplication.setOverrideCursor(Qt.BusyCursor)
            self.local_dir.tree_view.setDisabled(True)
            current_file_name = ''
            try:
                    copy_to = self.local_dir.current_dir.absolutePath()
                    files_list = Clipboard.get_clipboard_files()

                    for file_path in files_list:
                        copied_file_info = QFileInfo(file_path)
                        copied_file = QFile(file_path)
                        current_file_name = copied_file_info.fileName()
                        new_path = copy_to + QDir.separator()+copied_file_info.fileName()
                        if copied_file_info.isDir():
                            shutil.copytree(copied_file.fileName(), new_path)

                        else:
                            shutil.copy(copied_file.fileName(),new_path)

                        self.local_dir.update_dir_data()

            except (shutil.SameFileError ,FileExistsError):
                self.show_error_window(current_file_name,f"The destination already contains a folder/file named {current_file_name}")
            except FileNotFoundError:
                self.show_error_window(current_file_name, 'File Not found')
            except Exception:
                self.show_error_window(current_file_name,'Unknown Error')
            QApplication.restoreOverrideCursor()
            self.local_dir.tree_view.setDisabled(False)

    def show_error_window(self,fileName ,err ):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(fileName)
        msg.setInformativeText(err)
        msg.setWindowTitle("Error Occured")
        msg.exec_()



if __name__ == "__main__":

        win32clipboard.OpenClipboard()
        filenames = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        win32clipboard.CloseClipboard()
        print(filenames)
        for filename in filenames:
            print(filename)
