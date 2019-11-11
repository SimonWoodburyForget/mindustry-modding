import unittest

from mava import *


class TestJava(unittest.TestCase):

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

    def test_abstract_class(self):
        self.assertEqual(abstract_class.parse("abstract class xy"), "xy")
        self.assertEqual(abstract_class.parse("abstract   class  xy  "), "xy")

    def test_class_implements(self):
        self.assertEqual(class_implements.parse("class xy implements yx"), ("xy", "yx"))

    def test_abstract_class_implements(self):
        self.assertEqual(abstract_implements.parse("abstract class xy implements ab"), ("xy", "ab"))

    def test_literal(self):
        self.assertEqual(literal.parse("1"), 1)
        self.assertEqual(literal.parse("-1"), -1)
        self.assertTrue(literal.parse("-1") is not -1.)
        self.assertEqual(literal.parse("-1.1"), -1.1)
        self.assertTrue(literal.parse("true ") is True)
        self.assertTrue(literal.parse("false ") is False)
        self.assertEqual(literal.parse('"string"'), "string")

    def test_assignment(self):
        self.assertEqual(assignment.parse("x=1"), {'x': 1})
        self.assertEqual(assignment.parse("x = 1"), {'x': 1})
        self.assertEqual(assignment.parse('x = "1"'), {'x': '1'})
        self.assertEqual(assignment.parse('x = new Thing()'), {'x': Instance('Thing', [])})

    def test_declaration(self):
        pass
        # self.assertEqual(assignment.parse("int x"), ("int", "x", None))
        
if __name__ == '__main__':
    unittest.main()
