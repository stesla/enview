import os
import time
from posixpath import join as urljoin

import logging
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request
app = Flask(__name__)

from werkzeug.exceptions import NotFound

from .logs import grep, isDir, listLogs, Log
from .markup import parse

@app.route('/favicon.ico')
def favicon():
    return NotFound()

@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>')
def logs(path):
    if isDir(path):
        ps = listLogs(path)
        dirs = sorted([dir for dir in ps if dir.isdir],
                    key=lambda f: f.path, reverse=True)
        files = sorted([file for file in ps if not file.isdir],
                    key=lambda f: f.mtime, reverse=True)
        return render_template('directory.html', crumbs=crumbs(path), dirs=dirs, files=files, path=path)
    else:
        with Log(path).open() as f:
            text = f.read()
        html = ''.join(t.to_html() for t in parse(text))
        return render_template('log.html', crumbs=crumbs(path), path=path, html=html)

@app.route('/search/', methods=['GET'], defaults={'path': ''})
@app.route('/search/<path:path>')
def search(path):
    logger.info(f'PATH = {repr(path)}')
    query = request.args.get('q')
    grep_results = grep(query, path)
    results = [
        (urljoin('/', path, str(log)), str(log), ''.join(t.to_html() for t in parse("\n".join(lines))))
        for (log, lines) in sorted([result for result in grep_results], key=lambda f: str(f[0]))
    ]
    return render_template('search.html', crumbs=crumbs(path), results=results, query=query)

@app.template_filter()
def datetime(value):
    return time.strftime("%Y-%m-%d %H:%M:%S", value)

def crumbs(path):
    list = []
    while path:
        list.append((path, os.path.basename(path)))
        path = os.path.dirname(path)
    return reversed(list)
