Introduction
############

``metaprams`` is a MetaClass/Class/Decorator infrastructure to define params
without invoking objects and have them automatically parse/remove the ``kwargs``
passed to the class in which they are intalled


Features:
=========

  - ``metaparams`` decorator to params-enable any class

  - ``ParamsBase`` a class from which to subclass to also be params-enabled

  - ``MetaParams`` a MetaClass for more complex usage pattern


Installation
============

From pypi::

  pip install metaparams

From source:

  - Place the *metaparams* directory found in the sources inside your project
