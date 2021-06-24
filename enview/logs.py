import os
import time
from pathlib import Path

from .markup import parse_text

LOG_ROOT = Path(os.getenv("LOGS_ROOT", "~/rplogs")).expanduser()

def grep(query, path):
    def _grep():
        for log in listLogs(path):
            if log.isdir:
                continue
            lines = log.grep(query)
            if lines:
                yield (log, lines)
    return list(_grep())

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

    def grep(self, query):
        try:
            results = []
            with self.open() as f:
                for line in f:
                    if query in parse_text(line):
                        results.append(line)
            return results
        except:
            return []

    def open(self):
        return open(self.fullpath, mode='r', encoding='utf8')
