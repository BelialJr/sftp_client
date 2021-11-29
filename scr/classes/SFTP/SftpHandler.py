import paramiko
paramiko.util.log_to_file("paramiko.log")
from scr.classes.Credential.Credentials import Credentials

class FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)




class SftpHandler:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None
        self.start_time = None


    def create_session(self):
        import time
        from datetime import timedelta

        start_time = time.time()
        self.start_time = time.time()
        # self.ssh.connect(self.credentials.host_name, port=self.credentials.port_number,
        #                  username=self.credentials.user_name, password=self.credentials.password)
        # print("--- %s seconds ---" % (time.time() - start_time))
        # self.sftp = self.ssh.open_sftp()
        #print("--- %s seconds ---" % (time.time() - start_time))

        self.ssh = FastTransport((self.credentials.host_name, int(self.credentials.port_number)))
        print("--- %s seconds ---" % (time.time() - start_time))
        self.ssh.connect(username=self.credentials.user_name, password=self.credentials.password)
        print("--- %s seconds ---" % (time.time() - start_time))
        self.sftp = paramiko.SFTPClient.from_transport( self.ssh)
        print("--- %s seconds ---" % (time.time() - start_time))


    def close(self):
        if self.sftp:
            self.sftp.close()
        self.ssh.close()

    def __del__(self):
        if self.sftp:
            self.sftp.close()
            self.ssh.close()

