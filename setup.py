import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='PyChecko',
    version='1.0.0',
    url='https://github.com/viniciusfeitosa/pychecko/',
    license='MIT',
    author='Vinicius Pacheco',
    author_email='vfpweb@gmail.com',
    description='MicroFramework to compose instances in execution time',
    # long_description=read('README.md'),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'tox',
        'pytest',
    ]
)