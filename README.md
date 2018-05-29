# PyChecko  [![Build Status](https://travis-ci.org/viniciusfeitosa/pychecko.svg?branch=master)](https://travis-ci.org/viniciusfeitosa/pychecko)

The PyChecko is a MicroFramework to compose a instance in execution time by rules predefined.

# Example:

There are some [examples](example/).

# Installation:

```
pip install pychecko
```

# Getting started

Inside the directory application...

## Defining class to be used

Our example has two modules, the `app.py` and the `lib.py`.
Inside the `lib.py` there is a method to apply over a class.

```python
# lib.py
def bar(self):
    self.email = 'john.doe@email.com'
```

Inside the `app.py` there are a method to apply over the class instance too.
Take a look in the code comments to understand the logic

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

## Pychecko with bulk insert

```python
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
```

## Pychecko Using Classes

```python
from pychecko import PycheckoComponent

# Creating a pycheko component
class MyComponentA(PycheckoComponent):

    # is_applied is required for the PychecoComponents
    # It's responsible to identify if all class methods
    # should be applied in an instance
    def is_applied(self):
        return True

    def bar(self):
        self.email = 'john.doe@email.com'


class MyComponentB(PycheckoComponent):

    def is_applied(self):
        return True

    def name_changer(self):
        self.first_name = 'john doe'
```

```python
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

```

## Applying instance validation

Another possible option is validate the instance integrity.

```python
# app.py

'''
create a list with the name methods that must be
in the instance after execute the Pychecko
'''
instance_signature [
    'method_a',
    'method_b',
    'method_c',
]

# In the Pychecko declaration, send the list in the optional parameter
a = A('value1', 'value2')
pycheck = Pychecko(a, signature=instance_signature)
# ...

'''
At final, if all methods that you sent in the list
to Pychecko are in the instance, the instance will be returned
using the `execute` property.

If the instance does't respect the signature will the thrown the
Exception InvalidSignatureClassError
'''
a = pycheck.execute

# ...
```

# Next Features

* Check signature at method level
