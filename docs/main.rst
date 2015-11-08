Usage
#####

Params definition
=================

The definition of params can be done as follows::

  class A(object):
      params = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1

But wait ... this is a regular class not yet params-enabled

Decorator enabling
==================

Simply apply the decorator::

  from metaparams import metaparams

  @metaparams
  class A(object):
      params = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1

Et voilá! Of course we still need to make something sensible out of the params::

  a = A(params2=99)

As simple as that. The eager reader will notice the following:

  - ``params2`` is not declared in the list ``kwargs`` for :func:`__init__`

    And so must it be! The ``metaparams`` magic parses and removes the
    ``params2`` kwarg before it ever makes it to :func:`__init__` avoiding an
    error in the calls.

If we know queried the value of the params::

  print(a.params.param2)
  >>> 99

  print(a.params.param1)
  >>> True

Which shows that:

  - ``params1`` retains the default define value ``True``
  - ``params2`` has been changed to the passed kwarg value of ``99``

Of course:

  - ``p1`` which is declared by __init__ as kwarg has been not touched by
    ``metaparams``

.. note::
   Params as seen in the code excerpts above are reachable over the construct
   ``self.params`` which is also the name of the attribute defined during class
   definition.

   It should be obvious that the ``params`` tuple of tuples has been changed
   into an object.

Params syntax
-------------

The params are defined as a tuple of tuples. Of course being this Python it can
be a list of tuples, a tuple of lists and actually any iterable of
iterables. The interior tuples contain the following fields:

  - 1st item: param name
  - 2nd item: param default value
  - 3rd item (optional): param documentation (empty if not provided)

    Inheritance has not yet been visited, but if a param doc is changed
    during inheritance it will take over the original definition of the base class


Using your own ``params`` name
------------------------------

The ``metaparams`` decorator accepts 2 parameters:

  - ``_pname`` (def 'params'): Name of the attribute to look for the 2/3 tuples
    and use to set/store the Params subclasses/instances

  - ``_pshort`` (def: False): Install a 1-letter alias of the Params instance (if
    the original name is longer than 1 and respecting a leading underscore if
    any)

The following can therefore be done::

  from metaparams import metaparams

  @metaparams(_pname='_kargs', _pshort=True)
  class A(object):
      _kargs = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1

Notice how the ``params`` definition uses now the name ``_kargs`` as indicated
in the decorator (else the params would not be recognized).

Instantiating now::

  a = A(param2=99)

  print(a._kargs.param2)
  >>> 99

  print(a._k.param2)
  >>> 99

Mission accomplished:

  - Changed the name by which we can reach the params to ``_kargs``

  - Have a shorter alias (helping hand for PEP-8) ``_k``


Inheritance
-----------

Yes, we can also do that::

  class B(A):
    pass

It has inherited the params, but this would be so boring ... let's redo it::

  class B(A):
      params = (
          ('param2', 99),  # updating the existing param2
          ('newparam', None),
      )

Instantiating and testing::

  b = B()

  print(b._kargs.param2)
  >>> 99
  print(b._kargs.param1)
  >>> True
  print(b._kargs.newparam)
  >>> None


Querying the params
-------------------

One of the usual use cases is finding out if a param still has the default value
or it has been changed. Yes, we can::

  print(self.params._isdefault('params1')
  >>> True

  print(self.params._isdefault('params2')
  >>> False

The ``params`` object contains some other useful functions to retrieve the
names, default values, docs and dictionaries of names/values, names/docs. Check
the reference.

MetaClass-wise
==============

Applying the ``metaparams`` metaclass: ``MetaParams`` as the metaclass of your
classes. It can easily be done with the included classmethod ``as_metaclass``.

Let's metaclass it::

  from metaparams import MetaParams

  class A(MetaParams.as_metaclass(object)):

      params = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1


Just like with the decorator you can use kwargs with ``as_metaclass`` to
customize the parameters::

  from metaparams import MetaParams

  class A(MetaParams.as_metaclass(object, _pname='_kargs', _pshort=True)):

      _kargs = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1

And now even the short alias ``_k`` would be available.


You may directly subclass ``MetaParams`` before applying it to change the name
of the ``params`` atribute::

  from metaparams import MetaParams

  class MyMetaParams(MetaParams):
    _pname = '_kargs'
    _pshort = True

And then apply it to your desired classes.


ParamsBase subclassing
======================

Simply import ``ParamsBase`` and subclass from it::

  from metaparams import ParamsBase

  class A(ParamsBase):
      params = (
          ('param1', True, 'This is param1'),  # including doc
          ('param2', 53,),  # No need for the doc string
      )

      def __init__(self, p1=True):
        self.p1 = p1

In this case you cannot change the name ``params`` or the addition of the
shorter alias.
