# app.py
import lib  # inside lib has a method bar with the attribute email definition
from pychecko import PycheckoClassModifier


# There is another method bar with a different
# definition to the attribute email
def bar(self):
    self.email = 'bar@email.com'


# Class A definition
class A:
    def __init__(self, first_name, last_name):
        # There are just two attributes
        self.first_name = first_name
        self.last_name = last_name

    # And just the method foo
    def foo(self):
        print('{first_name} {last_name}: {email}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email))  # attribute that is defined just in the bar


# the main logic
if __name__ == '__main__':
    # Instantiate the class A
    instance = A('FirstName', 'LastName')
    # pass the instance variable to PyCheckoClassModifier
    # whit the classes that should be applied
    pycheck = PycheckoClassModifier(instance, [
        lib.MyComponentA(),  # This implements bar()
        lib.MyComponentB(),  # This implements name_changer()
    ])

    # running PyChecko and get the modified instance
    a = pycheck.execute

    a.bar()
    a.name_changer()
    a.foo()  # The result is: John Doe LastName: 'bar@email.com'
