from structs import *

def fields(names):
    if isinstance(names, str): names = names.split()
    def f(cls):
        cls.fields = names
        #cls.__init__ = init
        return cls
    return f

def reprlist(arr, indent):
    indent += 1
    txt = '['
    if len(arr)==0: return txt+']'
    for e in arr:
        txt += '\n'+' '*indent
        if isinstance(e, list): txt += reprlist(e, indent)
        elif isinstance(e, Asty): txt += e.repr(indent)
        else: txt += repr(e)
        txt += ','
    indent -= 1
    return txt[:-1]+'\n'+' '*indent+']'

class Asty:
    def __init__(self, *args):
        for f, a in zip(self.fields, args):
            setattr(self, f, a)

    def repr(self, indent):
        indent += 1
        txt = self.__class__.__qualname__
        for f in self.fields:
            txt += '\n'+' '*indent+f+': '
            v = getattr(self, f)
            if isinstance(v, list): txt += reprlist(v, indent)
            elif isinstance(v, Asty): txt += v.repr(indent)
            else: txt += repr(v)
        return txt
    __repr__ = lambda self: self.repr(0)

class Expr(Asty): pass

class Resolved(Asty):
    def resolve(self, st): return self

#literals

@fields('str')
class String(Expr, Resolved):
    def resolve(self, st):
        self.type = st.builtins['str']
        return self

@fields('name')
class Id(Expr):
    def resolve(self, st): return st[self.name]
    #def resolve_lval(self, st): #when the name is on the left side of an assignment
    #    pass

#operators

@fields('func args')
class FuncCall(Expr):
    def resolve(self, st):
        func = self.func.resolve(st)
        args = [x.resolve(st) for x in self.args]
        if isinstance(func, Func):
            return Call(func.select([x.type for x in args]), args)
        else: raise TypeError('todo: funccalling '+type(func).__name__)

@fields('this attr')
class Dot(Expr):
    def resolve(self, st):
        this = self.this.resolve(st)
        if isinstance(self.attr, Id):
            if self.attr.name in this.type.fields:
                return Attr(this, self.attr.name)
            else: return FuncCall(self.attr, [self.this]).resolve(st)
        elif isinstance(self.attr, FuncCall):
            self.attr.args[0:0] = [self.this]
            return self.attr.resolve(st)
        else: raise TypeError('what kind of dotting is this')

#statements

@fields('name args body')
class FuncDef(Asty): pass

#resolved code

@fields('this attr')
class Attr(Resolved): pass

@fields('func args') #func is Func1, not Func
class Call(Resolved): pass
