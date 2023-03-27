def fields(names):
    if isinstance(names, str): names = names.split()
    def init(self, *args):
        for n, a in zip(names, args):
            setattr(self, n, a)
    def f(cls):
        cls.__init__ = init
        return cls
    return f

class Asty: pass

#literals

@fields('str')
class String: pass

@fields('name')
class Id: pass

#operators

@fields('this meth')
class Method: pass

#statements

@fields('expr')
class Expr: pass

@fields('name args body')
class Function: pass
