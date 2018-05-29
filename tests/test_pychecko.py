import pytest
from pychecko import (
    InvalidInputError,
    InvalidMethodError,
    InvalidRuleError,
    InvalidSignatureClassError,
    InvalidSignatureInputTypeError,
    Pychecko,
    PycheckoClassModifier
)
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

    def test_simple_class_composition(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = PycheckoClassModifier(
            my_class, [
                fix_module.MyFixComponentA(),
            ])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        my_class.fix_method(3)
        my_class.fix_method_b(3)
        assert str(my_class) == '1, 28, 18'

    def test_multiple_class_composition(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = PycheckoClassModifier(
            my_class, [
                fix_module.MyFixComponentA(),
                fix_module.MyFixComponentB(),
            ])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        assert 'fix_method_b' in my_class.__dict__
        my_class.fix_method(3)
        my_class.fix_method_b(3)
        assert str(my_class) == '1, 33, 18'

    def test_sorting_multiple_class_composition(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = PycheckoClassModifier(
            my_class, [
                fix_module.MyFixComponentB(),
                fix_module.MyFixComponentA(),
            ])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        assert 'fix_method_b' in my_class.__dict__
        my_class.fix_method(3)
        my_class.fix_method_b(3)
        assert str(my_class) == '1, 28, 18'

    def test_false_multiple_class_composition(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = PycheckoClassModifier(
            my_class, [
                fix_module.MyFixComponentA(),
                fix_module.MyFixComponentB(),
                fix_module.MyFixComponentFalse(),
            ])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        assert 'fix_method_b' in my_class.__dict__
        my_class.fix_method(3)
        my_class.fix_method_b(3)
        assert str(my_class) == '1, 33, 18'

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

    def test_composition_with_two_equal_methods_true(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__

        p = Pychecko(my_class)
        p.add(fix_method, [True])
        p.add(fix_module.fix_method, [True])

        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        my_class.fix_method(5)
        assert str(my_class) == '1, 2, 15'

    def test_bulk_addiction(self):
        my_class = FixClass(1, 2)
        assert 'fix_method' not in my_class.__dict__
        assert 'fix_method_b' not in my_class.__dict__

        p = Pychecko(my_class)
        p.bulk_add(
            [
                fix_module.fix_method,
                fix_module.fix_method_b,
            ],
            [True]
        )
        my_class = p.execute
        assert 'fix_method' in my_class.__dict__
        assert 'fix_method_b' in my_class.__dict__
        my_class.fix_method(3)
        my_class.fix_method_b(4)
        assert str(my_class) == '1, 2, 13'
        assert my_class.d == 24

    def test_composition_with_signature(self):
        test_cases = [('fix_method', ), ['fix_method']]
        for test_case in test_cases:
            my_class = FixClass(1, 2)
            assert 'fix_method' not in my_class.__dict__

            p = Pychecko(my_class, ('fix_method', ))
            p.add(fix_method, [True])
            p.add(fix_module.fix_method, [False])

            my_class = p.execute
            assert 'fix_method' in my_class.__dict__
            my_class.fix_method(3)
            assert str(my_class) == '1, 2, 3'

    def test_exceptions(self):
        test_cases = [
            {
                'method': fix_method,
                'rule': True,
                'signature': None,
                'error': InvalidInputError,
            },
            {
                'method': 'method',
                'rule': [True],
                'signature': None,
                'error': InvalidMethodError,
            },
            {
                'method': fix_method,
                'rule': ['rule'],
                'signature': None,
                'error': InvalidRuleError},
            {
                'method': fix_method,
                'rule': [True],
                'signature': ['fix_method', 'method'],
                'error': InvalidSignatureClassError,
            },
            {
                'method': fix_method,
                'rule': [True],
                'signature': 'fix_method',
                'error': InvalidSignatureInputTypeError,
            },
        ]

        for test_case in test_cases:
            with pytest.raises(test_case['error']):
                my_class = FixClass(1, 2)
                p = Pychecko(my_class, test_case['signature'])
                p.add(test_case['method'], test_case['rule'])
                my_class = p.execute
