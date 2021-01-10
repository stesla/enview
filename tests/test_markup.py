from enview.markup import parse, Text

def test_parse_empty():
    assert parse('') == []

def test_parse_plain():
    assert parse('plaintext') == [Text('plaintext')]

def test_parse_low_colors():
    assert parse('some\x1b[36;44mcolor') == [Text('some'), Text('color', bg='#000080', fg='#008080')]

def test_parse_low_colors():
    assert parse('some\x1b[96;104mcolor') == [Text('some'), Text('color', bg='#0000ff', fg='#00ffff')]

def test_parse_256_low():
    assert parse('\x1b[38;5;1;48;5;2mword') == [Text('word', bg='#008000', fg='#800000')]

def test_parse_256_high():
    assert parse('\x1b[38;5;8;48;5;9mword') == [Text('word', bg='#ff0000', fg='#808080')]

def test_parse_color_cube():
    assert parse('\x1b[38;5;16mword') == [Text('word', fg='#000000')]
    assert parse('\x1b[38;5;42mword') == [Text('word', fg='#00d787')]

def test_parse_grayscale():
    assert parse('\x1b[38;5;243mword') == [Text('word', fg='#767676')]

def test_parse_reset():
    assert parse('foo\x1b[31mbar\x1b[0mbaz') == [Text('foo'), Text('bar', fg='#800000'), Text('baz')]

def test_parse_bold():
    assert parse('\x1b[1mfoo') == [Text('foo', bold=True)]

def test_parse_multiple_sequences():
    assert parse('\x1b[1m\x1b[33mfoo') == [Text('foo', bold=True, fg='#808000')]

def test_html_plain():
    assert Text('foo').to_html() == 'foo'

def test_html_all_attributes():
    assert Text('foo', bg='#808000', fg='#800000', bold=True).to_html() == \
            '<span style="background-color: #808000; color: #800000; font-weight: bold">foo</span>'

def test_html_escaped():
    assert Text('<title>').to_html() == '&lt;title&gt;'
