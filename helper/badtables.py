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
 
from pprint import pprint
import yaml


from parsy import generate, regex, string

whitespace = regex(r" *")
newline = regex("\n *").optional()
lexeme = lambda p: p
pipe = lexeme(string("|"))
name = lexeme(regex(r"[^\n\|\*]")).many().concat()
row = whitespace >> pipe >> lexeme((name.map(lambda x: x.strip())
                                    << pipe)).many()
rows = (newline >> row).many()

sect = regex("\** ") >> (name << string("\n").optional() )
text = (name << string("\n")).many()

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


def load(data):
    # TODO: fix lists within sections to make this useful?
    """ Takes an array of arrays (table) and 
    turns it into a more useful dictionary, 
    relative to column names (the first row), 
    skipping any separator, and org args such
    as `<10>` or `<r>` or `<r10>`.

    This simply assumes the table is properly
    and fully formatted:

    ```
    | name |
    |------|
    | <r>  |
    | name |
    ```

    We'll also just assume the first row are
    the column names.
    """

    def exclude(row):
        excludes = ["----", "<r>", "<l>", "<r10>", "<l10>", "<10>" ]
        chars = "".join(row)
        return not any(x in chars for x in excludes)

    def makecell(row):
        try:
            t = row["type"]
        except KeyError as e:
            print("not here", row)
            return row
        d = row["default"]
        if d == "":
            row["default"] = None
        elif t == "float":
            row["default"] = float(d) 
        elif t == "int":
            row["default"] = int(d) 
        elif t == "boolean":
            row["default"] = bool(d) 
        return row

    def makerows(tbl):
        """ Turns table from an array of array, into a dict. """
        # header = next(rows)
        # return { header[i]: cell for cell in row
        #          for row in rows }
        rows = list(row for row in tbl if exclude(row))
        try:
            header = rows[0]
            rows = rows[1:]
        except IndexError:
            # invalid rows or no data
            return None
        return [ makecell({ header[i]: c for i, c in enumerate(row, 0) })
                 for row in rows ]

    parsed = org_table.many().map(dict).parse(data)
    # removing... rows?
    # return { section: [ [ row for row in table ]
    #                     for table in tables ]
    #          for section, tables in parsed.items() }
    return { sec: { name: makerows(tbl)
                    for name, tbl in tbls.items() }
             for sec, tbls in parsed.items() }

test = """

text text

*** Turret


  | name | namo | namy |
  | <r>   |      |      |
  | namo |      | nome |

text
text

    | name |
    |------|

text


** Melter

  | tab |

*** Router

  | name |
  | not name |

"""

assert load(test)


real_test = """
** Item

   Extends [[Content][Content]] -- It's the object that can ride conveyors, sorters and be stored in containers, and is commonly used in crafters.

   | field          | type     | default | notes      |
   |----------------+----------+---------+------------|
   |                |          |         | <10>       |
   | color          | [[Color][Color]]    |         | hex string of color |
   | type           | [[Item][ItemType]] |         | resource or material; used for tabs and core acceptance |
   | explosiveness  | float    | 0     | how explosive this item is. |
   | flammability   | float    | 0     | flammability above 0.3 makes this eleigible for item burners. |
   | radioactivity  | float    |         | how radioactive this item is. 0=none, 1=chernobyl ground zero |
   | hardness       | int      | 0     | drill hardness of the item |
   | cost           | float    | 1     | used for calculating place times; 1 cost = 1 tick added to build time |
   | alwaysUnlocked | boolean  | false | If true, item is always unlocked. |

"""

pprint(load(real_test))
print(yaml.dump(load(real_test), Dumper=yaml.Dumper, default_flow_style=False))

if __name__ == "__main__":
    table = rows.parse("""
    | name | name | name |
    | nomo | neom | tohn |
    | e name |""")

    assert table == [["name", "name", "name"], ["nomo", "neom", "tohn"],["e name"]]


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


    
