#from sys import
from structs import *

builtins = {}
def bf(name, signature):
    builtins[name] = Func(name, BltnFunc(name, signature))

builtins['str'] = Type() #TBD

bf('print', lambda *x:x[0])
