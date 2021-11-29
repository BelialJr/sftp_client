from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QTreeView, QLineEdit


class DirExplorer(ABC):
    def_status_bar_text_part1 = "{count} item{plural} | "
    def_status_bar_text_part2 = "{sel_count} item{plural} selected {size} {measure_unit} | "


    def __init__(self, tree_view: QTreeView, path_bar: QLineEdit, status_bar: QLineEdit) -> None:
        self.tree_view = tree_view
        self.path_bar = path_bar
        self.status_bar = status_bar
        self.apply_style_sheet()


    @abstractmethod
    def create_and_apply_item_model(self):
        pass



    @abstractmethod
    def update_dir_data(self):
        pass

    @abstractmethod
    def change_dir(self, index):
        pass

    @abstractmethod
    def trigger_context_menu(self):
        pass

    @abstractmethod
    def disable_components(self,bool):
        pass

    def add_parent_directory(self):
        pass

    @abstractmethod
    def get_formated_data_from_file_info(self, file_info):
        pass


    def apply_style_sheet(self):
        self.path_bar.setStyleSheet(
            "QLineEdit { color : black ;background: rgb(251,204,170); selection-background-color: rgb(233, 99, 0); }")  # 251 204 170 rgb(135,206,250)
   #     self.tree_view.setStyleSheet(                                                                           #QTreeView::item:hover {  background-color: rgb(255,203,176);}
        #    "QTreeView::item { border-right: 0.5px solid #DFDCDC;}QTreeView::branch {background: palette(base);}  QTreeView::item:selected:active  {   background-color:  rgb(233, 136, 66);}")
      #  "QTreeView::item:selected { border: 1px solid #567dbc;} ")
    #    self.tree_view.setStyleSheet("QTreeView::item { border: 0.5px ; border-style: solid ; border-color: lightgray ;}")
