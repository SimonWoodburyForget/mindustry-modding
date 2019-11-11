''' Minimalistic Java parser to extract some data from Mindustry,
with the specialized interest of producing JSON API documentation.

parsec.py is used to do the parsing work.'''

from parsec import (generate, regex, string, many,
                    many1, optional, sepBy, ParseError,
                    sepEndBy, none_of)
from itertools import chain
from collections import namedtuple
from dataclasses import dataclass
from functools import reduce

# [{}, {}, {}] => {}
dicts = lambda x: reduce(lambda a, b: { **a, **b }, x)

Instance = namedtuple("Instance", "name params body")
Method = namedtuple("Method", "name")
Var = namedtuple("Var", "name")
Type = namedtuple("Type", "name pairs")

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
floating = lexeme(concat(regex(r"-?[0-9]+\.?[0-9]*f"))).parsecmap(lambda x: float(x[:-1]))
true = lexeme(string("true")).result(True)
false = lexeme(string("false")).result(False)
quoted = lexeme(string('"') >> concat(many(none_of('"'))) << string('"'))
boolean = lexeme(true | false)
literal = floating | integer | boolean | quoted

equals = lexeme(string('='))
comma = lexeme(string(','))
lpar = lexeme(string('('))
rpar = lexeme(string(')'))

@generate
def assignment():
    ''' 
    "x = 2, y = 5" => {'x': 2, 'y': 5} 
    '''
    kv_pairs = yield sepBy((name << equals) + value, comma)
    return dict(kv_pairs)

# "int x = 2, y = 3" => Type("int", {'x': 2, 'y': 3})
hinted_assignment = (name + assignment).parsecmap(lambda x: Type(*x))

@generate
def instanciation():
    x = yield lexeme(string('new')) >> name + params
    b = yield optional(anon_block)
    return Instance(*(x for x in chain(x, [b])))

value = literal | instanciation | name.parsecmap(Var)
params = lpar >> sepBy(value, comma) << rpar

term = lexeme(string(";"))
llblock = lexeme(string("{{"))
rrblock = lexeme(string("}}"))
block = sepEndBy(assignment, term).parsecmap(dicts)
anon_block = llblock >> block << rrblock




# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepEndBy(block_parsers, ";") << rblock
