# app.py
import lib  # inside lib has a method bar with the attribute email definition
from pychecko import Pychecko


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
    a = A('FirstName', 'LastName')
    # pass the instance variable to PyChecko
    pycheck = Pychecko(a)

    # Add the methods that you want apply

    # Two bool conditions
    pycheck.add(
        bar,
        [a.first_name == 'FirstName', a.last_name == 'LastName']
    )
    # One bool condition
    pycheck.add(
        lib.bar,
        [a.first_name != 'FirstName' or a.last_name != 'LastName']
    )

    # running PyChecko and get the modified instance
    a = pycheck.execute

    a.bar()
    a.foo()  # The result is: FirstName LastName: 'bar@email.com'
