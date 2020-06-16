import unittest
import python.overview

class OverviewTest(unittest.TestCase):
    def setUp(self):
        self.overview_class = python.overview.Overview('/home/matty/.vim/bundle/python/tests/data/example_class.py') 
        self.overview = self.overview_class.class_overview()

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

    def test_has_method(self):
        self.assertTrue(self.overview_class.has_method('ExampleClass', 'foo'))
        self.assertTrue(self.overview_class.has_method('ExampleClass', 'special'))

        self.assertFalse(self.overview_class.has_method('ExampleClass', 'nothere'))
        self.assertFalse(self.overview_class.has_method('Foo', 'nothere'))
        
    def test_has_method_takes_regex_pattern(self):
        self.assertTrue(self.overview_class.has_method('ExampleClass', 'f*'))
        self.assertTrue(self.overview_class.has_method('ExampleClass', 'spec.al'))
        self.assertFalse(self.overview_class.has_method('ExampleClass', 'spec.alzed'))
