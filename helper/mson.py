""" Parser for Mindustry JSON. 

This parser may be more forgiving then 
the actual Mindustry parser itself, so
to make parsing other mods possible.
"""

from parsy import generate, regex, string

whitespace = regex(r'\s*')
lexeme = lambda p: p << whitespace
lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('['))
rbrack = lexeme(string(']'))
colon  = lexeme(string(':'))
comma  = lexeme(string(',')).optional() # commas is optional
true   = lexeme(string('true')).result(True)
false  = lexeme(string('false')).result(False)
null   = lexeme(string('null')).result(None)
number = lexeme(
    regex(r'-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?')
).map(float)
string_part = regex(r'[^"\\]+')
string_esc = string('\\') >> (
    string('\\')
    | string('/')
    | string('"')
    | string('b').result('\b')
    | string('f').result('\f')
    | string('n').result('\n')
    | string('r').result('\r')
    | string('t').result('\t')
    | regex(r'u[0-9a-fA-F]{4}').map(lambda s: chr(int(s[1:], 16)))
)
quoted = lexeme(string('"') >>
                (string_part | string_esc).many().concat()
                << string('"'))
unquoted = lexeme(( regex(r"[a-zA-Z-]")).many().concat()
                  << regex("[ -,\s\t\n\r]")) # no idea, but it works

# Circular dependency between array and value means we use `generate` form here
@generate
def array():
    yield lbrack
    elements = yield value.sep_by(comma)
    yield comma.optional()
    yield rbrack
    return elements


@generate
def object_pair():
    key = yield quoted | unquoted
    yield colon
    val = yield value
    yield comma.optional()
    return (key, val)


json_object = lbrace >> object_pair.sep_by(comma).map(dict) << rbrace
value = quoted | number | json_object | array | true | false | null | unquoted
json = whitespace >> value

TEST = """
{
	"name": "Silver Crags",
	"description": "Salt and silver lie here.",
	"loadout": "basicFoundation",
    "startingItems": [
    	{"item": "copper", "amount": 200},
    	{"item": "lead", "amount": 300},
    ],
    "conditionWave": 10,
    "launchPeriod": 10
    "brequirements": [
    	{ type : ZoneWave
    		zone": groundZero

"wave": 40,
    	}
    	{
    		"type": Unlock"
block": "kiln"
    	},
    	{
    		"type": "Unlock",
    		"block": "solar-panel"
    	}
    ],
    "resources": ["copper", "silver", "lead", "coal", "sand"]
}

"""

if __name__ == '__main__':
    print(json.parse(TEST))
    
