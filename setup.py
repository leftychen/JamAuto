#using setuptools to get the package
from setuptools import setup, find_packages
from codecs import open
from os import path

filepath = path.abspath(path.dirname(__file__))

#Get the Description from the README FILE
with(open(path.join(filepath, "README.rst"), encoding='utf-8')) as f:
    description = f.read()

setup(
    name = 'JamAuto',
    version='0.1.0',
    description='Python Trading and Algorithm Platform',
    long_description=description,
    #main homepage
    url='https://github.com/leftychen/JamAuto',

    #Author info
    author='Jamauto team',
    author_email='lefty-chen@hotmail.com',
    license = 'Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Self',
        'Topic :: Software Development :: Build Platform and Algorithm',
        'License :: OSI Approved :: Apache 2.0',
        'Programming Language :: Python :: 3.5',

    ],
    packages = find_packages(exclude=['doc', 'tests', 'temp', 'tutorial']),

    install_requires = ['numpy>=1.9.0',
                        'statsmodels>=0.6.0',
                        'matplotlib>=1.4.0',
                        'tushare>=0.4.0',
                        'pandas>=0.16.0'
                        ]
)