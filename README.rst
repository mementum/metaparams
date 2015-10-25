
metaparams
==========

.. image:: https://img.shields.io/pypi/v/metaparams.svg
   :alt: PyPi Version
   :scale: 100%
   :target: https://pypi.python.org/pypi/metaparams/

.. image:: https://img.shields.io/pypi/dm/metaparams.svg
   :alt: PyPi Monthly Donwloads
   :scale: 100%
   :target: https://pypi.python.org/pypi/metaparams/

.. image:: https://img.shields.io/pypi/l/metaparams.svg
   :alt: License
   :scale: 100%
   :target: https://github.com/mementum/metaparams/blob/master/LICENSE

.. image:: https://travis-ci.org/mementum/metaparams.png?branch=master
   :alt: Travis-ci Build Status
   :scale: 100%
   :target: https://travis-ci.org/mementum/metaparams

.. image:: https://readthedocs.org/projects/metaparams/badge/?version=latest
   :alt: Documentation Status
   :scale: 100%
   :target: https://readthedocs.org/projects/metaparams/

.. image:: https://img.shields.io/pypi/pyversions/metaparams.svg
   :alt: Pytghon versions
   :scale: 100%
   :target: https://pypi.python.org/pypi/metaparams/

``metaparams`` is a MetaClass/Class/Decorator infrastructure to define params
without invoking objects and have them automatically parse/remove the ``kwargs``
passed to the class in which they are intalled

Documentation
=============

Read the full documentation at readthedocs.org:

  - `metaparams documentation <http://metaparams.readthedocs.org/en/latest/introduction.html>`_

Python 2/3 Support
==================

  - Python 2.7
  - Python 3.2/3.3/3.4/3.5

  - It also works with pypy and pypy3

Installation
============

From pypi::

  pip install metaparams

From source:

  - Place the *metaparams* directory found in the sources inside your project

Features:
=========

  - ``metaparams`` decorator to params-enable any class

  - ``ParamsBase`` a class from which to subclass to also be params-enabled

  - ``MetaParams`` a MetaClass for more complex usage pattern


Quick Usage
===========

With the decorator::

  from metaparams import metaparams


  @metaparams()
  class A(object):

      params = (
          ('p1', True, 'doc'),
          ('p2', 99),
      )

      def __init__(self):
          pass

  a = A()

  # Defined params are reachable below the attribute params
  print(a.params.p1)
  print(a.params.p2)

  # Modification of default values can be checked
  assert a.params._isdefault('p1')

  # Inheriting with modification an extension
  class B(A):

      params = (
          ('p1', False,),  # changed default value of p1
          ('p3', None),  # new parameter
      )

      def __init__(self):
          pass

  b = B()

  # Defined params are reachable below the attribute params
  print(b.params.p1)
  print(b.params.p2)
  print(b.params.p3)

  # Modification of default values can be checked
  assert b.params._isdefault('p1')

  # Over the class we can also check defaults
  # B has different default value for p1 than A
  assert b.params.p1 != A.params._default('p1')

  # The name of the attribute 'params' can be changed
  # and a shorter alias (PEP-8 ...) added
  @metaparams(_pname='kargs', _pshort=True)
  class A(object):

      kargs = (
          ('p1', True, 'doc'),
          ('p2', 99),
      )

      def __init__(self):
          pass

  a = A()

  # Defined params are reachable below the attribute params
  print(a.kargs.p1)
  print(a.kargs.p2)

  print(a.k.p1)
  print(a.k.p2)

  # Modification of default values can be checked
  assert a.kargs._isdefault('p1')


  # The metaclass works also so ... but it's a metaclass

  class A(MetaParams.as_metaclass(_pname='kargs', _pshort=True)):

      kargs = (
          ('p1', True, 'doc'),
          ('p2', 99),
      )

      def __init__(self):
          pass

  a = A()

  # Defined params are reachable below the attribute params
  print(a.kargs.p1)
  print(a.kargs.p2)

  print(a.k.p1)
  print(a.k.p2)

  # Modification of default values can be checked
  assert a.kargs._isdefault('p1')


  # And finally an already cooked base class with no customization
  class A(ParamsBase):

      params = (
          ('p1', True, 'doc'),
          ('p2', 99),
      )

      def __init__(self):
          pass

  a = A()

  # Defined params are reachable below the attribute params
  print(a.params.p1)
  print(a.params.p2)

  # Modification of default values can be checked
  assert a.params._isdefault('p1')
