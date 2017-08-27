# PyChecko  [![Build Status](https://travis-ci.org/viniciusfeitosa/pychecko.svg?branch=master)](https://travis-ci.org/viniciusfeitosa/pychecko)

The PyChecko is a MicroFramework to compose a instance in execution time by rules predefined.

# Example:

There is an [example](example/).

# Instalation:

```
pip install pychecko
```

# Getting started

Inside the directory application...

## Defining class to be used

Our example has two module, the `app.py` and the `lib.py`.
Inside the `lib.py` there is a method to apply over a class.

```python
# lib.py
def bar(self):
    self.email = 'john.doe@email.com'
```

Inside the `app.py` there are the a method to apply over the instance class, the class definition, the `PyChecko` and the `lib` module importation and run the logic to use `PyChecko`

Thake a look in the code comments to understand the logic

```python
# app.py
import lib # inside lib has a method bar with the attribute email definition
from pychecko import Pychecko


# There is another method bar with a different definition to the attribute email
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
            email=self.email)) # There is a attribute that is defined just in the bar


# the main logic
if __name__ == '__main__':
    # Instantiate the class A
    a = A('FirstName', 'LastName')
    # pass the instance variable to PyChecko
    pycheck = Pychecko(a)
    # Add the methods that you want apply
    pycheck.add(
        bar,
        [a.first_name == 'FirstName', a.last_name == 'LastName'] # Two bool conditions
    )
    pycheck.add(
        lib.bar,
        [a.first_name != 'FirstName' or a.last_name != 'LastName'] # One bool condition
    )

    # running PyChecko and get the modified instance
    a = pycheck.execute

    a.bar()
    a.foo() # The result will be: FirstName LastName: 'bar@email.com'
```

# Next Features

* Create the bulk add
* Create the validation to signature class