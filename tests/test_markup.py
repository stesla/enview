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
