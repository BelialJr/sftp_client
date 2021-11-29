from scr.classes.SFTP.SftpHandler import SftpHandler
import paramiko

class Session:
    start_path = '.'

    def __init__(self, sftp_handler:SftpHandler):
        self.sftp_handler = sftp_handler
        self.sftp_handler.sftp.chdir(Session.start_path)


