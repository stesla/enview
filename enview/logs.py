import os
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

    def __eq__(self, obj):
        if isinstance(obj, Log):
            return self.path == obj.path
        return False

    def __lt__(self, obj):
        if isinstance(obj, Log):
            return self.mtime < obj.mtime
        return NotImplemented

    @property
    def fullpath(self):
        return logPath(self.path)

    @property
    def mtime(self):
        return os.path.getmtime(self.fullpath)

    def open(self):
        return open(self.fullpath, mode='r', encoding='utf8')
