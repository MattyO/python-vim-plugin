import unittest
import python.file_properties

class IndentTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_indents(self):
        indent_array = python.file_properties.get_indents('/home/matty/.vim/bundle/python/tests/data/example_class.py')
        self.assertEqual(indent_array, ['    ', '    ', '  ']) 
