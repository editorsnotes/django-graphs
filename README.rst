======
Graphs
======

Graphs provides an mixin for associating instances of Django models
with graphs of data, and middleware for associating an RDFLib Store
with requests.

Quick start
-----------

1. Add "licensing" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'graphs',
      )
