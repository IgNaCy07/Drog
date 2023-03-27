def todo(descr):
    raise ValueError('todo: '+descr)

#tokenize
chartoks = ':()[]{}.'
class Ungitter:
    def __init__(self,iterable):
        self.iter = iter(iterable)
        self.last = None
        self.dent = True
    def __iter__(self): return self
    def __next__(self):
        if self.last is None:
            c = next(self.iter)
            r = c
        else:
            r = self.last
            self.last = None
        if r == '\n' and not self.dent:
            d = 0
            r = next(self.iter).replace('\t', '    ')
            while r.isspace():
                if r == '\n': d = 0
                else: d += len(r)
            self.dent = d
        return r
    def unget(self, last):
        self.last = last
    def peek(self):
        n = next(self)
        self.unget(n)
        return n
    def pop(self, match):
        n = next(self)
        match = (n==match)
        if not match: self.unget(n)
        return match
def ungitter(it):
    if isinstance(it, Ungitter): return it
    return Ungitter(it)
def tokenize(code):
    code = ungitter(code)
    for c in code:
        if c.islower():
            id = c
            try: c = next(code)
            except:
                yield id
                break
            while c.islower() or c.isdigit():
                id += c
                try: c = next(code)
                except: break
            code.unget(c)
            yield id
        elif c == '"':
            inside = ''
            while True:
                c = next(code)
                if c == '"': break
                elif c == '\\': todo('string escapes')
                else: inside += c
            yield '"'+inside+'"'
        elif c in chartoks: yield c
        elif c.isspace(): continue
        else: todo('character '+c)
    yield 'THE END'

#parsing
from asty import *
def parse(code):
    tokens = Ungitter(tokenize(code))
    dfns = []
    try:
        while True:
            dfns.append(parse_dfn(tokens))
    except StopIteration: pass
    return dfns

def parse_dfn(toks):
    t = next(toks)
    if t == 'type': todo('type definition')
    else: #function
        name = t
        if toks.peek() == '(': args = parse_args(toks)
        else: args = []
        body = parse_block(toks)
        return Function(name, args, body)

def parse_block(toks):
    colon = toks.pop(':')
    if colon: toks.dent = False #will be set to a number
    brace = toks.pop('{')
    assert colon or brace
    #if py-like block, a number (its dent), else False
    dent = colon and not brace and toks.dent
    stmts = []
    cont = True
    while cont:
        stmts.append(parse_stmt(toks))
        if dent: toks.dent = False #call dent-getting
        cont = toks.pop(';') or brace
        if brace and toks.pop('}'): break
        if dent and toks.dent == dent: cont = True #popping should get to a newline, acquiring the dent
    return stmts

def parse_stmt(toks):
    t = next(toks)
    #keyworded stmts
    if False:
        pass
    toks.unget(t)
    e = parse_expr(toks)
    if toks.peek()[-1] == '=': todo('assignment')
    return Expr(e)

def parse_expr(toks, prec=0):
    #literal
    t = next(toks)
    if t[0] == '"':
        curr = String(t[1:-1])
        t = next(toks)
    else: curr = Id(t)
    if t == '.':
        curr = Method(curr, parse_expr(toks))
        t = next(toks)
    #operators
    return curr
