try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='PyChecko',
    packages=find_packages(),
    version='1.1.1',
    url='https://github.com/viniciusfeitosa/pychecko/',
    license='MIT',
    author='Vinicius Pacheco',
    author_email='vfpweb@gmail.com',
    description='MicroFramework to compose instances in execution time',
    zip_safe=False,
    platforms='any',
)
