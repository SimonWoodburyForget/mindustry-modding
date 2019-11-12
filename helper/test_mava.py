import unittest

from mava import *


class TestJava(unittest.TestCase):

    def test_decompose(self):
        self.assertEqual(decompose((((1, 2), 3), 4)), [1, 2, 3, 4])

    def test_name(self):
        self.assertEqual(name.parse("abc "), "abc")
        self.assertEqual(name.parse("Abc "), "Abc")
        self.assertEqual(name.parse("Abc12 "), "Abc12")
        self.assertEqual(name.parse("a"), "a")
        self.assertEqual(name.parse("a1"), "a1")
        with self.assertRaises(ParseError):
            name.parse("1Abc")

    def test_class_name(self):
        self.assertEqual(class_name.parse("class xy"), "xy")
        self.assertEqual(class_name.parse("class   xy  "), "xy")

    def test_literal(self):
        self.assertEqual(literal.parse("1"), 1)
        self.assertTrue(type(literal.parse("-1")) is int)
        self.assertEqual(literal.parse("-1.1f"), -1.1)
        self.assertTrue(type(literal.parse("-1f")) is float)
        self.assertTrue(literal.parse("true ") is True)
        self.assertTrue(literal.parse("false ") is False)
        self.assertEqual(literal.parse('"string"'), "string")

    def test_assignment(self):
        self.assertEqual(assignment.parse("x=1"), {'x': 1})
        self.assertEqual(assignment.parse("x = 1"), {'x': 1})
        self.assertEqual(assignment.parse('x = "1"'), {'x': '1'})
        self.assertEqual(assignment.parse('x = new Thing()'), {'x': Instance('Thing', [], None)})
        self.assertEqual(assignment.parse('x = 1, y = 2'), {'x': 1, 'y': 2})

    def test_hinted_assign(self):
        self.assertEqual(hinted_assignment.parse("int x = 1"), Type('int', {'x': 1}))
        self.assertEqual(hinted_assignment.parse("int x"), Type('int', {'x': None}))
        
    def test_instanciation(self):
        self.assertEqual(instanciation.parse('new Thing()'), Instance('Thing', [], None))
        self.assertEqual(instanciation.parse('new Thing(2)'), Instance('Thing', [2], None))
        self.assertEqual(instanciation.parse('new Thing(x)'), Instance('Thing', [Var('x')], None))
        self.assertEqual(instanciation.parse('new Thing("x-n")'), Instance('Thing', ['x-n'], None))
        
    def test_args(self):
        self.assertEqual(args.parse('(1, 3, 4)'), [1, 3, 4], None)
        self.assertEqual(args.parse('(x, u)'), [Var('x'), Var('u')], None)
        self.assertEqual(args.parse('("x", "u")'), ['x', 'u'], None)

    def test_code_block(self):
        self.assertEqual(code_block.parse('{ x = 2; y = 5; z = "thing" }'),
                         { 'x': 2, 'y': 5, 'z': 'thing' })
        
    def test_anon_block(self):
        self.assertEqual(anon_block.parse("{{ x = 1; y=2; }}"), {"x": 1, "y" : 2})

    def test_params(self):
        self.assertEqual(params.parse('''(int x, float y)'''),
                         [("int", "x"), ("float", "y")])

    def test_class_method(self):
        def test_eq(a, b):
            self.assertEqual(method.parse(a), b)
        test_eq('public int mymy(int x, float y){}',
                Method(["public"],
                       "int",
                       "mymy",
                       [("int", "x"),
                        ("float", "y")],
                       []))

        test_eq('public int mymy(int x, float y){ int x = 1; }',
                Method(["public"],
                       "int",
                       "mymy",
                       [("int", "x"),
                        ("float", "y")],
                       [
                           [[], 'int', [('x', 1)]]
                       ]))
        
        # self.assertEqual(class_method.parse('''public int mymy(int x, float y){ x = 1; }'''),
        #                  Method(["public"], "int", "mymy",
        #                         [("int", "x"), ("float", "y")],
        #                         { "x": 1 }))
        # self.assertEqual(class_method.parse('''public int mymy(int x, float y){ 
        # x = new Floor("hotrock"){{ x = 1; }}; }'''),
        #                  Method(["public"], "int", "mymy",
        #                         [("int", "x"), ("float", "y")],
        #                         { "x": Instance("Floor",
        #                                         ["hotrock"],
        #                                         { "x": 1 }) }))
        # self.assertEqual(class_method.parse('''public int mymy(int x, float y){ 
        # x = new Floor("hotrock"){{ x = 1; y = 3; }}; }'''),
        #                  Method(["public"], "int", "mymy",
        #                         [("int", "x"), ("float", "y")],
        #                         { "x": Instance("Floor",
        #                                         ["hotrock"],
        #                                         { "x": 1, 'y': 3 }) }))

    def test_class_body(self):
        def test_eq(a, b):
            self.assertEqual(class_body.parse(a), b)

        # test_eq('{}', [])
        test_eq('{ void meth(){} }', [Method([], 'void', 'meth', [], [])])
        test_eq('{ static int x; }', [[['static'], 'int', [('x', None)]]])
        test_eq('{ static int x, y; }', [[['static'], 'int', [('x', None),
                                                              ('y', None)]]])
        test_eq('{ static int x, y; void meth(){} }',
                [[['static'], 'int', [('x', None),
                                      ('y', None)]],
                 Method([], 'void', 'meth', [], [])
                ])
        
    # def test_class_var_decs(self):
    #     string = """
    #     class Blocks implements ContentList{ 
    #         public Block one, two, three;
    #     }
    #     """
    #     data = Class( [],
    #                   "Blocks",
    #                   "ContentList",
    #                   { "one": Variable(["public"], "Block", "one", None),
    #                     "two": Variable(["public"], "Block", "two", None),
    #                     "three": Variable(["public"], "Block", "three", None)
    #                   })
    #     self.assertEqual(java_class.parse(string), data)


        
        # string = """
        # class Blocks implements ContentList{ 
        #     public Block one, two, three;

        #     @Override
        #     public void load(){
        #         one = new Bullet(1f, 0, "shell"){{ x = 1; }}
        #         two = new Bullet(2f, 0, "nice"){{ y = 2; }}
        #         three = new Bullet(3f, 0, "not-nice"){{ z = 3; }}
        #     }
        # }
        # """


if __name__ == '__main__':
    unittest.main()
