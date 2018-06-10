
metaparams
==========

.. image:: https://img.shields.io/pypi/v/metaparams.svg
   :alt: PyPi Version
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
   :target: https://metaparams.readthedocs.io/

.. image:: https://img.shields.io/pypi/pyversions/metaparams.svg
   :alt: Pytghon versions
   :scale: 100%
   :target: https://pypi.python.org/pypi/metaparams/

``metaparams`` is a MetaClass/Class infrastructure to define params
without invoking objects and have them automatically parse/remove the ``kwargs``
passed to the class in which they are intalled

Documentation
=============

Read the full documentation at readthedocs.org:

  - `metaparams documentation <https://metaparams.readthedocs.io/>`_

Python 3 Only
=============

  - Yes it is time to move forward

Installation
============

From pypi::

  pip install metaparams

From source:

  - Place the *metaparams* directory found in the sources inside your project

Features:
=========

  - ``ParamsBase`` a class from which to subclass to also be params-enabled

  - ``MetaParams`` a MetaClass for more complex usage pattern
