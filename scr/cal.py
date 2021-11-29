import traceback

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QFile

from PyQt5.QtGui import QIcon, QPixmap, QFont, QTransform
from PyQt5.QtWidgets import QStyle, QPushButton, QApplication, QSpacerItem, QSizePolicy

from scr.classes.Credential.CredentialHadler import CredentialHadler
from scr.classes.Credential.Credentials import Credentials
from scr.classes.DirExplorer.Local.Cust_TreeView import  Cust_TreeView
from scr.classes.DirExplorer.Local.LocalDirExplorer import LocalDirExplorer
from scr.classes.DirExplorer.Remote.RemoteDirExplorer import RemoteDirExplorer
from scr.classes.DirPanelButtons.LocalDirPanelButtons import LocalDirPanelButtons, LocalDirPanelButtons
from scr.classes.DirPanelButtons.RemoteDirPanelButtons import RemoteDirPanelButtons
from scr.classes.SFTP.SftpHandler import SftpHandler
from scr.classes.Session.SessionHandler import SessionHandler
from scr.classes.Session.Ui_NewSessionWindow import Ui_NewSession
from scr.classes.View.ThemeView import ThemeView


class Ui_MainWindow(object):
    current_style_sheet = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("SFTP client ")
        MainWindow.resize(1123, 639)
        self.mainWindow = MainWindow



        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout_3 = QtWidgets.QHBoxLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")

        # self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_6.setObjectName("pushButton_6")
        # self.pushButton_6.setMinimumSize(QtCore.QSize(85, 25))
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(   self.pushButton_6.sizePolicy().hasHeightForWidth())
        # self.pushButton_6.setSizePolicy(sizePolicy)
        # spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gridLayout_3.addWidget(self.pushButton_6)
        # self.gridLayout_3.addItem(spacerItem5)






        self.verticalLayout_7.addLayout(self.gridLayout_3)
        self.session_layout = QtWidgets.QHBoxLayout()
        self.session_layout.setObjectName("session_layout")
        self.new_session_button_local = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_session_button_local.sizePolicy().hasHeightForWidth())
        self.new_session_button_local.setSizePolicy(sizePolicy)
        self.new_session_button_local.setObjectName("new_session_button_local")
        self.session_layout.addWidget(self.new_session_button_local)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.session_layout.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.session_layout)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(3)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.local_driver_chooser = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.local_driver_chooser.sizePolicy().hasHeightForWidth())
        self.local_driver_chooser.setSizePolicy(sizePolicy)
        self.local_driver_chooser.setMaximumSize(QtCore.QSize(120, 16777215))

        self.local_driver_chooser.setObjectName("local_driver_chooser")
        self.horizontalLayout.addWidget(self.local_driver_chooser)

        verticalSpacer = QSpacerItem(1, 26, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(verticalSpacer)


        self.go_back_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( self.go_back_button.sizePolicy().hasHeightForWidth())
        icon = QIcon('../icons/7768642.png')

        self.go_back_button.setSizePolicy(sizePolicy)
        self.go_back_button.setMinimumSize(QtCore.QSize(40, 26))
        self.go_back_button.setMaximumSize(QtCore.QSize(40, 26))
        self.go_back_button.setObjectName("go_forward_button")
        self.go_back_button.setToolTip('Got back')

        self.go_back_button.setIcon(icon)
        self.go_back_button.setStyleSheet(
            "QPushButton  { background-color:  rgb(224, 224, 224); border:0px solid #808080; } QPushButton:hover { background-color:  rgb(233, 136, 66); }")
        self.horizontalLayout.addWidget(self.go_back_button)


        self.go_forward_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth( self.go_forward_button.sizePolicy().hasHeightForWidth())
        self.go_forward_button.setSizePolicy(sizePolicy)
        self.go_forward_button.setMinimumSize(QtCore.QSize(40, 26))
        self.go_forward_button.setMaximumSize(QtCore.QSize(40, 26))
        self.go_forward_button.setObjectName("go_forward_button")
        self.go_forward_button.setToolTip('Got forward')
        self.go_forward_button.setIcon(QIcon('../icons/776864.png'))
        self.go_forward_button.setStyleSheet(
            "QPushButton  { background-color:  rgb(224, 224, 224); border-left:1px solid #808080;border-top: 0px; border-bottom: 0px; border-right: 0px; } } QPushButton:hover { background-color:  rgb(233, 136, 66); }")
        self.horizontalLayout.addWidget(self.go_forward_button)

        verticalSpacer = QSpacerItem(20, 26, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(verticalSpacer)

        self.push_button_root_dir_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_root_dir_local.sizePolicy().hasHeightForWidth())
        self.push_button_root_dir_local.setSizePolicy(sizePolicy)
        self.push_button_root_dir_local.setMinimumSize(QtCore.QSize(30, 26))
        self.push_button_root_dir_local.setMaximumSize(QtCore.QSize(30, 26))
        self.push_button_root_dir_local.setObjectName("push_button_root_dir_local")
        self.push_button_root_dir_local.setToolTip('Got to root directory')
        self.push_button_root_dir_local.setIcon(QIcon('../icons/folder_root_1.png'))
        self.push_button_root_dir_local.setStyleSheet("QPushButton  { background-color:  rgb(224, 224, 224); border: 0px } QPushButton:hover { background-color:  rgb(233, 136, 66); }")
        self.horizontalLayout.addWidget(self.push_button_root_dir_local)



        self.push_button_parent_dir_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_parent_dir_local.sizePolicy().hasHeightForWidth())
        self.push_button_parent_dir_local.setSizePolicy(sizePolicy)
        self.push_button_parent_dir_local.setMinimumSize(QtCore.QSize(30, 26))
        self.push_button_parent_dir_local.setMaximumSize(QtCore.QSize(30, 26))
        self.push_button_parent_dir_local.setObjectName("push_button_parent_dir_local")
        self.push_button_parent_dir_local.setIcon(QIcon('../icons/folder_parent2.png'))
        self.push_button_parent_dir_local.setToolTip('Got to parent directory')
        self.push_button_parent_dir_local.setStyleSheet(
            "QPushButton  { background-color:  rgb(224, 224, 224); border: 0px } QPushButton:hover { background-color:  rgb(233, 136, 66); }")
        self.horizontalLayout.addWidget(self.push_button_parent_dir_local)

        self.push_button_home_dir_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_home_dir_local.sizePolicy().hasHeightForWidth())
        self.push_button_home_dir_local.setSizePolicy(sizePolicy)
        self.push_button_home_dir_local.setMinimumSize(QtCore.QSize(30, 26))
        self.push_button_home_dir_local.setMaximumSize(QtCore.QSize(30, 26))
        self.push_button_home_dir_local.setObjectName("push_button_home_dir_local")
        self.push_button_home_dir_local.setIcon(QIcon('../icons/house.png'))
        self.push_button_home_dir_local.setToolTip('Got to home directory')
        self.push_button_home_dir_local.setStyleSheet("QPushButton  { background-color:  rgb(224, 224, 224); border: 0px } QPushButton:hover { background-color:  rgb(233, 136, 66); }")
        self.horizontalLayout.addWidget(self.push_button_home_dir_local)

        self.push_button_refresh_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_refresh_local.sizePolicy().hasHeightForWidth())
        self.push_button_refresh_local.setSizePolicy(sizePolicy)
        self.push_button_refresh_local.setMaximumSize(QtCore.QSize(30, 26))
        self.push_button_refresh_local.setMinimumSize(QtCore.QSize(30, 26))
        self.push_button_refresh_local.setObjectName("push_button_refresh_local")
        self.push_button_refresh_local.setToolTip('Refresh local context')
        self.push_button_refresh_local.setIcon(QIcon('../icons/refresh3.png'))
        self.push_button_refresh_local.setStyleSheet("QPushButton  { background-color:  rgb(224, 224, 224); border: 0px } QPushButton:hover { background-color:  rgb(233, 136, 66); }")

        self.horizontalLayout.addWidget(self.push_button_refresh_local)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")


        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()





        self.push_button_upload_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.push_button_upload_local.setToolTip('Upload selected files')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(  self.push_button_upload_local.sizePolicy().hasHeightForWidth())
        self.push_button_upload_local.setSizePolicy(sizePolicy)
        self.push_button_upload_local.setMaximumSize(QtCore.QSize(1798, 26))
        self.push_button_upload_local.setIcon(QIcon('../icons/submit.png'))

        self.push_button_upload_local.setObjectName("push_button_upload_local")

        self.horizontalLayout_5.addWidget(self.push_button_upload_local)

        self.push_button_edit_local = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.push_button_edit_local.setToolTip('Edit selected file')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_edit_local.sizePolicy().hasHeightForWidth())
        self.push_button_edit_local.setSizePolicy(sizePolicy)
        self.push_button_edit_local.setMinimumSize(QtCore.QSize(78, 26))
        self.push_button_edit_local.setMaximumSize(QtCore.QSize(78, 26))
        self.push_button_edit_local.setIcon(QIcon('../icons/document.png'))
        self.push_button_upload_local.setObjectName("push_button_edit_local")

        self.horizontalLayout_5.addWidget(self.push_button_edit_local)

        self.hidden_show_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hidden_show_button.sizePolicy().hasHeightForWidth())
        self.hidden_show_button.setSizePolicy(sizePolicy)

        self.hidden_show_button.setMinimumSize(QtCore.QSize(30, 26))
        self.hidden_show_button.setMaximumSize(QtCore.QSize(30, 26))

        self.hidden_show_button.setIcon(QIcon('../icons/hide.png'))
        self.hidden_show_button.setToolTip('Show/Hide hidden files')
        self.hidden_show_button.setStyleSheet('QPushButton  { background-color:  rgb(224, 224, 224); border: 0px } QPushButton:hover { background-color:  rgb(233, 136, 66); }  QPushButton:checked { background-color:  rgb(233, 136, 66); }')
        self.hidden_show_button.setCheckable(True)
        self.hidden_show_button.clicked.connect(self.hidden_show_button_clicked)
        self.horizontalLayout_5.addWidget(self.hidden_show_button)

        self.horizontalLayout_5.addItem(spacerItem1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.local_path_bar = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.local_path_bar.setReadOnly(True)
        self.local_path_bar.setObjectName("local_path_bar")
        self.verticalLayout_3.addWidget(self.local_path_bar)
        self.local_TreeView = Cust_TreeView(self.verticalLayoutWidget)
        self.local_TreeView.setObjectName("local_TreeView")
        self.verticalLayout_3.addWidget(self.local_TreeView)
        self.local_status_bar = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.local_status_bar.setReadOnly(True)
        self.local_status_bar.setObjectName("local_status_bar")
        self.verticalLayout_3.addWidget(self.local_status_bar)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")




        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)
        self.remote_download = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remote_download.sizePolicy().hasHeightForWidth())
        self.remote_download.setSizePolicy(sizePolicy)
        self.remote_download.setMinimumSize(QtCore.QSize(78, 26))
        self.remote_download.setMaximumSize(QtCore.QSize(105, 26))
        self.remote_download.setObjectName("remote_download")
        self.remote_download.setIcon(QIcon('../icons/download.png'))
        self.horizontalLayout_7.addWidget(self.remote_download)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.remote_path_bar = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.remote_path_bar.setReadOnly(True)
        self.remote_path_bar.setObjectName("remote_path_bar")
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6.addWidget(self.remote_path_bar)
        self.remote_TreeView =Cust_TreeView(self.verticalLayoutWidget_2)
        self.remote_TreeView.setObjectName("remote_TreeView")
        self.verticalLayout_6.addWidget(self.remote_TreeView)
        self.remote_status_bar = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.remote_status_bar.setReadOnly(True)
        self.remote_status_bar.setObjectName("remote_status_bar")
        self.verticalLayout_6.addWidget(self.remote_status_bar)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addWidget(self.splitter)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.connected_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.connected_line_edit.setReadOnly(True)
        self.connected_line_edit.setObjectName("connected_line_edit")
        self.horizontalLayout_3.addWidget(self.connected_line_edit)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(40, 16777215))
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_3.addWidget(self.lineEdit_5)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_3.addWidget(self.lineEdit_7)
        font_for_time = QFont()
        font_for_time.setPointSize(9)
        self.time_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.time_line_edit.setMaximumSize(QtCore.QSize(70, 16777215))
        self.time_line_edit.setReadOnly(True)
        self.time_line_edit.setObjectName("time_line_edit")
        self.time_line_edit.setFont(font_for_time)
        self.horizontalLayout_3.addWidget(self.time_line_edit)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 623, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuLocal = QtWidgets.QMenu(self.menuBar)
        self.menuLocal.setObjectName("menuLocal")
        self.menuLocal.setDisabled(True)

        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuLocal.menuAction())
        self.menuView = QtWidgets.QMenu(self.menuBar)


        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuView.menuAction())

        self.menuSession = QtWidgets.QMenu(self.menuBar)
        self.menuSession.setDisabled(True)
        self.menuBar.addAction(self.menuSession.menuAction())
        self.init_components()
        self.mainWindow.setWindowIcon(QIcon('../icons/sftp1.png'))
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SFTP client"))
        self.new_session_button_local.setText(_translate("MainWindow", "New session"))
        self.connected_line_edit.setText('Not Connected')
        self.push_button_edit_local.setText(_translate("MainWindow", "Edit"))
        self.push_button_upload_local.setText(_translate("MainWindow", "Upload"))
        self.remote_download.setText(_translate("MainWindow", "Download"))
        self.menuLocal.setTitle(_translate("MainWindow", "Local"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuSession.setTitle(_translate("MainWindow", "Session"))


    def init_components(self):
        ThemeView.set_menu(self.menuView,app)

        self.local_dir_buttons_panel = LocalDirPanelButtons()
        self.local_dir_buttons_panel.set_mainwindow(self.mainWindow)
        self.local_dir_buttons_panel.set_driver_chooser(self.local_driver_chooser)
        self.local_dir_buttons_panel.set_parent_dir_button(self.push_button_parent_dir_local)
        self.local_dir_buttons_panel.set_root_dir_button(self.push_button_root_dir_local)
        self.local_dir_buttons_panel.set_home_dir_button(self.push_button_home_dir_local)
        self.local_dir_buttons_panel.set_refresh_button(self.push_button_refresh_local)
        self.local_dir_buttons_panel.set_edit_button(self.push_button_edit_local)
        self.local_dir_buttons_panel.set_upload_button(self.push_button_upload_local)
        self.local_dir_buttons_panel.set_button_go_back(self.go_back_button)
        self.local_dir_buttons_panel.set_button_go_forward(self.go_forward_button)

        self.local_dir_explorer = LocalDirExplorer(self.local_TreeView, self.local_path_bar, self.local_status_bar,self.local_dir_buttons_panel.update_driver_chooser)
        self.local_dir_buttons_panel.set_dir_explorer(self.local_dir_explorer)
        self.remote_dir_explorer = RemoteDirExplorer(self.remote_TreeView, self.remote_path_bar, self.remote_status_bar)
        self.local_dir_buttons_panel.set_remote_dir_explorer(self.remote_dir_explorer)

        self.remote_dir_buttons_panel = RemoteDirPanelButtons(self.remote_download,self.comboBox_2,  self.remote_dir_explorer,self.local_dir_explorer)

        self.session_handler = SessionHandler(self.remote_dir_buttons_panel,self.new_session_button_local, self.menuSession,self.remote_dir_explorer,self.mainWindow,self.connected_line_edit,self.time_line_edit)
        self.local_dir_buttons_panel.set_session_handler(self.session_handler)

    def hidden_show_button_clicked(self):
        self.local_dir_explorer.change_hidden_visible()
        self.local_dir_explorer.update_dir_data()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
