from pychecko import PycheckoComponent


def fix_method(self, c):
    self.c = (c + 10)


def fix_method_b(self, d):
    self.d = (d + 20)


class MyFixComponentA(PycheckoComponent):
    def is_applied(self):
        return True

    def fix_method(self, c):
        self.c = (c + 15)

    def fix_method_b(self, b):
        self.b = (b + 25)


class MyFixComponentB(PycheckoComponent):
    def is_applied(self):
        return True

    def fix_method_b(self, b):
        self.b = (b + 30)


class MyFixComponentFalse(PycheckoComponent):
    def is_applied(self):
        return False

    def fix_method_b(self, b):
        self.b = (b + 40)
