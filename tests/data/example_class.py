class ExampleClass(object):
    def foo(self):
        return 'test'

    def bar(self):
        return 'test'

    def special(self):
        def foo():
          return 'test'

        return foo()

