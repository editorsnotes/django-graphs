======
Graphs
======

Graphs provides a mixin for associating instances of Django models
with graphs of data, and middleware for associating an RDFLib Store
with requests.

Quick start
-----------

0. Run tests like this::

      django-admin.py test --settings=graphs.testsettings

1. Add "graphs" to your ``INSTALLED_APPS`` setting like this::

      INSTALLED_APPS = (
          ...
          'graphs',
      )

2. Put your triplestore info in a ``STORE`` setting::

      STORE = {'TYPE':'SQLAlchemy',  # name of rdflib Store plugin
               'ID':'mytriplestore', # your store identifier
                                     # plugin-specific configuration string
               'CONFIG':'sqlite:///{}/test.sqlite'.format(os.getcwd())}


