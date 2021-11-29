import time
import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import *

from PyQt5.QtWidgets import *

from scr.classes.Credential.CreadentialsChooserWindow import CredentialsChooserWindow
from scr.classes.Credential.CredentialHadler import CredentialHadler
from scr.classes.Credential.Credentials import Credentials
from scr.classes.DirExplorer.Remote.RemoteDirExplorer import RemoteDirExplorer
from scr.classes.DirPanelButtons.RemoteDirPanelButtons import RemoteDirPanelButtons
from scr.classes.SFTP.SftpHandler import SftpHandler
from scr.classes.Session.Session import Session
from scr.classes.Session.Ui_NewSessionWindow import Ui_NewSession


class SessionHandler:
    ONE_OR_MORE_CONNECTED_FLAG = False

    def __init__(self,remote_dir_buttons_panel:RemoteDirPanelButtons, new_session_button: QPushButton, menuSession :QMenu, dir_explorer: RemoteDirExplorer, main_window: QMainWindow,connected_line_edit :QLineEdit,time_line_edit:QLineEdit):
        CredentialHadler.locate_config_file()
        self.timer= QTimer()
        self.remote_dir_buttons_panel = remote_dir_buttons_panel
        self.connected_line_edit = connected_line_edit
        self.time_line_edit = time_line_edit
        self.connected_line_edit.setText("Not connected")
        self.sessions_list = []
        self.sessions_menuAction = dict()
        self.new_session_ui = None
        self.new_session_window = None
        self.credentials_new_session_ui = None
        self.credentials_session_window = None
        self.menuSession = menuSession
        self.main_window = main_window
        self.new_session_button = new_session_button
        self.remote_dir_explorer = dir_explorer
        self.remote_dir_explorer.disable_components(True)
        self.remote_dir_buttons_panel.disable_components(True)
        self.new_session_button.clicked.connect(self.open_new_session_window)

    def open_new_session_window(self):
        self.new_session_window = QDialog()
        self.new_session_ui = Ui_NewSession()
        self.new_session_ui.setupUi(self.new_session_window)
        self.new_session_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.new_session_window.raise_()
        self.new_session_window.closeEvent = self.close_event
        self.new_session_window.showEvent = self.show_event
        self.new_session_ui.close_button.clicked.connect(self.close_clicked)
        self.new_session_ui.login_button.clicked.connect(self.login_event)
        self.new_session_ui.open_button.clicked.connect(self.open_clicked)
        self.new_session_window.show()




    #-------------------EVENTS-------------------------#
    def close_clicked(self):
        self.new_session_window.close()


    def open_clicked(self):
        self.credentials_session_window = QDialog()
        self.credentials_ui = CredentialsChooserWindow(self.new_session_ui)
        self.credentials_ui.setupUi(self.credentials_session_window)
        self.credentials_session_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.credentials_session_window.raise_()
        self.credentials_session_window.closeEvent = self.credetials_close_event
        self.credentials_session_window.showEvent = self.credetials_show_event
        self.credentials_session_window.show()



    def login_event(self):
        print('login pressed')

        credentials = self.new_session_ui.get_credentials()


        if self.new_session_ui.save_check_box.isChecked():
            CredentialHadler.save_credential(credentials)

        sftp_handler = None
        session = None
        try:
            sftp_handler = SftpHandler(credentials)
            print('session creation')
            sftp_handler.create_session()
            print('session created')
            session = Session(sftp_handler)
            self.add_session(session)
            self.remote_dir_explorer.set_current_session(session)
            self.set_action_checked(self.sessions_menuAction[session],session)
            self.new_session_window.close()

        except Exception as e:
            traceback.print_exc()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error occurred while connecting to SFTP server")
            msg.setWindowTitle("Error")
            msg.setWindowFlag(Qt.WindowStaysOnTopHint)
            msg.exec_()

    def close_event(self, e):
        self.main_window.setDisabled(False)

    def show_event(self, e):
        self.main_window.setDisabled(True)

    def credetials_close_event(self, e):
        self.new_session_window.show()

    def credetials_show_event(self, e):
        self.new_session_window.hide()


    def showTime(self,session):
        hours, rem = divmod(time.time() - session.sftp_handler.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        self.time_line_edit.setText("{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds)))


    #-------------------SESSION--------------------------#

    def add_session(self, session: Session):
        if len(self.sessions_list) == 0:
            SessionHandler.ONE_OR_MORE_CONNECTED_FLAG = True
            self.remote_dir_explorer.disable_components(False)
            self.remote_dir_buttons_panel.disable_components(False)
            self.connected_line_edit.setText("Connected")
        self.sessions_list.append(session)
        self.add_action(session)


    def remove_session(self, session: Session):
        self.sessions_list.remove(session)
        if len(self.sessions_list) == 0:
            SessionHandler.ONE_OR_MORE_CONNECTED_FLAG = False
            self.remote_dir_explorer.disable_components(True)
            self.remote_dir_buttons_panel.disable_components(True)
            self.connected_line_edit.setText("Not connected")
        self.remove_action(session)

    def add_action(self, session: Session):
        action_name = session.sftp_handler.credentials.host_name + ' : ' + session.sftp_handler.credentials.user_name

        action = self.menuSession.addAction(action_name,lambda:(
                            self.remote_dir_explorer.set_current_session(session),
                            self.set_action_checked(action,session)))

        action.setCheckable(True)
        self.sessions_menuAction.update({session:action})
        self.menuSession.setDisabled(False)


    def remove_action(self, session: Session):
        action = self.sessions_menuAction.pop(session)
        self.menuSession.removeAction(action)
        if len(self.sessions_menuAction.keys()) == 0:
            self.menuSession.setDisabled(True)


    def set_action_checked(self,action,session):
        for a in  self.sessions_menuAction.values():
            a.setChecked(False)
        action.setChecked(True)

        self.timer.timeout.connect(lambda : self.showTime(session))
        self.timer.setInterval(1000)
        self.timer.start()