# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ployparser',
    version='0.1.0',
    description='Expression parser for BRASS MARS project',
    long_description=readme,
    author='Pooyan Jamshidi',
    author_email='pooyan.jamshidi@gmail.com',
    url='https://github.com/pooyanjamshidi',
    acknowledgement='The class parser in this repository is mainly based on js-expression-eval, by Matthew Crumley (email@matthewcrumley.com, http://silentmatt.com/) https://github.com/silentmatt/js-expression-eval and https://github.com/Axiacore/py-expression-eval',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)