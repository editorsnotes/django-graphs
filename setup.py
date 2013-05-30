import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# TODO: run tests from setup.py

setup(
    name='django-graphs',
    version='0.1',
    packages=['graphs'],
    install_requires=['rdflib-sqlalchemy==0.2.dev'],
    include_package_data=True,
    license='Public Domain',
    description='A Django mixin and middleware for linking graphs to objects.',
    long_description=README,
    url='http://github.com/editorsnotes/django-graphs',
    author='Ryan Shaw',
    author_email='ryanshaw@unc.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
