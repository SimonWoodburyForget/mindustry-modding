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
dicts = lambda x: reduce(lambda a, b: { **a, **b }, x, {})
concat = lambda p: p.parsecmap(lambda x: "".join(chain.from_iterable(x)))

Var = namedtuple("Var", "name")
Type = namedtuple("Type", "name pairs")

Class = namedtuple("Class", "mods name impls body")
def class_from_raw(raw):
    (((mods, name), impls), body) = raw
    return Class(mods, name, impls, body)
Method = namedtuple("Method", "mods rtype name params body")
Variable = namedtuple("Variable", "mods vtype name value")
Instance = namedtuple("Instance", "name args body")

@generate
def ignore():
    ''' Things we just want to ignore for now. '''
    yield annotation

whitespace = regex(r"\s*") | ignore
lexeme = lambda p: p << whitespace

headchar = regex(r"[a-zA-Z]")
tailchar = regex(r"[a-zA-Z0-9]")
name = lexeme(concat(many1(headchar) + many(tailchar)))

at = string('@')
annotation = lexeme(at >> name)

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
    kv_pairs = yield sepBy(name + optional(equals >> value), comma)
    return dict(kv_pairs)

# "int x = 2, y = 3" => Type("int", {'x': 2, 'y': 3})
hinted_assignment = (name + assignment).parsecmap(lambda x: Type(*x))

@generate
def instanciation():
    x = yield lexeme(string('new')) >> name + args
    b = yield optional(anon_block)
    return Instance(*(x for x in chain(x, [b])))

value = literal | instanciation | name.parsecmap(Var)
args = lpar >> sepBy(value, comma) << rpar

term = lexeme(string(";"))
llblock = lexeme(string("{{"))
rrblock = lexeme(string("}}"))
# 'x = 3; y = 5; z = "thing";' => {'x': 3, 'y': 5, 'z': 'thing'}
block = sepEndBy(assignment, term).parsecmap(dicts)
anon_block = llblock >> block << rrblock

lbrace = lexeme(string("{"))
rbrace = lexeme(string("}"))
code_block = lbrace >> block << rbrace

modifier = lexeme(string("public") | string("protected") | string("private")
                  | string("abstract") | string("default") | string("static")
                  | string("final") | string("transient") | string("volatile")
                  | string("synchronized") | string("native") | string("strictfp"))
modifiers = many(modifier)

class_name = optional(modifiers) + (lexeme(string("class")) >> name)
impls_name = lexeme(string("implements")) >> name

@generate
def vdec():
    ''' Variable Declerations. '''
    mods = yield modifiers
    vtype = yield name
    vnames = yield sepBy(name + optional(equals >> value), comma)
    return { k: Variable(mods, vtype, k, v) for k, v in vnames }

class_assignments = sepEndBy(vdec, term).parsecmap(dicts)
params = lpar >> sepBy(name + name, comma) << rpar
@generate
def class_method():
    mods = yield modifiers
    rtype = yield name
    mname = yield name
    pars = yield params
    body = yield lbrace >> sepEndBy(assignment, term).parsecmap(dicts) << rbrace
    return Method(mods, rtype, mname, pars, body)

class_block = lbrace >> (class_assignments | class_method) << rbrace

java_class = whitespace >> (class_name + impls_name + class_block).parsecmap(class_from_raw)

# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepEndBy(block_parsers, ";") << rblock
