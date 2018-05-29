'''
Pychecko is a microframework to compose
the methods in an instance in real time.
'''
import collections
import inspect
import types

from abc import (
    ABCMeta,
    abstractmethod,
)


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


class InvalidSignatureInputTypeError(PyCheckoException):
    '''
    This exception will be thrown when the signature has not
    completely attended by the methods passed to PyChecko
    '''

    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class InvalidSignatureClassError(PyCheckoException):
    '''
    This exception will be thrown when the signature has not
    completely attended by the methods passed to PyChecko
    '''

    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class InvalidInputError(PyCheckoException):
    '''
    This exception will be thrown when the signature has not
    completely attended by the inputs passed to PyChecko
    '''

    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class Pychecko:
    def __init__(self, instance, signature=None):
        self.__methods_to_add = list()
        self.__instance = instance
        if (
            signature and
            (
                not isinstance(signature, (tuple, list)) or
                not all(isinstance(s, str) for s in signature)
            )
        ):
            raise InvalidSignatureInputTypeError(
                "Type is: {}. The type should be tuple or list"
                .format(type(signature))
            )
        self.__signature = signature

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

    def bulk_add(self, methods, rules=[]):
        self.__validate_iterable(methods)

        for method in methods:
            self.add(method, rules)

    def __inputs_validate(self, method, rules=[]):
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

        self.__validate_iterable(rules)

        for rule in rules:
            if not isinstance(rule, bool):
                raise InvalidRuleError(
                    "The {rule} isn't a boolean condition".format(
                        rule=rule,
                    )
                )

    def __validate_iterable(self, iterable):
        if not isinstance(iterable, collections.Iterable):
            raise InvalidInputError('The input is not an Iterable')

    @property
    def class_signature(self):
        return self.__instance

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

        if (
            self.__signature and not
            set(self.__signature).issubset(self.__instance.__dict__)
        ):
            raise InvalidSignatureClassError()
        return self.__instance


class PycheckoComponent:
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_applied(self):
        pass


class PycheckoClassModifier:
    """
    Class reponsible to modify an instance and create the composition.
    Must be sent to the class an Intance and the components list that
    will be applied over the instance.
    * The Pychecko Framework manipulate just Instances and Methods.
    No attributes, properties or just class signature.
    All the params sent to the Framework must be instantiated
    * The component list sent has precedence order priority
    from the last to the first item in the list
    * All the components in the component list must be a
    PycheckoComponent by inheritance and implement the method
    **is_apply**. The is_apply must return a boolean condition.
    * If the methods in the component list are in the instance calulator,
    the method in the instance calulator will be overwrited.
    * If the methods in the component list are not in the instance
    calulator, these methods will be added.
    * If some instance in component list is not a PycheckoComponent
    will be thrown an InvalidInputError.
    * If after read all the itens in component list no methods
    are found will be thrown an InvalidMethodError.
    * After process all the used the property **get_modified_instance**
    to get the modified instance.

    :param: instance\n
    :param: components (optional)
    """

    def __init__(self, instance, components=[]):
        self.__instance = instance
        for component in components:
            if not issubclass(component.__class__, PycheckoComponent):
                raise InvalidInputError(
                    '{} are not a Pychecko Component'.format(
                        component.__class__.__name__
                    )
                )
        self.__components = components

    @property
    def execute(self):
        """
        Property responsible to apply all method that the rules match
        and prepare the instance
        :return: modified instance
        """
        for component in self.__components:
            methods = inspect.getmembers(component, inspect.ismethod)
            methods = [
                m
                for m in methods
                if not m[0].startswith('_') and
                not m[0] == 'is_applied'
            ]
            if not methods:
                raise InvalidMethodError(
                    'There are no methods in the component {}'.format(
                        component.__class__.__name__
                    )
                )
            if component.is_applied():
                for method in methods:
                    method_name = method[0]
                    setattr(
                        self.__instance,
                        method_name,
                        types.MethodType(
                            component.__class__.__dict__[method_name],
                            self.__instance
                        ),
                    )
        return self.__instance
