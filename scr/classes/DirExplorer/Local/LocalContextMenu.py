
import os
import traceback
import subprocess as sp
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QFile, QDir, QCoreApplication, QFileDevice, QModelIndex, QFileInfo
from PyQt5.QtGui import QIcon, QKeySequence, QStandardItem, QPixmap
from PyQt5.QtWidgets import QMenu, QStyle, QAction, QWidget, QApplication, QMessageBox, QCheckBox

from scr.classes.DirExplorer.ClipBoard import Clipboard
from scr.classes.DirExplorer.Local import LocalDirExplorer


class LocalContextMenu(QMenu):

    def __init__(self, local_dir: LocalDirExplorer):
        super(LocalContextMenu, self).__init__()
        self.local_dir = local_dir
        self.initialize()
        self.not_show_delete_dialog = False

    def initialize(self):
        style = self.style()
        self.open_action = self.addAction("&Open", self.open_file)
        self.local_dir.tree_view.addAction(self.open_action)
        self.edit_action = self.addAction("&Edit ", self.edit_file)
        self.edit_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_E))
        self.local_dir.tree_view.addAction(self.edit_action)
        self.upload_action = self.addAction("Upload")
        self.delete_action = self.addAction("Delete", self.remove_file)
        self.rename_action = self.addAction("Rename", self.rename_file)
        self.addSeparator()
        self.copy_action = self.addAction("&Copy", self.set_copied_files)
        self.copy_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
        self.local_dir.tree_view.addAction(self.copy_action)
        self.properties_action = self.addAction("Properties")
        self.open_action.setIcon(QIcon(style.standardIcon(QStyle.SP_DirIcon)))
        self.edit_action.setIcon(QIcon('../icons/document.png'))
        self.upload_action.setIcon(QIcon('../icons/submit.png'))

    def edit_file(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            if len(self.local_dir.tree_view.selectionModel().selectedRows()) == 1:
                selected_row = self.local_dir.tree_view.selectionModel().selectedRows()[0]
                file_info:QFileInfo = self.local_dir.current_entry_info_list[selected_row.row()]
                if file_info.isFile():
                    programName = "notepad.exe"
                    fileName = file_info.absoluteFilePath()
                    sp.Popen([programName, fileName])

    def remove_file(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            try:
                selected_rows = self.local_dir.tree_view.selectionModel().selectedRows()
                reply = None
                if not self.not_show_delete_dialog:
                    cb = QCheckBox("Do not show this again.")
                    msgbox = QMessageBox(QMessageBox.Question, "Confirm close",
                                         f"Are you sure you want to remove {len(selected_rows)} selected file{'s' if len(selected_rows) > 1 else ''}?")
                    msgbox.addButton(QMessageBox.Yes)
                    msgbox.addButton(QMessageBox.No)
                    msgbox.setCheckBox(cb)
                    reply = msgbox.exec()
                    self.not_show_delete_dialog = cb.isChecked()

                if reply == QMessageBox.Yes or  self.not_show_delete_dialog is True:
                    QApplication.setOverrideCursor(Qt.BusyCursor)
                    try:
                        for selected_row in self.local_dir.tree_view.selectionModel().selectedRows():
                            file_info = self.local_dir.current_entry_info_list[selected_row.row()]
                            if file_info.isDir():
                               direct = QDir(file_info.absoluteFilePath())
                               file = QFile(file_info.absoluteFilePath())
                               file.setPermissions(file.permissions()|QFileDevice.WriteOwner|QFileDevice.WriteGroup |QFileDevice.WriteUser | QFileDevice.WriteOther)
                               direct.removeRecursively()
                            else:
                               QFile.remove(file_info.absoluteFilePath())
                            #QCoreApplication.processEvents()
                        self.local_dir.update_dir_data()

                    except Exception:
                        traceback.print_exc()
                    QApplication.restoreOverrideCursor()
            except Exception:
                traceback.print_exc()

    def open_file(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            if len(self.local_dir.tree_view.selectionModel().selectedRows()) == 1:
                selected_row = self.local_dir.tree_view.selectionModel().selectedRows()[0]
                file_info = self.local_dir.current_entry_info_list[selected_row.row()]

                QApplication.setOverrideCursor(Qt.BusyCursor)
                if file_info.isDir():
                    self.local_dir.change_dir(selected_row)

                elif file_info.isFile():
                    os.startfile(file_info.absoluteFilePath())

                QApplication.restoreOverrideCursor()

    def set_copied_files(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            selected_rows = self.local_dir.tree_view.selectionModel().selectedRows()
            file_paths = []
            for selected_row in selected_rows:
                file_paths.append(self.local_dir.current_entry_info_list[selected_row.row()].absoluteFilePath())
            Clipboard.set_clipboard_files(file_paths)

    def rename_file(self):
        if QApplication.focusWidget() == self or QApplication.focusWidget() == self.local_dir.tree_view:
            if len(self.local_dir.tree_view.selectionModel().selectedRows()) == 1:
                selected_index:QModelIndex = self.local_dir.tree_view.selectedIndexes()[0]
                self.local_dir.tree_view.edit(selected_index)
                #print(self.local_dir.current_entry_info_list[selected_index.row()])
                #file_info = self.local_dir.current_entry_info_list[selected_row.row()]



    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        selected_row = self.local_dir.tree_view.selectionModel().selectedRows()[0]
        selected_file_info: QFileInfo = self.local_dir.current_entry_info_list[selected_row.row()]

        if len(self.local_dir.tree_view.selectionModel().selectedRows()) > 1:
            self.open_action.setDisabled(True)
            self.rename_action.setDisabled(True)
            self.edit_action.setDisabled(True)
            self.properties_action.setDisabled(True)
        else:
            for action in self.actions():
                action.setDisabled(False)

            if not selected_file_info.isFile():
                self.edit_action.setDisabled(True)

        self.properties_action.setDisabled(True)

        super().enterEvent(a0)
