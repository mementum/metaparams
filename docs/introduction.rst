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


Quick Start
===========

Any class can be quickly metaparams-enabled. For example::

    from metaparams import MetaParams


    class A(MetaParams.as_metaclass()):
        params = (
	    ('p1', True),
	    ('p2', 88, 'with doc')
	)

The :func:`as_metaclass` from ``MetaParams`` is compatible with Python 2
and 3. Notice that class ``A`` has no :func:`__init__`` method. Yet the params
will be initialized::

    a = A(p2=93)

The magic has happened in the background:

  - Param ``p2`` will be initialized to ``93`` as specified in the ``kwargs``

  - Param ``p1`` will be initialized to its default value of ``True``

To check it we can add::

    assert a.params.p1 is True
    assert a.params.p2 == 93

Notice the following important trait:

  - params are reachable in a consolidated manner over a ``params`` attribute of
    ``a``

This deserves an explanation:

  - ``class A`` has been declared with ``params`` taking the form of a tuple of
    tuples

  - In the background ``class A`` has replaced the tuple of tuples with a
    ``metaparams.Params`` class definition using the params declarations

  - When ``class A`` is instantiated as ``a`` so is the ``params`` class also
    instantiated.

The replacement and instantiation can be checked with a simple ``print``::

    print(A.params)
    >>> <class 'metaparams.metaparams.Params_A'>

    print(a.params)
    >>> <metaparams.metaparams.Params_A object at 0x0000000002649358>
