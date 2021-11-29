import traceback
import typing

import PyQt5.QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scr.classes.DirExplorer.CustomItemDelegate import CustomItemDelegate


class Cust_TreeView(QTreeView):

    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)
        self.rubber_band_origin_pos = None
        self.initialize()
        self.rubberBand: QRubberBand = None
        self.items_rects = None
        self.rubberBand_pal = QPalette()
        self.rubberBand_pal.setBrush(QPalette.Highlight, QBrush(QColor(255, 180, 176, 255)))
        self.verticalScrollBar().setSingleStep(1)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return:
            for action in self.actions():
                if action.text() == "&Open" or action.text() == "Open":
                    action.trigger()
        super().keyPressEvent(event)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() != Qt.RightButton:
            # Start Drawing RubberBand
            self.items_rects = self.get_items_rect()
            self.rubber_band_origin_pos: QPoint = self.mapFromGlobal(QCursor().pos())
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberBand.setPalette(self.rubberBand_pal)
            self.rubberBand.setGeometry(QRect(self.rubber_band_origin_pos, QSize()))
            self.rubberBand.show()

            modifiers = QApplication.keyboardModifiers()
            if modifiers != QtCore.Qt.ShiftModifier and modifiers != QtCore.Qt.ControlModifier:
                self.selectionModel().clearSelection()

            super().mousePressEvent(e)
        else:
            # IF Mouse not under selected indexes --> clear selection so No Selection Context Menu would appear
            indexes = self.selectionModel().selectedIndexes()
            for index in indexes:
                rect_visual = self.visualRect(index).normalized()
                model_rect = QRect(rect_visual.bottomLeft() + QPoint(0, 7), rect_visual.bottomRight() - (
                        rect_visual.topRight() - rect_visual.bottomRight()) + QPoint(0, 7))
                if model_rect.contains(self.mapFromGlobal(QCursor().pos())):
                    return
            self.selectionModel().clear()

    def mouseMoveEvent(self, event):
        if event.button() != Qt.RightButton:
            self.items_rects = self.get_items_rect()
            self.rubberBand.setGeometry(
                QRect(self.rubber_band_origin_pos, self.mapFromGlobal(QCursor().pos())).normalized())
            rect = QRect()
            rect.setTopLeft(self.rubberBand.pos())
            rect.setSize(self.rubberBand.rect().size())

            selected_indexes = []
            not_selected_indexes = []

            for key, value in self.items_rects.items():
                if rect.intersects(value):
                    selected_indexes.append(key)
                else:
                    if self.selectionModel().isSelected(key):
                        not_selected_indexes.append(key)

            if selected_indexes:
                self.selectionModel().select(QItemSelection(selected_indexes[0], selected_indexes[-1]),
                                             QItemSelectionModel.Select)
            if not_selected_indexes:
                self.selectionModel().select(QItemSelection(not_selected_indexes[0], not_selected_indexes[-1]),
                                             QItemSelectionModel.Deselect)


            if self.selectionModel().selectedIndexes():
                if rect.topLeft().y() < self.rubber_band_origin_pos.y():

                    self.scrollTo(self.selectionModel().selectedIndexes()[0])
                else:

                    self.scrollTo(self.selectionModel().selectedIndexes()[-1])

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() != Qt.RightButton:
            self.rubberBand.hide()

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        if self.items_rects:
            element_rect: QRect = self.items_rects[self.model().index(0, 0)]
            padding = element_rect.height() * (dy)
            self.rubber_band_origin_pos.setY(self.rubber_band_origin_pos.y() + padding)
        super().scrollContentsBy(dx, dy)


    def get_items_rect(self):
        result_dict = dict()  # {"modelIndex":rect() }
        for i in range(self.model().rowCount()):
            if self.model().hasIndex(i, 0):
                modelIndex = self.model().index(i, 0)
                rect_visual = self.visualRect(modelIndex).normalized()
                model_rect = QRect(rect_visual.bottomLeft() + QPoint(0, 8), rect_visual.bottomRight() - (
                        rect_visual.topRight() - rect_visual.bottomRight()) + QPoint(0, 8))
                result_dict[modelIndex] = model_rect
        return result_dict

    def initialize(self):

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setIndentation(0)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setUniformRowHeights(True)
        # self.setItemDelegateForColumn(2,CustomItemDelegate())
        self.setItemDelegate(CustomItemDelegate())
