import html
import re

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

    def to_html(self):
        escaped = html.escape(self.text)
        styles = []
        if self.bg:
            styles.append(f'background-color: {self.bg}')
        if self.fg:
            styles.append(f'color: {self.fg}')
        if self.bold:
            styles.append('font-weight: bold')
        if not styles:
            return escaped
        else:
            style = '; '.join(styles)
            return f'<span style="{style}">{escaped}</span>'

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

def parse_html(text):
    return ''.join(t.to_html() for t in parse(text))

def parse_text(text):
    return ''.join(t.text for t in parse(text))

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
            codes = self.code.split(';')
            while codes:
                c = int(codes.pop(0))
                if 0 == c:
                    t.fg = None
                    t.bg = None
                    t.bold = False
                elif 1 == c:
                    t.bold = True
                elif 30 <= c and c <= 37:
                    t.fg = LOW[c - 30]
                elif 38 == c and 5 == int(codes.pop(0)):
                    t.fg = color8bit(codes.pop(0)) 
                elif 40 <= c and c <= 47:
                    t.bg = LOW[c - 40]
                elif 48 == c and 5 == int(codes.pop(0)):
                    t.bg = color8bit(codes.pop(0)) 
                elif 90 <= c and c <= 97:
                    t.fg = HIGH[c - 90]
                elif 100 <= c and c <= 107:
                    t.bg = HIGH[c - 100]
            return t, parsePlain
        else:
            self.code += c
            return t, self

LOW = [
    '#303030', # black
    '#800000', # red
    '#008000', # green
    '#808000', # yellow
    '#000080', # blue
    '#800080', # magenta
    '#008080', # cyan
    '#c0c0c0', # white
]

HIGH = [
    '#808080', # black
    '#ff0000', # red
    '#00ff00', # green
    '#ffff00', # yellow
    '#0000ff', # blue
    '#ff00ff', # magenta
    '#00ffff', # cyan
    '#ffffff', # white
]

# i = n - 232
GRAYSCALE = [
        '#080808','#121212','#1c1c1c','#262626','#303030','#3a3a3a',
        '#444444','#4e4e4e','#585858','#626262','#6c6c6c','#767676',
        '#808080','#8a8a8a','#9e9e9e','#9e9e9e','#a8a8a8','#b2b2b2',
        '#bcbcbc','#c6c6c6','#d0d0d0','#dadada','#e4e4e4','#eeeeee',
        ]

CUBE = ['00','5f','87','af','d7','ff']

def color8bit(code):
    n = int(code)
    if 0 <= n and n <= 7:
        return LOW[n]
    elif 8 <= n and n <= 15:
        return HIGH[n - 8]
    elif 16 <= n and n <= 231:
        r = (n - 16) // 36
        g = (n - 16 - 36*r) // 6
        b = n - 16 - 36*r - 6*g
        return '#' + CUBE[r] + CUBE[g] + CUBE[b]
    elif 232 <= n and n <= 255:
        return GRAYSCALE[n - 232]
