import traceback

import paramiko
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scr.classes.DirExplorer.AbstractDirExplorer import DirExplorer
from scr.classes.Session.Session import Session
import stat

class RemoteDirExplorer(DirExplorer):
    start_path = '.'
    horizontal_header_items_align = {'Name': Qt.AlignLeft, 'Size': Qt.AlignRight, "File Type": Qt.AlignLeft,
                                     "Rights": Qt.AlignLeft, "Owner": Qt.AlignLeft, " ": Qt.AlignLeft}

    def __init__(self, tree_view: QTreeView, path_bar: QLineEdit, status_bar: QLineEdit) -> None:
        super().__init__(tree_view, path_bar, status_bar)
        self.sftp:paramiko.sftp = None
        self.model = QStandardItemModel()


    def set_current_session(self, session: Session):
        if self.model.columnCount() == 0:
            self.create_and_apply_item_model()

        self.sftp = session.sftp_handler.sftp
        # Modify path and stuff
        self.update_dir_data()
        self.tree_view.resizeColumnToContents(0)
        pass

    def create_and_apply_item_model(self):
        for key, index in zip(self.horizontal_header_items_align.keys(),
                              range(len(self.horizontal_header_items_align))):
            item = QStandardItem(key)
            item.setTextAlignment(self.horizontal_header_items_align[key])
            self.model.setHorizontalHeaderItem(index, item)

        self.model.setColumnCount(len(self.horizontal_header_items_align))
        self.tree_view.setModel(self.model)


        self.tree_view.doubleClicked.connect(self.trigger_double_clik_tree_v_item)
        self.tree_view.selectionModel().selectionChanged.connect(self.trigger_selection_changed)

    def create_context_menu(self):
        pass

    def update_dir_data(self):
        qFileIconProvider = QFileIconProvider()
        self.current_entry_info_list = []
        self.model.removeRows(0, self.model.rowCount())
        self.add_parent_directory()

        for file_info in self.sftp.listdir_attr():

            self.current_entry_info_list.append(file_info)
            print(file_info.filename)
            file_name,file_size,file_type,file_rights,file_owner = self.get_formated_data_from_file_info(file_info)
            icon = None
            if stat.S_ISDIR(file_info.st_mode):
                icon = QIcon(self.tree_view.style().standardIcon(QStyle.SP_DirIcon))
            else:
                icon = qFileIconProvider.icon(QFileInfo(file_name))
            item1 = QStandardItem(file_name)
            item2 = QStandardItem(file_size)
            item3 = QStandardItem(file_type)
            item4 = QStandardItem(file_rights)
            item5 = QStandardItem(file_owner)
            item1.setIcon(icon)
            items = [item1, item2, item3, item4,item5,QStandardItem('')]

            for value, index in zip(self.horizontal_header_items_align.values(), range(len(items))):
                items[index].setTextAlignment(value)
                items[index].setSelectable(False)
            item1.setSelectable(True)

            self.model.appendRow(items)
        self.path_bar.setText(self.sftp.getcwd())
        self.set_formated_status_bar()

    def add_parent_directory(self):
        self.parent_directory_present = False
        if self.sftp.getcwd() != '/':
            item1 = QStandardItem("..")
            item2 = QStandardItem()
            item3 = QStandardItem("Parent directory")
          #  item4 = QStandardItem(  QFileInfo(self.current_dir.absolutePath()).lastModified().toString("dd.MM.yyyy hh:mm:ss"))
            item5 = QStandardItem()
            style = self.tree_view.style()
            item1.setIcon(QIcon(style.standardIcon(QStyle.SP_DirIcon)))
            file_info = paramiko.sftp_attr.SFTPAttributes()
            file_info.filename = ".."
            file_info.st_mode = 16832
            self.current_entry_info_list.insert(0, file_info)
            row = [item1, item2, item3, item5]
            for element in row:
                element.setSelectable(False)
            item1.setSelectable(True)
            self.model.appendRow(row)
            self.parent_directory_present = True



    def get_formated_data_from_file_info(self, file_info):
        file_size = 0
        if file_info.st_size > 0:
            file_size = '{:,.0f} KB'.format(file_info.st_size / float(1 << 10))
        file_type = ''
        if stat.S_ISDIR(file_info.st_mode):
            file_type = 'File Directory'
        elif stat.S_ISLNK(file_info.st_mode):
            file_type = 'Symbolic link'
        else:
            file:QFileInfo = QFileInfo(file_info.filename)
            file_type = 'File ' + file.suffix()
        return file_info.filename,file_size,file_type,stat.filemode(file_info.st_mode),""



    def trigger_context_menu(self):
        pass

    def disable_components(self, bool):
        self.tree_view.setDisabled(bool)
        self.path_bar.setDisabled(bool)
        self.status_bar.setDisabled(bool)
        if bool is True:
            self.model.clear()

    def change_dir(self, index):
        target_path = self.model.index(index.row(), 0, QModelIndex()).data()

        if target_path == "..":
            self.sftp.chdir('..')
        else:
            self.sftp.chdir(target_path)

        self.update_dir_data()
#------------------TRIGGERS----------------------------------
    def set_formated_status_bar(self):
        count = len(self.current_entry_info_list) - (1 if self.parent_directory_present else 0)
        plural = "" if count == 1 else "s"
        self.status_bar_p1 = self.def_status_bar_text_part1.format(count=count, plural=plural)
        self.status_bar.setText(self.status_bar_p1)


    def trigger_selection_changed(self):
        try:
            selected_rows = self.tree_view.selectionModel().selectedRows()
            selected_files_size = 0
            selected_files_count = len(selected_rows)
            selected_files_plural = "" if selected_files_count == 1 else "s"

            if selected_files_count > 0 and self.parent_directory_present and selected_rows[0].row() == 0:
                selected_rows.pop(0)
                selected_files_count -= 1

            if selected_files_count == 0:
                self.status_bar.setText(self.status_bar_p1)
            else:
                for row in selected_rows:
                    selected_files_size += int((self.current_entry_info_list[row.row()].st_size / float(1 << 10)))

                selected_files_size = "{:,d} ".format(selected_files_size)
                status_bar_text = self.def_status_bar_text_part2.format(sel_count=selected_files_count,
                                                                        plural=selected_files_plural,
                                                                        size=selected_files_size, measure_unit="KB")
                status_bar_text = self.status_bar_p1 + status_bar_text
                self.status_bar.setText(status_bar_text)

        except Exception:
            traceback.print_exc()

    def trigger_double_clik_tree_v_item(self, index):
        file_info:paramiko.sftp_attr.SFTPAttributes = self.current_entry_info_list[index.row()]
        if index.column() == 0:
            QApplication.setOverrideCursor(Qt.BusyCursor)

            if  stat.S_ISDIR(file_info.st_mode):
                self.change_dir(index)

            # elif file_info.isFile() or file_info.isExecutable():
            #     os.startfile(file_info.absoluteFilePath())
            QApplication.restoreOverrideCursor()

    #def get_file_rights(self,attr):



