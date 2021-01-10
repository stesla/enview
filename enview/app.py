import os

import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

from .logs import isDir, listLogs, Log
from .markup import parse

@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>')
def logs(path):
    if isDir(path):
        files = listLogs(path)
        return render_template('directory.html', files=sorted(files, reverse=True))
    else:
        with Log(path).open() as f:
            text = f.read()
        html = ''.join(t.to_html() for t in parse(text))
        return render_template('log.html', html=html)

