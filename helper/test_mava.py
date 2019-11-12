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
        
    def test_instanciation(self):
        def test_eq(a, b):
            self.assertEqual(instance.parse(a), b)

        test_eq('new Thing()', Instance('Thing', [], None))
        test_eq('new Thing(2)', Instance('Thing', [2], None))
        test_eq('new Thing(x)', Instance('Thing', [Variable('x')], None))
        test_eq('new Thing("x-n")', Instance('Thing', ['x-n'], None))

    def test_params(self):
        self.assertEqual(params.parse('''(int x, float y)'''),
                         [("int", "x"), ("float", "y")])

    def test_class_method(self):
        def test_eq(a, b):
            self.assertEqual(method.parse(a), b)
        test_eq('public int mymy(int x, float y){}',
                Method({"public"},
                       "int",
                       "mymy",
                       [("int", "x"),
                        ("float", "y")],
                       []))

        test_eq('public int mymy(int x, float y){ int x = 1; }',
                Method({"public"},
                       "int",
                       "mymy",
                       [("int", "x"),
                        ("float", "y")],
                       [
                           VariableDefinition(set(), 'int', [('x', 1)])
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
        test_eq('{ void meth(){} }', [ Method(set(), 'void', 'meth', [], []) ])
        
        test_eq('{ static int x; }', [ VariableDefinition({'static'},
                                                          'int',
                                                          [('x', None)]) ])
        
        test_eq('{ static int x, y; }', [
            VariableDefinition({'static'},
                               'int',
                               [('x', None),
                                ('y', None)])
        ])

        test_eq('{ static int x, y; void meth(){} }', [
                VariableDefinition({'static'},
                                   'int',
                                   [('x', None),
                                    ('y', None)]),
                Method(set(), 'void', 'meth', [], [])
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
