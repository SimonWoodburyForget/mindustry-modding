''' Minimalistic Java parser to extract some data from Mindustry, 
with the specialized interest of producing JSON API documentation. 

parsec.py is used to do the parsing work.'''

from parsec import generate, regex, string, many, many1, optional, sepBy, ParseError
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

# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepBy(keywords, ";") << rblock
