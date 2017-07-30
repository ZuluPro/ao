#!/usr/bin/env python
from setuptools import setup, find_packages
import ao


def get_requirements():
    return open('requirements.txt').read().splitlines()


def get_test_requirements():
    return open('requirements-tests.txt').read().splitlines()

keywords = [
    'cloud', 'test', 'mock', 'azure', 'microsoft',
]

setup(
    name='ao',
    version=ao.__version__,
    description=ao.__doc__,
    author=ao.__author__,
    author_email=ao.__email__,
    install_requires=get_requirements(),
    tests_require=get_test_requirements(),
    license='BSD',
    url=ao.__url__,
    keywords=keywords,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
