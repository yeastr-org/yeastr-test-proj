# Look at the output of this example saved into localci/out/src_macros_py*

@def_macro(hygienic=False)
def m_hf(b):
    if a > 3:
        c = 3
    if b > 3:
        c = -3

@def_macro(hygienic=True)
def m_ht(b):
    if a > 3:
        c = 3
    if b > 3:
        c = -3

def test_hygiene():
    for hyg in (True, False):
        a = 2
        # NOPE, u cannot (m_ht if hyg else m_hf)(4)
        if hyg: m_ht(4)
        else: m_hf(4)
        try:
            print(c)
        except NameError:
            print('why did u switch hygienic on?')
        try:
            print(b)
        except NameError:
            print('all right')
test_hygiene()

'''
# gotta fight with this
@def_macro(hygienic=False)
def acc(x):
    a += x

@with_macros
def test():
    a = 3
    print(a, acc(3), a)
'''


# Now we want to evaluate something during macro expansion
# we have a very limited mLang flag (please should be limited)

@def_macro(severity=-1, mLang=True)
def printout(msg):
    with mIf(severity > 0):
        print(msg)

def letssee():
    printout('ciao', severity=1)
    printout('no', severity=0)
    printout('no')

letssee()

# Now we want to make sure we can retain macros after the build
@def_macro(strip=False)
def preserved_macro(as_fn):
    print((msg := 'dangerous, used as function'
                  if as_fn else
                  'macro preserved'))


preserved_macro(True, defer_expansion=True)
try:
    assert msg is None
except NameError:
    ...

@with_macros()
def correct_preserved_usage():
    preserved_macro(False, defer_expansion=True)
    assert msg == 'macro preserved', 'Failed'

correct_preserved_usage()

def also_expandable_at_build_time():
    preserved_macro(False)
    assert msg == 'macro preserved', 'Failed'

also_expandable_at_build_time()

# Now you can compare "the same example" at import time

@def_macro(severity=-1, mLang=True, strip=False)
def printout(msg):
    with mIf(severity > 0):
        print(msg)

@with_macros()
def letssee():
    printout('ciao', severity=1, defer_expansion=True)
    printout('no', severity=0, defer_expansion=True)
    printout('no', defer_expansion=True)

letssee()

# Let's make sure you can nest macro definitions

@def_macro()
def inner():
    print('inner')

@def_macro()
def outer():
    inner()
    inner()

outer()  # expecting two print('inner')

# Well, does that also work at import time?

@def_macro(strip=False)
def inner2():
    print('inner2 it')

@def_macro(strip=False)
def outer2():
    inner2(defer_expansion=True)
    inner2(defer_expansion=True)

@with_macros()
def test_it_nested():
    outer2(defer_expansion=True)

test_it_nested()


# ok, so you can use @def_macro without ()

@def_macro
def my_m():
    print('okay')

my_m()


# so you want expression macros?
# mhh.. why?
# let's try shortening some code
import ast
@def_macro(expr=True, mLang=True)
def a_cmp(left, ops, comparators):
    """ast.Compare: usually you cmp just 2 objs"""
    with mIf(
        isinstance(ops, ast.List)
        and isinstance(comparators, ast.List)
    ):
        # keep the default behaviours
        ast.Compare(
            left=left,
            ops=ops,
            comparators=comparators,
        )
    with mIf(not isinstance(ops, ast.List)):
        # if ops is not a list, it means
        # comparators is not a list either
        ast.Compare(
            left=left,
            ops=[ops],
            comparators=[comparators],
        )

print(ast.dump(
    a_cmp(
        ast.Name('subj', ctx=ast.Load()),
        ast.Eq(),
        ast.Constant(3)
    )
))
# Compare(left=Name(id='subj'), ops=[Eq()], comparators=[Constant(value=3)])
# awesome... ofc, this means after mLang, there must be only 1 expression left.
# as you can see, you can use positional arguments,
# and they can be whatever you want, won't get converted..
# TODO: check they actually don't get converted
# no new names are bound, just literal substitution.

# an expr macro without mLang raises a TransformError
# when more than one expression is used
# ... it's AssertionError...
#@def_macro(expr=True)
#def wrong():
#    exp1
#    exp2
