import os
import stat
import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scr.classes.DirExplorer.Local.LocalDirExplorer import LocalDirExplorer
from scr.classes.DirExplorer.Remote.RemoteDirExplorer import RemoteDirExplorer


class RemoteDirPanelButtons:

    def __init__(self,download_button,combo_box,remote_Dir_Explorer:RemoteDirExplorer,local_dir_explorer : LocalDirExplorer):
        self.download_button = download_button
        self.combo_box = combo_box
        self.remote_Dir_Explorer = remote_Dir_Explorer
        self.local_dir_explorer = local_dir_explorer
        self.download_button.clicked.connect(self.download_selected_files)
        self.widgets = [self.download_button,self.combo_box]

    def download_selected_files(self):
        try:
            QApplication.setOverrideCursor(Qt.BusyCursor)
            for row in  self.remote_Dir_Explorer.tree_view.selectionModel().selectedRows():
                selected_file_info = self.remote_Dir_Explorer.current_entry_info_list[row.row()]
                remote_file_path = '%s/%s' % (self.remote_Dir_Explorer.sftp.getcwd(),selected_file_info.filename)

                if stat.S_ISDIR(selected_file_info.st_mode):
                    self.download_dir(selected_file_info.filename,remote_file_path,self.local_dir_explorer.current_dir.absolutePath())
                else:
                    self.download_file(remote_file_path,os.path.join(self.local_dir_explorer.current_dir.absolutePath(),selected_file_info.filename))
                self.local_dir_explorer.update_dir_data()
            QApplication.restoreOverrideCursor()
        except Exception:
            traceback.print_exc()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error occurred while downloading file from SFTP server")
            msg.setWindowTitle("Error")
            msg.setWindowFlag(Qt.WindowStaysOnTopHint)
            msg.exec_()

        finally:
            QApplication.restoreOverrideCursor()

    def download_file(self,remote_file_path,local_file_path):
       self.remote_Dir_Explorer.sftp.get(remote_file_path,local_file_path)

    def download_dir(self,dir_name,remote_dir_path,local_path):
        sftp = self.remote_Dir_Explorer.sftp
        local_dir_path = '%s/%s' % (local_path,dir_name)
        print(local_dir_path)
        os.mkdir(local_dir_path)

        for filename in sftp.listdir(remote_dir_path):
            if stat.S_ISDIR(sftp.stat(remote_dir_path +'/'+ filename).st_mode):
                self.download_dir(filename,remote_dir_path +'/'+ filename,local_dir_path)
            else:

                self.download_file(remote_dir_path +'/'+ filename, os.path.join(local_dir_path, filename))


    def disable_components(self, param:bool):
        for widget in self.widgets:
            widget.setDisabled(param)
