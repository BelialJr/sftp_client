from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime


class IconBuffer:
    files_to_buffer =      {} #suffix :Buffer (icon,ttl)
    executable_to_buffer = {} #suffix :Buffer (icon,ttl)
    qFileIconProvider = QFileIconProvider()
    TTL_DEF = 500 #in seconds


    @classmethod
    def get_icon(cls,target_file:QFileInfo):

        current_time = datetime.datetime.now()

        if target_file.isDir():
            return qApp.style().standardIcon(QStyle.SP_DirIcon)

        else:
            file_key = None
            if target_file.isFile():
                file_key = target_file.suffix()
            if target_file.isExecutable():
                file_key = target_file.absoluteFilePath()

            buffer = cls.files_to_buffer.get(file_key)

            if buffer:
                if current_time > buffer.ttl:
                    buffer.icon = cls.qFileIconProvider.icon(QFileInfo(target_file.absoluteFilePath()))
                    buffer.ttl = current_time + datetime.timedelta(seconds=cls.TTL_DEF)
                else:
                    buffer.ttl = current_time + datetime.timedelta(seconds=cls.TTL_DEF)
                return buffer.icon
            else:
                new_icon = cls.qFileIconProvider.icon(QFileInfo(target_file.absoluteFilePath()))
                new_ttl = current_time + datetime.timedelta(seconds=cls.TTL_DEF)
                buffer = Buffer(new_icon,new_ttl)
                cls.files_to_buffer.update({file_key:buffer})
                return new_icon


class Buffer:
    def __init__(self,icon:QIcon,ttl:datetime):
        self.icon = icon
        self.ttl = ttl

