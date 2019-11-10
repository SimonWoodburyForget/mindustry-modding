''' Minimalistic Java parser to extract some data from Mindustry, 
with the specialized interest of producing JSON API documentation. 

parsec.py is used to do the parsing work.'''

from parsec import (generate, regex, string, many,
                    many1, optional, sepBy, ParseError,
                    sepEndBy, none_of)
from itertools import chain

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

integer = concat(many1(regex(r"-?[0-9]"))).parsecmap(lambda x: int(x))
floating = concat(regex(r"-?[0-9]+\.?[0-9]*f?")).parsecmap(lambda x: float(x))
true = string("true").result(True)
false = string("false").result(False)
quoted = string('"') >> concat(many(none_of('"'))) << string('"')
boolean = true | false
literal = floating | integer | boolean | quoted

# definition = (name << operator) + literal

# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepEndBy(block_parsers, ";") << rblock
