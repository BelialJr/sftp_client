# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'session_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


from scr.classes.Credential.Credentials import Credentials


class Ui_NewSession(QtWidgets.QMainWindow):


    def __init__(self):
        super().__init__()

    def setupUi(self, NewSession):

        NewSession.setObjectName("NewSession")
        NewSession.setWindowModality(QtCore.Qt.NonModal)
        NewSession.resize(495, 233)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewSession.sizePolicy().hasHeightForWidth())
        NewSession.setSizePolicy(sizePolicy)
        NewSession.setMinimumSize(QtCore.QSize(495, 233))
        NewSession.setMaximumSize(QtCore.QSize(495, 233))
        NewSession.setBaseSize(QtCore.QSize(495, 233))
        NewSession.setFocusPolicy(QtCore.Qt.TabFocus)
        NewSession.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QtWidgets.QGridLayout(NewSession)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(NewSession)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(200)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_3 = QtWidgets.QLineEdit(NewSession)
        self.lineEdit_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(215, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(NewSession)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.save_check_box = QtWidgets.QCheckBox(NewSession)
        self.save_check_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.save_check_box.setObjectName("save_check_box")
        self.horizontalLayout_5.addWidget(self.save_check_box)
        self.open_button = QtWidgets.QPushButton(NewSession)
        self.open_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.open_button.setObjectName("open_button")
        self.horizontalLayout_5.addWidget(self.open_button)
        spacerItem = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.login_button = QtWidgets.QPushButton(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_button.sizePolicy().hasHeightForWidth())
        self.login_button.setSizePolicy(sizePolicy)
        self.login_button.setObjectName("login_button")
        self.horizontalLayout_5.addWidget(self.login_button)
        self.close_button = QtWidgets.QPushButton(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout_5.addWidget(self.close_button)
        self.gridLayout.addLayout(self.horizontalLayout_5, 7, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_4.addWidget(self.lineEdit_5)
        self.lineEdit_4 = QtWidgets.QLineEdit(NewSession)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(238, 0))
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_4.addWidget(self.lineEdit_4)
        self.gridLayout.addLayout(self.horizontalLayout_4, 6, 0, 1, 1)

        self.retranslateUi(NewSession)
        QtCore.QMetaObject.connectSlotsByName(NewSession)

    def retranslateUi(self, NewSession):
        _translate = QtCore.QCoreApplication.translate
        NewSession.setWindowTitle(_translate("NewSession", "New Session"))
        self.label.setText(_translate("NewSession", "File Protocol:"))
        self.label_3.setText(_translate("NewSession", "Host Name:"))
        self.label_2.setText(_translate("NewSession", "Port number:"))
        self.label_5.setText(_translate("NewSession", "User name:"))
        self.label_4.setText(_translate("NewSession", "Password:"))
        self.save_check_box.setText(_translate("NewSession", "Save"))
        self.open_button.setText(_translate("NewSession", "Open"))
        self.login_button.setText(_translate("NewSession", "Login"))
        self.close_button.setText(_translate("NewSession", "Close"))
        self.lineEdit.setText("SFTP")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setText("22")
        self.lineEdit_2.setReadOnly(True)




    def get_credentials(self):
       credential =  Credentials(self.lineEdit.text(),self.lineEdit_3.text(),self.lineEdit_2.text(),
                          self.lineEdit_5.text(),self.lineEdit_4.text())
       credential.decode()
       return credential

    def set_credentials(self,credential:Credentials):
       self.lineEdit_3.setText(credential.host_name)
       self.lineEdit_5.setText(credential.user_name)
       self.lineEdit_4.setText(credential.password)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewSession = QtWidgets.QDialog()
    ui = Ui_NewSession()
    ui.setupUi(NewSession)
    NewSession.show()
    sys.exit(app.exec_())