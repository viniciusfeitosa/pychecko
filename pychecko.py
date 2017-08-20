# file: pychecko
import types


class PyCheckoException(Exception):
    pass


class InvalidRuleError(PyCheckoException):
    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class InvalidMethodError(PyCheckoException):
    def __init__(self, msgError=None):
        if msgError:
            self.message = msgError


class Pychecko:
    def __init__(self, instance):
        self.__methods_to_add = list()
        self.__instance = instance

    def add(self, method, rules=[]):
        self.__validate(method, rules)
        if self.__is_applied(rules):
            self.__methods_to_add.append(method)

    def __validate(sel, method, rules=[]):
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

    def __is_applied(self, rules):
        return all(rules)

    @property
    def execute(self):
        for method in self.__methods_to_add:
            setattr(
                self.__instance,
                method.func_name,
                types.MethodType(method, self.__instance),
            )
        return self.__instance
