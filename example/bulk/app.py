# app.py
from pychecko import Pychecko


# Method bar definition outside the class
def bar(self):
    self.email = 'bar@email.com'


# Method foo definition outside the class
def foo(self):
    print('{first_name} {last_name}: {email}'.format(
        first_name=self.first_name,
        last_name=self.last_name,
        email=self.email))  # attribute that is defined just in the bar


# Class A definition
class A:
    def __init__(self, first_name, last_name):
        # There are just two attributes
        self.first_name = first_name
        self.last_name = last_name


# the main logic
if __name__ == '__main__':
    # Instantiate the class A
    a = A('FirstName', 'LastName')
    # pass the instance variable to PyChecko
    pycheck = Pychecko(a)

    # Add the methods that you want apply

    # Two bool conditions
    pycheck.bulk_add(
        [
            bar,
            foo,
        ]
        [True]
    )

    # running PyChecko and get the modified instance
    a = pycheck.execute

    a.bar()
    a.foo()  # The result is: FirstName LastName: 'bar@email.com'
