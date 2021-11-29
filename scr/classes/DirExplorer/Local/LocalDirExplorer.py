import time
import traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scr.classes.DirExplorer.AbstractDirExplorer import DirExplorer
import locale
import os
from pyxtension.streams import stream
from scr.classes.DirExplorer.Local.Cust_TreeView import Cust_TreeView
from scr.classes.DirExplorer.Local.IconBuffer import IconBuffer
from scr.classes.DirExplorer.Local.LocalContextMenu import LocalContextMenu
from scr.classes.DirExplorer.NoSelectionContextMenu import NoSelecetionContextMenu



class LocalDirExplorer(DirExplorer):
    horizontal_header_items_align = {'Name': Qt.AlignLeft, 'Size': Qt.AlignRight, 'Type': Qt.AlignLeft,
                                     "Changed": Qt.AlignLeft, " ": Qt.AlignLeft}
    PATH_HISTORY_SIZE = 20
    start_path = QDir.rootPath()

    def __init__(self, tree_view: Cust_TreeView, path_bar: QLineEdit, status_bar: QLineEdit,driver_update_pointer) -> None:
        super().__init__(tree_view, path_bar, status_bar)
        self.driver_update_pointer = driver_update_pointer
        locale.setlocale(locale.LC_ALL, '')
        self.filter_list = [QDir.Filter.AllEntries ,QDir.Filter.NoDotAndDotDot]
        self.current_filter = 0
        self.hidden_visible = False
        self.current_path = self.start_path
        self.path_history = []
        self.path_history_index = -1
        self.current_dir = QDir()
        self.set_current_dir( QDir(self.current_path),True)
        self.context_menu = LocalContextMenu(self)
        self.context_menu_no_sel = NoSelecetionContextMenu(self)
        self.create_and_apply_item_model()
        self.update_dir_data()
        self.tree_view.resizeColumnToContents(0)
        locale.setlocale(locale.LC_ALL, '')

    def set_current_dir(self,path:QDir,save_to_history:bool):
        if save_to_history and self.current_dir.absolutePath() != path.absolutePath():
            self.add_to_history(path)
        self.current_dir = QDir(path)

    def add_to_history(self,path:QDir):
        self.path_history = self.path_history[:self.path_history_index + 1: 1] # C/:test1/test2/test3  <- <- C:/test1 + test8(append new path should remove all pathes from current index)

        if len(self.path_history) == LocalDirExplorer.PATH_HISTORY_SIZE:
            self.path_history.pop(0)
            self.path_history.append(path.absolutePath())
        else:
            self.path_history.append(path.absolutePath())
            self.path_history_index = self.path_history_index + 1


    def update_dir_data(self):
        qFileIconProvider = QFileIconProvider()
        self.tree_view.scrollToTop()
        self.current_entry_info_list = []
        self.model.removeRows(0, self.model.rowCount())
        self.add_parent_directory()

        self.current_filter = self.calculate_filter_value()
        for file_info in self.current_dir.entryInfoList(sort=QDir.SortFlag.DirsFirst,
                                                        filters= self.current_filter ):

            f :QFileInfo = file_info
            file_info.isHidden()
            self.current_entry_info_list.append(file_info)
            file_name, file_size, file_type, file_last_mod = self.get_formated_data_from_file_info(file_info)


            icon = qFileIconProvider.icon(QFileInfo(file_info.absoluteFilePath()))

            item1 = QStandardItem(file_name)
            item2 = QStandardItem(file_size)
            item3 = QStandardItem(file_type)
            item4 = QStandardItem(file_last_mod)
            item5 = QStandardItem()
            item1.setIcon(icon)
            items = [item1, item2, item3, item4,item5]

            for value, index in zip(self.horizontal_header_items_align.values(), range(len(items))):
                items[index].setTextAlignment(value)
                if file_info.isHidden():
                    items[index].setForeground(Qt.gray)

            for item in items:
                item.setSelectable(False)
            item1.setSelectable(True)
            self.model.appendRow(items)

        self.path_bar.setText(self.current_dir.absolutePath())
        self.set_formated_status_bar()
        self.driver_update_pointer(self.current_dir)


    def set_formated_status_bar(self):
        count = len(self.current_entry_info_list) - (1 if self.parent_directory_present else 0)
        plural = "" if count == 1 else "s"
        self.status_bar_p1 = self.def_status_bar_text_part1.format(count=count, plural=plural)
        self.status_bar.setText(self.status_bar_p1)


    def get_formated_data_from_file_info(self, file_info: QFileInfo):
        data1 = file_info.fileName()
        data2 = ""
        if file_info.size() > 0:
            # data2 = "{:,d} KB".format(file_info.size())
            data2 = '{:,.0f} KB'.format(file_info.size() / float(1 << 10))
        data3 = self.get_file_type(file_info)
        data4 = file_info.lastModified().toString("dd.MM.yyyy hh:mm:ss")
        return data1, data2, data3, data4

    def get_file_type(self, file_info: QFileInfo):
        if file_info.isDir():
            return "File Directory"
        if file_info.isFile():
            return ( file_info.suffix() + ' File')
        return ''

    def add_parent_directory(self):
        self.parent_directory_present = False
        if self.current_dir.absolutePath() not in  stream(QDir.drives()).map(lambda x:x.path()).toList():
            item1 = QStandardItem("..")
            item2 = QStandardItem()
            item3 = QStandardItem("Parent directory")
            item4 = QStandardItem(
                QFileInfo(self.current_dir.absolutePath()).lastModified().toString("dd.MM.yyyy hh:mm:ss"))
            item5 = QStandardItem()
            style = self.tree_view.style()
            item1.setIcon(QIcon(style.standardIcon(QStyle.SP_DirIcon)))
            file_info = QFileInfo(self.current_dir.absolutePath() + "\\..")
            self.current_entry_info_list.insert(0, file_info)
            row = [item1, item2, item3, item4, item5]

            for element in row:
                element.setSelectable(False)
            item1.setSelectable(True)

            self.model.appendRow(row)
            self.parent_directory_present = True

    def create_and_apply_item_model(self):
        self.model = QStandardItemModel()

        for key, index in zip(self.horizontal_header_items_align.keys(),
                              range(len(self.horizontal_header_items_align))):
            item = QStandardItem(key)
            item.setTextAlignment(self.horizontal_header_items_align[key])
            self.model.setHorizontalHeaderItem(index, item)

        self.model.setColumnCount(len(self.horizontal_header_items_align))
        self.tree_view.setModel(self.model)
        self.model.itemChanged.connect(self.onItemChanged)
        self.tree_view.doubleClicked.connect(self.trigger_double_clik_tree_item)
        self.tree_view.selectionModel().selectionChanged.connect(self.trigger_selection_changed)
        self.tree_view.customContextMenuRequested.connect(self.trigger_context_menu)

    def onItemChanged(self,item:QStandardItem):
        old_name = self.current_entry_info_list[item.index().row()]
        new_name = old_name.absolutePath()+'/'+ item.text()
        success = QFile.rename(old_name.absoluteFilePath(),new_name)
        if not success:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Failed to rename {'directory'if old_name.isDir() else 'file'}")

            msg.setWindowTitle("Error")
            msg.exec()
        self.update_dir_data()



    def change_dir(self, index: QModelIndex):
        target_path = self.model.index(index.row(), 0, QModelIndex()).data()
        if target_path == "..":
            self.current_dir.cdUp()
        else:
            self.current_dir.cd(target_path)
        self.add_to_history(self.current_dir)
        self.update_dir_data()


    # -----------TRIGGERS-------------------

    def trigger_selection_changed(self):
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
                selected_files_size += self.current_entry_info_list[row.row()].size()

            selected_files_size = "{:,d} ".format(selected_files_size)
            status_bar_text = self.def_status_bar_text_part2.format(sel_count=selected_files_count,
                                                                    plural=selected_files_plural,
                                                                    size=selected_files_size, measure_unit="KB")
            status_bar_text = self.status_bar_p1 + status_bar_text
            self.status_bar.setText(status_bar_text)

    def trigger_double_clik_tree_item(self, index:QModelIndex):

        file_info = self.current_entry_info_list[index.row()]
        if index.column() == 0:
            QApplication.setOverrideCursor(Qt.BusyCursor)
            if file_info.isDir():
                self.change_dir(index)

            elif file_info.isFile() and not file_info.isExecutable():
                os.startfile(file_info.absoluteFilePath())

            QApplication.restoreOverrideCursor()

    def trigger_context_menu(self):
        try:
            cursor = QCursor()

            if len(self.tree_view.selectionModel().selectedRows()) == 0:
                self.context_menu_no_sel.exec_(cursor.pos())
            else:
                self.context_menu.exec_(cursor.pos())
        except Exception:
            traceback.print_exc()

    # --------------------------------------------------

    def disable_components(self, bool):
        self.tree_view.setDisabled(bool)
        self.path_bar.setDisabled(bool)
        self.status_bar.setDisabled(bool)

    def show_error_window(self, fileName, err):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('More information')
        msg.setWindowTitle("Error")
        msg.exec_()

    def change_hidden_visible(self):

            self.hidden_visible = not self.hidden_visible
            if QDir.Hidden in self.filter_list:
                self.filter_list.remove(QDir.Hidden)
            else:
                self.filter_list.append(QDir.Hidden)


    def calculate_filter_value(self):
        value = 0
        for filter in self.filter_list:
            value = value | filter
        return value

