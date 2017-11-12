from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = '\n' + readme.read()

setup(
    name='datatyping',
    description='Pythonic type checking',
    long_description=long_description,
    keywords='safe data validation typing type check',
    url='https://github.com/Zaab1t/datatyping',
    author='Carl Bordum Hansen',
    author_email='carl@bordum.dk',
    version='0.5.1',
    copyright='Copyright (c) 2017 Carl Bordum Hansen',
    license='MIT',
    packages=['datatyping'],
)
