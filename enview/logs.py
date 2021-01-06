import os
from pathlib import Path

root = Path(os.getenv("LOGS_ROOT", "~/rplogs")).expanduser()

def isDir(path):
    p = os.path.join(root, path)
    return os.path.isdir(p)

def listLogs(path):
    p = os.path.join(root, path)
    return os.listdir(p)

def openLog(path):
    p = os.path.join(root, path)
    return open(p, mode='r')
