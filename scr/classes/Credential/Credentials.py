from scr.classes.Crypto import Base64


class Credentials:

    def __init__(self, file_protocol, host_name, port_number, user_name, password):
        self.file_protocol = file_protocol
        self.host_name = host_name
        self.port_number = port_number
        self.user_name = user_name
        self.password = password

    def __str__(self) -> str:
        return f"file protocol:{self.file_protocol} :host name {self.host_name} " \
               f"port number: {self.port_number} :user name {self.user_name} : password {self.password} :"

    def encode(self):
        self.password = Base64.encode(self.password)

    def decode(self):
        self.password = Base64.decode(self.password)

    @classmethod
    def create_from_dict(cls, dict):
        file_protocol = dict["file_protocol"]
        host_name = dict["host_name"]
        port_number = dict["port_number"]
        user_name = dict["user_name"]
        password = dict["password"]
        return Credentials(file_protocol, host_name, port_number, user_name, password)

    @classmethod
    def parse_dict_list(cls, dict_list):
        creadentials_list = []
        for dict in dict_list:
            creadentials_list.append(cls.create_from_dict(dict))
        return creadentials_list
