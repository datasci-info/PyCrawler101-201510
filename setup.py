'''
Created on Sep 20, 2015

@author: c3h3
'''

#try:
#    from setuptools import setup
#except ImportError:
#    from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name='pycrawler101',
    version='0.0.1dev',
    author='Chia-Chi Chang',
    author_email='c3h3.tw@gmail.com',
    packages=find_packages(),
    install_requires=["html5lib",
                      "requests",
                      "pyquery",
                      "pandas",
                      "numpy"],
)
