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

def decompose(args):
    '''(((a, b), c), d) => [a, b, c, d]'''
    if type(args) in (tuple, list) and len(args) > 1:
        a, b = args
        return decompose(a) + [b]
    else:
        return [args]

def decomposed(fn):
    '''Decorates decompose on fn.'''
    return lambda x: fn(*decompose(x))

Var = namedtuple("Var", "name")
Type = namedtuple("Type", "name pairs")

def statement(keyword):
    '''Parses a statement.'''
    return lexeme(string(keyword)) >> name

Method = namedtuple("Method", "mods rtype name params body")
Variable = namedtuple("Variable", "mods vtype name value")
Instance = namedtuple("Instance", "name args body")

@dataclass
class Class:
    '''The definition of a class.'''

    '''The modifiers of said class, like `public`.'''
    mods: [str]

    '''The name of the class.'''
    name: str

    '''The name of an implemented trait.'''
    impl: str

    '''The body of the class, with all 
    the variable/method definitions.'''
    body: []

@dataclass
class VariableDefinition:
    '''The initial definition of a variable, with type information.'''

    '''The modifier of said variable, like `static`.'''
    mods: [str]
    
    '''The type of this specific definition.'''
    vtype: str

    '''The list of variable names and values defined.'''
    variables: []

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

@generate
def literal():
    integer = lexeme(concat(many1(regex(r"-?[0-9]")))).parsecmap(lambda x: int(x))
    floating = lexeme(concat(regex(r"-?[0-9]+\.?[0-9]*f"))).parsecmap(lambda x: float(x[:-1]))
    true = lexeme(string("true")).result(True)
    false = lexeme(string("false")).result(False)
    quoted = lexeme(string('"') >> concat(many(none_of('"'))) << string('"'))
    boolean = lexeme(true | false)
    x = yield floating | integer | boolean | quoted
    return x

equals = lexeme(string('='))
comma = lexeme(string(','))
lpar = lexeme(string('('))
rpar = lexeme(string(')'))

# @generate
# def instanciation():
#     x = yield lexeme(string('new')) >> name + args
#     b = yield optional(anon_block)
#     return Instance(*(x for x in chain(x, [b])))

value = literal | name.parsecmap(Var) 
args = lpar >> sepBy(value, comma) << rpar

term = lexeme(string(";"))
llblace = lexeme(string("{{"))
rrblace = lexeme(string("}}"))
lbrace = lexeme(string("{"))
rbrace = lexeme(string("}"))

modifier = lexeme(string("public") | string("protected") | string("private")
                  | string("abstract") | string("default") | string("static")
                  | string("final") | string("transient") | string("volatile")
                  | string("synchronized") | string("native") | string("strictfp"))
modifiers = many(modifier)

class_name = statement("class")
impls_name = statement("implements")
new_name = statement("new")

instance = (new_name
            + (lpar
               >> sepBy(name | value, comma)
               << rpar))

variable = (modifiers
            + name
            + sepBy(name + optional(equals >> value), comma)
            << term).parsecmap(decomposed(VariableDefinition))

params = lpar >> sepBy(name + name, comma) << rpar
method = (modifiers
          + name
          + name
          + params
          + (lbrace
             >> many(variable)
             << rbrace)).parsecmap(decomposed(Method))

class_body = (lbrace
              >> many(variable ^ method)
              << rbrace)

java_class = whitespace >> (modifiers
                            + class_name
                            + impls_name
                            + class_body).parsecmap(decomposed(Class))

# lblock = lexeme(string("{"))
# rblock = lexeme(string("}"))
# block = lblock >> sepEndBy(block_parsers, ";") << rblock
