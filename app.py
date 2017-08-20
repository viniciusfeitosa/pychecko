import lib
from pychecko import Pychecko


def bar(self):
    self.c = 'vfpweb@gmail.com'


class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def foo(self):
        print('{a} {b}: {c}'.format(a=self.a, b=self.b, c=self.c))


if __name__ == '__main__':
    a = A('vinicius', 'pacheco')
    pycheck = Pychecko(a)
    pycheck.add(bar, [a.a == 'vinicius', a.b == 'pacheco']),
    pycheck.add(lib.bar, [a.a != 'vinicius' or a.b != 'pacheco']),

    a = pycheck.execute

    a.bar()
    a.foo()
