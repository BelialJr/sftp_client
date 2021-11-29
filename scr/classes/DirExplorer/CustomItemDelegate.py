import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QModelIndex, QEvent, QAbstractItemModel, Qt
from PyQt5.QtGui import QPainter, QPalette, QBrush, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem, QItemDelegate


class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem , index: QModelIndex) -> None:

            if index.column() != 0:
                QStyledItemDelegate.paint(self, painter, option, index)
                # if option.state & QStyle.State_MouseOver:
                #     print('Over')
                #     print(f"{index.row()}  : {index.column()}")
                   
                    # #painter.fillRect (option.rect, Qt.white)
                    # font = option.font
                    # font.setPointSize(option.font.pointSize())
                    # painter.setFont(font)
                    #
                    # option.backgroundBrush = QBrush(QColor(Qt.white))
                    # option.widget.style().drawPrimitive(QStyle.PE_PanelItemViewItem,option,painter)
                    # option.widget.style().drawItemText(painter,option.rect,Qt.AlignLeft | Qt.AlignVCenter,option.palette,True,index.data())


            else:
                if option.state & QStyle.State_MouseOver:

                    option.backgroundBrush = QBrush(QColor( 255, 203, 176))
                    option.widget.style().drawPrimitive(QStyle.PE_PanelItemViewItem,option,painter)
                QStyledItemDelegate.paint(self, painter, option, index)


