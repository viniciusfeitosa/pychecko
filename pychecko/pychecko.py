'''
Pychecko is a microframework to compose
the methods in an instance in real time.
'''
import types


class PyCheckoException(Exception):
    '''Most genetic exception in Pychecko.'''
    pass


class InvalidRuleError(PyCheckoException):
    '''
    This exception will be thrown when the rule sent to
    Pychecko is not a Boolean condition.
    '''

    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class InvalidMethodError(PyCheckoException):
    '''
    This exception will be thrown when the method sent to
    Pychecko is not a real method.
    '''

    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class Pychecko:
    def __init__(self, instance):
        self.__methods_to_add = list()
        self.__instance = instance

    def add(self, method, rules=[]):
        '''
        The method is responsible to add all methods to compose an instance.

        :param method: is the method that will be applied over the instance
        :param rules: (optional) a list of boolean conditions to check if the
        method should be applied in execution time.
        '''
        self.__inputs_validate(method, rules)
        if all(rules):
            self.__methods_to_add.append(method)

    def __inputs_validate(sel, method, rules=[]):
        '''
        Method resposible to validade if the inputs are right to
        apply over the instance.
        '''
        if not hasattr(method, '__call__'):
            raise InvalidMethodError(
                "The {method} isn't a valid method".format(
                    method=method,
                )
            )

        for rule in rules:
            if not isinstance(rule, bool):
                raise InvalidRuleError(
                    "The {rule} isn't a boolean condition".format(
                        rule=rule,
                    )
                )

    @property
    def execute(self):
        '''
        Property responsible to apply all method that the rules match
        and prepare the instance

        :return: modified instance
        '''
        for method in self.__methods_to_add:
            setattr(
                self.__instance,
                method.__name__,
                types.MethodType(method, self.__instance),
            )
        return self.__instance
