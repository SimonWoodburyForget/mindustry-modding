""" Simple parser for org tables. 

Specifically the org file must be sectioned,
and any text between tables will be ignored.
There must be one or two tables per section,
one for new definitions and the other for 
defaults/resetting of previous definitions.

```org

Comment on document.

* DataType

Comment on type.

| field | value |
|-------|-------|
| ohno  | 0     |
| ohyes | 1     |

Comment on secondairy table?

| field | value |
|-------|-------|
| ohoh  | 11    |

Footer comment???

* AnotherType

No data here for some reason.
```

"""

from parsy import generate, regex, string

whitespace = regex(r" *")
newline = regex("\n *").optional()
lexeme = lambda p: p << whitespace
pipe = lexeme(string("|"))
name = lexeme(regex(r"[^\n\|\*]"))
row = whitespace >> pipe >> lexeme((name.many().concat() << pipe)).many()
rows = (newline >> row).many()

sect = regex("\** ") >> (name.many().concat() << string("\n").optional() )
text = (name.many().concat() << string("\n")).many()

def to_table():
    """ Takes an array of arrays (table) and turns it into a more useful dictionary, 
    relative to column names (the first row), skipping any separator.  """


@generate
def org_table():
    """ Parses a section with two tables. """
    yield text
    section = yield sect
    yield text
    data = yield rows
    yield text
    data2 = yield rows
    yield text
    return section, { "definitions": data, "defaults": data2 }


print(org_table.many().map(dict).parse("""

text text

*** Turret


  | name |
  | namo |

text
text

    | name |

text


** Melter

  | tab |

*** Router

  | name |
  | not name |

"""))




if __name__ == "__main__":
    table = rows.parse("""
    | name | name | name |
    | nomo | neom | tohn |
    | e name |""")

    assert table == [["name", "name", "name"], ["nomo", "neom", "tohn"],["ename"]]


    org = """
    * Section

    text

    text 

    | table | one |
    |-------|-----|
    | a     | 12  |

    ** Section 2

    text 

    text

    | table | two |
    |-------|-----|
    | b     | 12  |
    """


    
