from stat import *
import platform
import os


def is_hidden(file):
    if platform.system() == "Windows":
        stat = os.stat(file)

        return file.name.startswith(".") or stat.st_file_attributes == FILE_ATTRIBUTE_HIDDEN
    else:
        return file.name.startswith(".")