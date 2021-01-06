import os
import re

import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

from .logs import isDir, listLogs, openLog

@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>')
def logs(path):
    if isDir(path):
        files = listLogs(path)
        return render_template('directory.html', files=files)
    else:
        with openLog(path) as f:
            text = f.read()
        text = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', text)
        return render_template('log.html', text=text)
