import os
import json
import base64

import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QMessageBox
from pyxtension.streams import stream

from scr.classes.Credential.Credentials import Credentials


class CredentialHadler:
    programDirName = "CustomApplication"
    dataFileName = "data.json"
    dataFilePath = ''
    def_config_data = {'accounts': []}
    current_config_data = []
    data = {"file_protocol": "", "host_name": "", "port_number": "", "user_name": "", "password": ""}

    @classmethod
    def locate_config_file(cls):
        dir_path = os.environ['APPDATA'] + "\\" + cls.programDirName
        cls.dataFilePath = dir_path + "\\" + cls.dataFileName

        if os.path.isdir(dir_path):
            if not os.path.isfile(cls.dataFilePath):
                CredentialHadler.generate_config_file(cls.dataFilePath)
        else:
            os.makedirs(dir_path)
            CredentialHadler.generate_config_file(cls.dataFilePath)

    @classmethod
    def get_saved_credentials(cls):
        saved_credentials = []
        try:
            with open(cls.dataFilePath, "r") as file:
                data = json.load(file)
                saved_credentials = Credentials.parse_dict_list(data["accounts"])
                #saved_credentials.decode()
        except Exception:
            pass
            # traceback.print_exc()
        return saved_credentials

    @classmethod
    def save_credential(cls, credentials):

        with open(cls.dataFilePath, "r+") as file:
            data = json.load(file)
            credentials.encode()

            if cls.credentials_already_exist(credentials, data):
                if cls.should_override(credentials):
                    for d in data['accounts']:
                        if credentials.host_name in d.values() and credentials.user_name in d.values():
                            data['accounts'].remove(d)
                else:
                    credentials.decode()
                    return

            data["accounts"].append(vars(credentials))
            file.seek(0)
            json.dump(data, file,indent=4)
            credentials.decode()

    @classmethod
    def remove_credential(cls,credentials):
        if not cls.should_remove(credentials):
            return
        with open(cls.dataFilePath, "r+") as file:
            try:
                data = json.load(file)
                print(data)
                temp = filter(lambda item:False if credentials.host_name == item['host_name'] and credentials.user_name ==item['user_name'] else True, data["accounts"])
                data["accounts"] = list(temp)
                print(data)
                file.truncate(0)
                file.seek(0)
                json.dump(data, file,indent=4)
            except Exception:
                traceback.print_exc()

    @classmethod
    def credentials_already_exist(cls, credentials, data):
        for d in data['accounts']:
            if credentials.host_name in d.values() and credentials.user_name in d.values():
                # data['accounts'].remove(d)
                return True
        return False

    @classmethod
    def generate_config_file(cls, path):
        with open(path, "a") as file:
            json.dump(cls.def_config_data, file)

    @classmethod
    def should_override(cls, credentials):
        msgbox = QMessageBox(QMessageBox.Question, "Confirm credential overriding",
                             f"Are you sure you want to override already existing credentials :[{credentials.host_name} : {credentials.user_name}]?")
        msgbox.setWindowFlag( Qt.WindowStaysOnTopHint)
        msgbox.addButton(QMessageBox.Yes)
        msgbox.addButton(QMessageBox.No)

        reply = msgbox.exec()

        return reply == QMessageBox.Yes

    @classmethod
    def should_remove(cls, credentials):
        msgbox = QMessageBox(QMessageBox.Question, "Confirm credential removing",
                             f"Are you sure you want to remove  credentials :[{credentials.host_name} : {credentials.user_name}]?")
        msgbox.setWindowFlag(Qt.WindowStaysOnTopHint)
        msgbox.addButton(QMessageBox.Yes)
        msgbox.addButton(QMessageBox.No)
        reply = msgbox.exec()

        return reply == QMessageBox.Yes
