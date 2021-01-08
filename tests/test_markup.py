from enview.markup import parse, Text

def test_parse_empty():
    assert parse('') == []

def test_parse_plain():
    assert parse('plaintext') == [Text('plaintext')]

def test_parse_simplecolors():
    assert parse('some\x1b[36;44mcolor') == [Text('some'), Text('color', bg='blue', fg='cyan')]

def test_parse_reset():
    assert parse('foo\x1b[31mbar\x1b[0mbaz') == [Text('foo'), Text('bar', fg='red'), Text('baz')]

def test_parse_bold():
    assert parse('\x1b[1mfoo') == [Text('foo', bold=True)]

def test_parse_multiple_sequences():
    assert parse('\x1b[1m\x1b[33mfoo') == [Text('foo', bold=True, fg='yellow')]

def test_html_plain():
    assert Text('foo').to_html() == 'foo'

def test_html_all_attributes():
    assert Text('foo', bg='yellow', fg='red', bold=True).to_html() == \
            '<span style="background-color: yellow; color: red; font-weight: bold">foo</span>'
