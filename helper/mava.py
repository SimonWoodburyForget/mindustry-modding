''' Minimalistic Java parser to extract some data from Mindustry,
with the specialized interest of producing JSON API documentation.

parsec.py is used to do the parsing work.'''

from parsec import (generate, regex, string, many,
                    many1, optional, sepBy, ParseError,
                    sepEndBy, none_of)
from itertools import chain
from collections import namedtuple

Instance = namedtuple("Instance", "name args")
Method = namedtuple("Method", "name")

concat = lambda p: p.parsecmap(lambda x: "".join(chain.from_iterable(x)))
whitespace = regex(r"\s*")
lexeme = lambda p: p << whitespace

headchar = regex(r"[a-zA-Z]")
tailchar = regex(r"[a-zA-Z0-9]")
name = lexeme(concat(many1(headchar) + many(tailchar)))

class_name = lexeme(string("class")) >> name
abstract_class = lexeme(string("abstract")) >> class_name

implements = lexeme(string("implements"))
class_implements = class_name + (implements >> name)
abstract_implements = abstract_class + (implements >> name)

integer = lexeme(concat(many1(regex(r"-?[0-9]")))).parsecmap(lambda x: int(x))
floating = lexeme(concat(regex(r"-?[0-9]+\.?[0-9]*f?"))).parsecmap(lambda x: float(x))
true = lexeme(string("true")).result(True)
false = lexeme(string("false")).result(False)
quoted = lexeme(string('"') >> concat(many(none_of('"'))) << string('"'))
boolean = lexeme(true | false)
literal = floating | integer | boolean | quoted

equals = lexeme(string('='))
comma = lexeme(string(','))


@generate
def assignment():
    kv_pairs = yield sepBy((name << equals) +
                           (literal | instanciation),
                           comma)
    return dict(kv_pairs)

args = string("(") >> sepBy(literal, comma) << string(")")
instanciation = (lexeme(string('new')) >> name + args).parsecmap(lambda x: Instance(*x))

@generate
def declaration():
    ''' Parses a declaration. 
    ```
    int a;
    int doSomething() {}
    int a, b, c;
    int a = 2, b = 8;
    ```
    '''
    actual = yield (type_of, assignment)

# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepEndBy(block_parsers, ";") << rblock
