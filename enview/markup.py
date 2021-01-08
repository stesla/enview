import re

CODE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

def strip(text):
    return re.sub(CODE, '', text)

def parse(text):
    if not text:
        return []
    t = Text()
    ts = []
    state = parsePlain
    for c in text:
        t, state = state(c, t, ts)
    ts.append(t)
    return ts

class Text:
    def __init__(self, text='', bg=None, fg=None, bold=False):
        self.text = text
        self.bg = bg
        self.fg = fg
        self.bold = bold

    def __repr__(self):
        return f"Text('{self.text}', bg={self.bg}, fg={self.fg}, bold={self.bold})"

    def __eq__(self, obj):
        if isinstance(obj, Text):
            return self.text == obj.text and self.bg == obj.bg and self.fg == obj.fg and self.bold == obj.bold
        return False

class ParseError(Exception):
    pass

def parsePlain(c, t, ts):
    if c == '\x1b':
        if t.text: 
            ts.append(t)
        return Text(bg=t.bg, fg=t.fg, bold=t.bold), parseESC
    t.text += c
    return t, parsePlain

def parseESC(c, t, ts):
    if c == '[':
        return t, parseCSI()
    raise ParseError

class parseCSI:
    def __init__(self):
        self.code = ''

    def __call__(self, c, t, ts):
        if c == 'm':
            for code in self.code.split(';'):
                c = int(code)
                if c == 0:
                    t.fg = None
                    t.bg = None
                    t.bold = False
                if c == 1:
                    t.bold = True
                elif 30 <= c and c <= 37:
                    t.fg = simplecolor[c - 30]
                elif 40 <= c and c <= 47:
                    t.bg = simplecolor[c - 40]
            return t, parsePlain
        else:
            self.code += c
            return t, self

simplecolor = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
]
