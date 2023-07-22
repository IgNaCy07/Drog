def compile(st, **opts):
    compiler = PyCompiler(**opts) #object-oriented garbage cuz why not
    return '\n'.join(compiler.compile(st))

class PyCompiler:
    def __init__(self, **opts):
        pass
    def compile(self, st):
        code = []
        self.st = st #manipped
        for stmt in st.code:
            s = self.dispatch(stmt)
            print(s)
            code.append(s)
        return code
    def dispatch(self, stmt):
        f = getattr(self, 'compile'+type(stmt).__name__)
        s = f(stmt)
        return s
    def compileBltnFunc(self, stmt):
        return '__drog_builtins__.'+stmt.name
    def compileCall(self, stmt):
        print(stmt)
        f1 = stmt.func
        args = stmt.args
        return self.dispatch(f1)+'(' \
               +','.join(self.dispatch(a) for a in args)+')'
    def compileString(self, stmt):
        return repr(stmt.str)
