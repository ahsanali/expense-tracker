# -*- coding: utf-8 -*-

from setuptools import setup

project = "Expense Tracker"

setup(
    name=project,
    version='0.1',
    url='https://github.com/ahsanali/expense-tracker',
    description='Expense Tracker is a Flask, Angular JS based web app to track expenses',
    author='Muhammad Ahsan Ali',
    author_email='ahsan.snali@gmail.com',
    packages=["tracker"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-Testing',
        'Flask-Mail',
        'Flask-Cache',
        'Flask-Login',
        'Flask-OpenID',
        'nose',
        'tornado',
        'psycopg2',
        'wtforms_alchemy',
        'flask-restful',
        'Flask-WTF',
        'marshmallow'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
