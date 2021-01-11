import os
import time
from pathlib import Path

LOG_ROOT = Path(os.getenv("LOGS_ROOT", "~/rplogs")).expanduser()

def isDir(path):
    return os.path.isdir(logPath(path))

def listLogs(path):
    return [Log(os.path.join(path, f)) for f in os.listdir(logPath(path))]

def logPath(path):
    return os.path.join(LOG_ROOT, path)

class Log:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return os.path.basename(self.path)

    @property
    def fullpath(self):
        return logPath(self.path)

    @property
    def isdir(self):
        return os.path.isdir(self.fullpath)

    @property
    def mtime(self):
        return time.localtime(os.path.getmtime(self.fullpath))

    def open(self):
        return open(self.fullpath, mode='r', encoding='utf8')
