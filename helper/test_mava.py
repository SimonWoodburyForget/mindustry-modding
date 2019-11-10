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
        self.assertTrue(literal.parse("true"))
        self.assertTrue(not literal.parse("false"))
        self.assertEqual(literal.parse('"string"'), "string")
    
if __name__ == '__main__':
    unittest.main()
