#!/usr/bin/python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(
    name = 'redmine-issue-registerd',
    version = '0.0.1',
    description = 'Register auto issue of Redmine by receiving e-mail',
    license = 'MIT license',
    author = 'Yusuke Watanabe',
    author_email = 'yusuke.w62@gmail.com',
    url = 'https://github.com/yusukew62/redmine-issue-registerd.git',
    keywords = 'python redmine',
    packages = find_packages(),
    install_requires = [''],
    entry_points = {
        'console_scripts': [
            'redmine-ird=redmine-ird.redmine-ird:main',
        ],
    },
)
    
