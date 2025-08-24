@def_macro(cfg=None, mLang=True)
def test_conditionals():
    print('first print')
    with mIf(cfg[0] is True):
        print('0 True')
        with mIf(cfg[1] is True):
            print('1 True')
    print('middle print')
    with mIf(cfg[2] is True):
        print('2 True')
        print('2 True again')
    print('last print')

print([True, True, True])
test_conditionals(cfg=[True, True, True])
print([True, True, False])
test_conditionals(cfg=[True, True, False])
print([True, False, True])
test_conditionals(cfg=[True, False, True])
print([True, False, False])
test_conditionals(cfg=[True, False, False])
print([False, True, False])
test_conditionals(cfg=[False, True, False])

print('---------- test 2')
@def_macro(cfg=None, mLang=True)
def test_conditionals2():
    with mIf(cfg[0] is True):
        with mIf(cfg[1] is True):
            print('1 True')
    if True:
        with mIf(cfg[2] is True):
            print('2 True')
        pass
print([True, True, True])
test_conditionals2(cfg=[True, True, True])
print([True, True, False])
test_conditionals2(cfg=[True, True, False])
print([True, False, True])
test_conditionals2(cfg=[True, False, True])
print([True, False, False])
test_conditionals2(cfg=[True, False, False])
print([False, True, False])
test_conditionals2(cfg=[False, True, False])


