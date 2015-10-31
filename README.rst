
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

The example below is available in the source as a single file test. It's broken
down into parts to ease up reading::

    from __future__ import (absolute_import, division, print_function,
                            unicode_literals)


    from metaparams import metaparams, MetaParams, ParamsBase

    print('=' * 50)
    print('Creating A with params with DECORATOR')


    @metaparams()
    class A(object):

        params = (
            ('p1', True, 'doc'),
            ('p2', 99),
        )

        def __init__(self):
            pass

    print('-- Instantiating A with no kwargs')
    a = A()

    # Defined params are reachable below the attribute params
    print('a.params.p1:', a.params.p1)
    print('a.params.p2:', a.params.p2)

    # Modification of default values can be checked
    print('Checking if p1 has default value:', a.params._isdefault('p1'))

    print('=' * 50)
    print('Creating B as subclass from A, changing p1, adding p3')

This first part produces the following output::

    ==================================================
    Creating A with params with DECORATOR
    -- Instantiating A with no kwargs
    a.params.p1: True
    a.params.p2: 99
    Checking if p1 has default value: True

The 2nd part::

    # Inheriting with modification an extension
    class B(A):

        params = (
            ('p1', False,),  # changed default value of p1
            ('p3', None),  # new parameter
        )

        def __init__(self):
            pass

    print('-- Instantiating B with no kwargs')
    b = B()

    # Defined params are reachable below the attribute params
    print('b.param.p1 (default changed):', b.params.p1)
    print('b.params.p2 (same default):', b.params.p2)
    print('b.params.p3 (new param):', b.params.p3)

    # Modification of default values can be checked
    print('Checking if p1 has default value:', b.params._isdefault('p1'))

    # Over the class we can also check defaults
    # B has different default value for p1 than A
    print('Checking default in B for p1 is not the same as default in A:',
          b.params.p1 != A.params._default('p1'))

Output::

    ==================================================
    Creating B as subclass from A, changing p1, adding p3
    -- Instantiating B with no kwargs
    b.param.p1 (default changed): False
    b.params.p2 (same default): 99
    b.params.p3 (new param): None
    Checking if p1 has default value: True
    Checking default in B for p1 is not the same as default in A: True


3rd part::

    print('=' * 50)
    print('Recreating A with Decorator - name is "kargs" and short alias')


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

    print('-- Instantiating A with no kwargs')
    a = A()

    # Defined params are reachable below the attribute params
    print('Checking if a params are reachable over "kargs"')
    print('a.kargs.p1:', a.kargs.p1)
    print('a.kargs.p2:', a.kargs.p2)

    print('Checking if a params are reachable over shorter alias "k"')
    print(a.k.p1)
    print(a.k.p2)

    # Modification of default values can be checked
    print('Checking if p1 has default value:', a.kargs._isdefault('p1'))

Output::

    ==================================================
    Recreating A with Decorator - name is "kargs" and short alias
    -- Instantiating A with no kwargs
    Checking if a params are reachable over "kargs"
    a.kargs.p1: True
    a.kargs.p2: 99
    Checking if a params are reachable over shorter alias "k"
    True
    99
    Checking if p1 has default value: True


4th part::

    print('=' * 50)
    print('Recreating A with new attr for params - "kargs" and short alias')
    print('USING THE METACLASS')


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
    print('Checking if a params are reachable over "kargs"')
    print('a.kargs.p1:', a.kargs.p1)
    print('a.kargs.p2:', a.kargs.p2)

    print('Checking if a params are reachable over shorter alias "k"')
    print(a.k.p1)
    print(a.k.p2)

    # Modification of default values can be checked
    print('Checking if p1 has default value:', a.kargs._isdefault('p1'))

Output::

    ==================================================
    Recreating A with new attr for params - "kargs" and short alias
    USING THE METACLASS
    Checking if a params are reachable over "kargs"
    a.kargs.p1: True
    a.kargs.p2: 99
    Checking if a params are reachable over shorter alias "k"
    True
    99
    Checking if p1 has default value: True


Final part::

    print('=' * 50)
    print('Recreating A with ParamsBase ... nothing can be changed')

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
    print('a.params.p1:', a.params.p1)
    print('a.params.p2:', a.params.p2)

    # Modification of default values can be checked
    print('Checking if p1 has default value:', a.params._isdefault('p1'))

Output::

    ==================================================
    Recreating A with ParamsBase ... nothing can be changed
    a.params.p1: True
    a.params.p2: 99
    Checking if p1 has default value: True
