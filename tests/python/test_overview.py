import unittest
import python.overview

class Class_overviewTest(unittest.TestCase):
    def setUp(self):
        self.overview = python.overview.class_overview('/home/matty/.vim/bundle/python/tests/data/example_class.py')
        pass

    def test_class_overview_has_class_name(self):
        self.assertTrue('ExampleClass' in self.overview)

    def test_class_overview_has_funcation_name(self):
        self.assertTrue('zed' in self.overview)

    def test_class_overview_doesnt_have_methods(self):
        self.assertFalse('foo' in self.overview)

    def test_class_overivew_class_list_methods(self):
        self.assertTrue('foo' in self.overview['ExampleClass']['functions'])

    def test_class_overivew_class_list_methods(self):
        self.assertTrue('special' in self.overview['ExampleClass']['functions'])

    def test_class_overview_method_start(self):
        self.assertEqual(self.overview['ExampleClass']['functions']['foo'], 2)
        self.assertEqual(self.overview['ExampleClass']['functions']['special'], 8)

    def test_class_has_start(self):
        self.assertEqual(self.overview['ExampleClass']['line'], 1)

    def test_class_has_end(self):
        self.assertEqual(self.overview['ExampleClass']['end'], 13)


