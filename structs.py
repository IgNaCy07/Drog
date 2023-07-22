class Type:
    '''Data type type'''
    def __init__(self, **args):
        self.fields = args.get('fields', {})

class Func:
    '''Function overloading, templating and dispatching'''
    #Overloading plan: overload based on the first arg only
    def __init__(self, name, principal):
        self.name = name #qualified name
        self.principal = principal #principal overload
        self.overloads = {}
    def select(self, argtypes):
        arg = argtypes[0]
        #COOOOOOODE
        return self.principal

class Func1:
    '''A single overload'''
    def __init__(self, name):
        self.name = name

class BltnFunc(Func1):
    '''Built-in function'''
    def __init__(self, name, signature):
        self.name = name
        self.signature = signature
    def __repr__(self): return '[builtin] '+self.name
    def getout(self, *argtypes): return self.signature(*argtypes)

class Symtable:
    '''Holds the symbol table, does all the syntax resolving'''
    def __init__(self, builtins, parent=None):
        self.builtins = builtins
        self.st = {}
        self.code = []
        if parent is None: self.parent = builtins
        else: self.parent = parent
    def proc(self, stmt):
        stmt = stmt.resolve(self)
        print(stmt)
        self.code.append(stmt)
    def sub(self): return Symtable(builtins, self)
    def __getitem__(self, id):
        if id in self.st: return self.st[id]
        else: return self.parent[id]
