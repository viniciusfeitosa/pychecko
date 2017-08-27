from pychecko import Pychecko
from tests import fix_module


def fix_method(self, c):
    self.c = c


class FixClass(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        if hasattr(self, 'c'):
            return '{}, {}, {}'.format(self.a, self.b, self.c)
        return '{}, {}'.format(self.a, self.b)


class TestPyChecko(object):

    def test_composition_without_condition(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = Pychecko(my_class)
        p.add(fix_method)

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        my_class.fix_method(3)
        assert str(my_class) == '1, 2, 3'

    def test_composition_with_condition_false(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = Pychecko(my_class)
        p.add(fix_method, [False])

        my_class = p.execute
        assert 'fix_method' not in my_class.__dict__
        assert str(my_class) == '1, 2'

    def test_composition_with_condition_true(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = Pychecko(my_class)
        p.add(fix_method, [True])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        my_class.fix_method(5)
        assert str(my_class) == '1, 2, 5'

    def test_composition_with_two_equal_methods(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = Pychecko(my_class)
        p.add(fix_method, [False, True])
        p.add(fix_module.fix_method, [True])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        my_class.fix_method(5)
        assert str(my_class) == '1, 2, 15'
