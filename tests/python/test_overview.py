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
        self.assertEqual(self.overview['ExampleClass']['functions']['foo']['start'], 5)
        self.assertEqual(self.overview['ExampleClass']['functions']['special']['start'], 11)

    def test_class_overview_method_end(self):
        self.assertEqual(self.overview['ExampleClass']['functions']['foo']['end'], 7)
        self.assertEqual(self.overview['ExampleClass']['functions']['special']['end'], 16)

    def test_class_has_start(self):
        self.assertEqual(self.overview['ExampleClass']['start'], 4)

    def test_class_has_end(self):
        self.assertEqual(self.overview['ExampleClass']['end'], 16)

    def test_match_methods(self):
        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'foo'), [5])
        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'special'), [11])

        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'nothere'), [])
        self.assertEquals(self.overview_class.match_methods('Foo', 'nothere'), [])

    def test_has_method_takes_regex_pattern(self):
        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'f*'), [11, 8, 5])
        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'spec.al'), [11])
        self.assertEquals(self.overview_class.match_methods('ExampleClass', 'spec.alzed'), [])

    def test_class_and_method_names(self):
        self.assertEquals(self.overview_class.class_and_method_names(9), ('ExampleClass', 'bar'))
        self.assertEquals(self.overview_class.class_and_method_names(8), ('ExampleClass', 'bar'))
        self.assertEquals(self.overview_class.class_and_method_names(10), ('ExampleClass', 'bar'))
        self.assertEquals(self.overview_class.class_and_method_names(13), ('ExampleClass', 'special'))

        self.assertEquals(self.overview_class.class_and_method_names(2), (None, 'first'))
        self.assertEquals(self.overview_class.class_and_method_names(18), (None, 'zed'))

    #def test_the_whole_thing(self):
    #    from pprint import pprint
    #    pprint(self.overview_class.class_overview())
    #    self.assertTrue(False)
