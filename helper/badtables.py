""" Parser for tables. """

from parsy import generate, regex, string

whitespace = regex(r" *")
newline = regex("\n *").optional()
lexeme = lambda p: p << whitespace
pipe = lexeme(string("|"))
name = lexeme(regex(r"[a-zA-Z- ]"))
row = pipe >> lexeme((name.many().concat() << pipe)).many()
rows = (newline >> row).many()


# words = regex(r"[a-zA-Z-]").many().sep_by(" ")
# section = string("* ") >> (name.many().concat() << string("\n"))

# @generate
# def table():
#     sname = yield section
#     yield regex("\n*")
#     data = yield rows
#     yield regex("\n*")
#     return (sname, data)


# print(table.parse("""* Section Name

# | a |



# """))




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


    
