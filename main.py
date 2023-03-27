testinput = ['drog', 'test.dr', 'test.py']

#command-line arguments
from sys import argv, exit
try: argv = testinput
except: pass
argv = iter(argv)
scriptname = next(argv)
files = []
opts = {}
for a in argv:
    if a == '-h':
        print('usage:', scriptname, 'program.dr output')
        exit(0)
    else: files.append(a)
if len(files)==0:
    infile = input('File to be compiled: ')
    outfile = input('Compiled file name: ')
else:
    infile = files[0]
    try: outfile = files[1]
    except: outfile = infile.removesuffix('.dr')

#process
with open(infile) as f: code = f.read()
from parser import parse
dfns = parse(code)
print(dfns)
#stuff:tm:

#compile
lang = 'py' #for now
backend = __import__('backend_'+lang)
backend.compile(dfns, outfile, **opts)
