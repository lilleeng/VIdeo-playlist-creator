
def foo():
    yield 'hello'
    print('!')
    yield 'world'
    yield

bar = foo()
print(next(bar))
print(next(bar))
next(bar)