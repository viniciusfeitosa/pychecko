from pychecko import PycheckoComponent


class MyComponentA(PycheckoComponent):

    def is_applied(self):
        return True

    def bar(self):
        self.email = 'john.doe@email.com'


class MyComponentB(PycheckoComponent):

    def is_applied(self):
        return True

    def name_changer(self):
        self.first_name = 'john doe'
