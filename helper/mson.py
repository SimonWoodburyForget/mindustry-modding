""" Parser for Mindustry JSON. (uses parsec.py)

The specific implimentation changes to JSON goes as follows:
- `//` maybe used for single line comments;
- `"` quotes aren't required for strings;
- `,` commas aren't required for arrays or objects.

This parser doesn't actually currently work as it should.
"""

from parsec import *

@generate
def comment():
    yield optional(many(one_of(" \n\t\r")))
    yield string("//")
    comment = yield regex(".*")
    yield string("\n")
    return comment

rs = regex(r'\s*')
cm = many(comment)
whitespace =  rs << cm

lexeme = lambda p: p << whitespace

lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('['))
rbrack = lexeme(string(']'))
colon = lexeme(string(':'))
comma = lexeme(one_of(','))
true = lexeme(string('true')).result(True)
false = lexeme(string('false')).result(False)
null = lexeme(string('null')).result(None)


def number():
    '''Parse number.'''
    return lexeme(
        regex(r'-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?')
    ).parsecmap(float)

def charseq():
    '''Parse string. (normal string and escaped string)'''
    def string_part():
        '''Parse normal string.'''
        return regex(r'[^"\\]+')

    def string_esc():
        '''Parse escaped string.'''
        return string('\\') >> (
            string('\\')
            | string('/')
            | string('"')
            | string('b').result('\b')
            | string('f').result('\f')
            | string('n').result('\n')
            | string('r').result('\r')
            | string('t').result('\t')
            | regex(r'u[0-9a-fA-F]{4}').parsecmap(lambda s: chr(int(s[1:], 16)))
        )
    return string_part() | string_esc()

@lexeme
@generate
def quoted():
    '''Parse quoted string.'''
    yield string('"')
    body = yield many(charseq())
    yield string('"')
    return ''.join(body)

@generate
def unquoted():
    '''Parse unquoted string.'''
    body = yield many1(regex(r"[a-zA-Z- ]"))
    return ''.join(body).strip()

@generate
def unquotedvalue():
    '''Parse unquoted string specifically for values.'''
    body = yield many(regex(r"."))
    return ''.join(body).strip()

@generate
def array():
    '''Parse array element in JSON text.'''
    yield lbrack
    elements = yield sepEndBy(value | unquoted, one_of(",\n") << whitespace)
    yield rbrack
    return elements

@generate
def object_pair():
    '''Parse object pair in JSON.'''
    key = yield quoted | unquoted
    yield colon
    val = yield value | unquoted | unquotedvalue
    return (key, val)

@generate
def json_object():
    '''Parse JSON object.'''
    yield lbrace
    pairs = yield sepBy(object_pair, comma | whitespace)
    yield rbrace
    return dict(pairs)

value = quoted | number() | json_object | array | true | false | null
jsonc = whitespace >> json_object

def load(text):
    return jsonc.parse(text)

if __name__ == '__main__':
    assert array.parse('''[ "value" ]''') == [ 'value' ]
    assert array.parse('''[ value ]''') == [ 'value' ]
    assert array.parse('''[ value
                            value ]''') == [ 'value' ] * 2
    assert array.parse('''[ value
                            value
                            value ]''') == [ 'value' ] * 3
    assert array.parse('''[ value
                            value   ,
                            value
                            "" ]''') == ([ 'value' ] * 3) + ['']
    # assert array.parse('''[ value // comment
    #                         value
    #                         value
    #                         "" ]''') == ([ 'value' ] * 3) + ['']


    
    assert jsonc.parse(""" 
// comment 1
// comment 2
{}
// comment 3
""") == {}
    assert jsonc.parse('{"test" : "json"  }') == {'test': 'json'}
    assert jsonc.parse('{"test" :  json  }') == {'test': 'json'}
    assert jsonc.parse('{ test  : "json" }') == {'test': 'json'}
    assert jsonc.parse('{ test  :  json  }') == {'test': 'json'}
    assert jsonc.parse('''{ test: json,
                           tist : jons }''') == {'test': 'json', 'tist': 'jons'}
    assert jsonc.parse('''{test :json 
                           tist : jons}''') == {'test': 'json', 'tist': 'jons'}
    assert jsonc.parse('{} //comment') == {}
    assert jsonc.parse('''{ test : json 
                           tist : jons } //comment''') == {'test': 'json', 'tist': 'jons'}
    assert jsonc.parse('''{ test : jsona //
                           tist : jons }''') == {'test': 'jsona', 'tist': 'jons'}
    assert jsonc.parse('''{ test : jsonb // comment
                           tist : jons }''')
    assert jsonc.parse('''{ test : jsonc 
// comment
                           tist : jons }''') == {'test': 'jsonc', 'tist': 'jons'}

    assert jsonc.parse('''{ test : json 
// comment 
      // comment
                           tist : jons }''') == {'test': 'json', 'tist': 'jons'}

    assert jsonc.parse('''{ test : "js//on" }''') == {'test': 'js//on' }
    assert jsonc.parse('''{ test : "js//on", }''') == {'test': 'js//on' }
    # print(jsonc.parse('''{ test : http:ohnocom }''') ) # you're insane right? this will not work.
    assert jsonc.parse('''{ test : js on, }''') == {'test': 'js on' }
    assert jsonc.parse('''{ test : js on }''') == {'test': 'js on' }
    # print(jsonc.parse('''{ test : json
    #                         testthing : testtest }''')) # TODO: this doesn't work either
    assert jsonc.parse('''{ a: [ "test" ] }''') == { 'a': [ 'test' ] } 

    # TODO: well that doesn't work.
    # assert jsonc.parse('''{ a: [  test ] }''') == { 'a': [ 'test' ] } 
    # assert jsonc.parse('''{ a: [  test, test  ] }''') == { 'a': [ 'test' ] }
