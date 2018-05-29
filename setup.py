try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyChecko',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.3.0',
    url='https://github.com/viniciusfeitosa/pychecko/',
    license='MIT',
    author='Vinicius Pacheco',
    author_email='vfpweb@gmail.com',
    description='MicroFramework to compose instances in execution time',
    zip_safe=False,
    platforms='any',
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
