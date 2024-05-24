import unittest
import os
from glob import glob

from logfacil.log import Controller
from logfacil import setup

class Foo:

    def __init__(self):
        self.atributo1 = 2
        self.atributo2 = type(int)

    def metodo1(self, x):
        return x+2
    
    def metodo2(self, x):
        return x+1

class testeController(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(testeController, self).__init__(*args, **kwargs)

    def test_filter_methods(self):
        controler = Controller()
        foo = Foo()
        controler.__list_methods__(foo)
        methods = controler.cache[id(foo)]
        assert len(methods) == 2
        assert methods.get('metodo1') == foo.metodo1
        assert methods.get('metodo2') == foo.metodo2
    
    def teste_ignore_methods(self):
        controler = Controller()
        foo = Foo()
        controler.__list_methods__(foo)
        methods = controler.cache.get(id(foo))
        assert len(methods) == 2
        
        # ignoring metodo1
        controler.ignore(foo, 'metodo1')
        methods = controler.cache.get(id(foo))
        assert len(methods) == 1
        assert hasattr(foo.metodo1, '__wrapped__') == False
        assert methods.get('metodo2') == foo.metodo2

class testeControllerIntegracao(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(testeControllerIntegracao, self).__init__(*args, **kwargs)
        self.foo = Foo()
        self.controler = Controller()
        self.handlers = setup.init()
        self.log_path = glob('logs/*')[0]

    def loglen(self):
        with open(self.log_path) as reader:
            return len(reader.read())

    def clean_logs(self):
        setup.close_all(self.handlers)
        os.remove(self.log_path)
        os.rmdir('logs')

    def test_enable_disable_logs(self):
        
        self.foo.metodo1(15)
        assert self.loglen() == 0

        # enable logs
        self.controler.enable_logs(self.foo)
        self.foo.metodo1(10)
        assert self.loglen() > 0
        self.clean_logs()

        # disable logs
        self.controler.disable_logs(self.foo)
        self.handlers = setup.init()
        self.foo.metodo1(10)
        assert self.loglen() == 0
        self.clean_logs()

if __name__ == '__main__':
    unittest.main()