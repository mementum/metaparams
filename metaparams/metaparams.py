#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


from collections import OrderedDict
import sys

from metaframe import MetaFrame, MetaFrameBase


class Params(object):
    '''Holds a 3-tuple (in the form of 2 OrderedDicts) list of informations to
    define params (name, default, doc), with "doc" optionally being empty.

    During init it receives a reference to the ``kwargs`` (non-expanded to
    enable modification) passed to the class holding it. All params are
    initialized to either the default value or the value passed with the kwargs
    (in which case it is removed from kwargs)

    The class can subclass itself with a new set of params (passed as real
    3-tuples) and other bases (subclasses of Params themselves)

    This class is not meant to be used directly but rather by the metaclass
    MetaParams which installs / subclasses it in a client class and also
    creates an instance

    Attribute setting:
      - Defined params can be set
      - New attributes with a leading underscore can be set

      - Setting other attributes is rejected and raises an AttributeError
    '''

    # Holders of information
    _pdefs = OrderedDict()  # Holds the names / default values pairs of params
    _pdocs = OrderedDict()  # Holds the names / docs pairs of params

    def __init__(self, kwargs):
        # NOTE: No error is kwargs and not **kwargs to modify it
        for pname, pdefault in self._pdefs.items():
            setattr(self, pname, kwargs.pop(pname, pdefault))

    def __setattr__(self, name, value):
        '''Only adds items if defined as params or underscored'''
        if name not in self._pdefs and not name.startswith('_'):
            raise AttributeError

        super(Params, self).__setattr__(name, value)

    def __iter__(self):
        return iter(self._pdefs)

    @classmethod
    def _subclass(cls, clsname, newparams, *otherbases):
        '''Produces a subclass of this class using the given paramerters

        Args:
            cls: the class which is going to be subclassed
            clsname (string): Name of the class holding this Params
            newparams (tuple): 2 or 3 tuples containing the params definitions
            otherbases (Params subclasses): other basec classes to use

        Returns:
            A subclass of this class with the new parameters and including
            those of the other bases
        '''
        # Make a copy of the defaults and docs of this class
        pdefs = cls._pdefs.copy()
        pdocs = cls._pdocs.copy()

        # Add/Update with the infos from other bases
        for otherbase in otherbases:
            pdefs.update(otherbase._pdefs)
            pdocs.update(otherbase._pdocs)

        # Add/Update with the new params
        for np in newparams:
            name, default = np[0:2]
            doc = np[2] if len(np) > 2 else ''

            pdefs[name] = default
            pdocs[name] = doc

        # Dynamically create the new class
        klsname = str(cls.__name__ + '_' + clsname)
        newcls = type(klsname, (cls,), {})

        # Add it to a module (needed for pickling support)
        clsmodule = sys.modules[cls.__module__]
        setattr(clsmodule, klsname, newcls)

        # Set the attributes in the new subclass
        newcls._pdefs = pdefs
        newcls._pdocs = pdocs

        return newcls

    def _isdefault(self, pname):
        '''Returns True if parameter ``pname`` still has the default value'''
        return getattr(self, pname) == self._pdefs[pname]

    def _value(self, pname):
        '''Returns the current value for parameter ``pname``'''
        return getattr(self, pname)

    @classmethod
    def _default(cls, pname):
        '''Returns the default value for parameter ``pname``'''
        return cls._pdefs[pname]

    @classmethod
    def _doc(cls, pname):
        '''Returns the documentation for parameter ``pname``'''
        return cls._pdocs[pname]

    @classmethod
    def _names(cls):
        '''Returns a list with the parameter names'''
        return list(cls._pdefs.keys())

    def _values(self):
        '''Returns a list with the current parameter values'''
        return [getattr(self, x) for x in self._pdefs]

    @classmethod
    def _defaults(cls):
        '''Returns a list with the default parameter values'''
        return list(cls._pdefs.values())

    @classmethod
    def _docs(cls):
        '''Returns a list with the parameter documentations'''
        return list(cls._pdocs.values())

    def _kwvalues(self):
        '''Returns an OrderedDict names/current values pairss'''
        return OrderedDict(map(lambda x: (x, getattr(self, x)), self._pdefs))

    @classmethod
    def _kwdefaults(cls):
        '''Returns an OrderedDict names/default values pairs'''
        return cls._pdefs.copy()

    @classmethod
    def _kwdocs(cls):
        '''Returns an OrderedDict names/doc values pairs'''
        return cls._pdocs.copy()


class MetaParams(MetaFrame):
    '''Intercepts the creation of a client class looking for a specific
    attribute definition (matching name to own attribute ``_pname``) which
    must a be a 2/3-tuple defining the parameters.

    The attribute is removed during class creation and replaced with a subclass
    of Params. All the bases of the client class are scanned and if any other
    also contains the attribute it is passed to the subclassing action.

    Instantiation is also intercepted to give the Params subclass the chance to
    use the ``kwargs`` for initialization and removal of the used names/values.

    During instantiation the Params class in the instance is substituted with
    the Params instance.

    Attributes:
        _pname (def: 'params'):
            Name of the attribute to look for the 2/3 tuples and use to
            set/store the Params subclasses/instances

        _pshort (def: False):
            Install a 1-letter alias of the Params instance (if the original
            name is longer than 1 and respecting a leading underscore if any)
    '''
    _pname = 'params'  # Name of the attribute in the client class
    _pshort = False  # Whether a 1-letter extra-attribute will be added

    @classmethod
    def as_metaclass(meta, *bases, **kwargs):
        '''Create a base class with 'this metaclass' as metaclass

        Meant to be used in the definition of classes for Py2/3 syntax equality

        Args:
            meta: the class itself to be used as metaclass (automatic)
            *bases (iterable): base classes to apply (can be empty)
            *kwargs:
                _pname (def: 'params'):
                    Name of the attribute to look for the 2/3 tuples and use to
                    set/store the Params subclasses/instances

                _pshort (def: False):
                    Install a 1-letter alias of the Params instance (if the
                    original name is longer than 1 and respecting a leading
                    underscore if any)
        '''
        class metaclass(meta):
            def __new__(metaklass, name, this_bases, d):
                mt = meta
                if kwargs:
                    mt = type(str('xxxxx'), (meta,), kwargs)

                return mt(name, bases, d)

        return type.__new__(metaclass, str('tmpcls'), (), {})

    def __new__(meta, name, bases, dct):
        # Remove any params definition from the class dict before creation
        newparams = dct.pop(meta._pname, tuple())

        # Create the new class - this pulls previously defined "params"
        cls = super(MetaParams, meta).__new__(meta, name, bases, dct)

        # Pulls base params class
        baseparams = getattr(cls, cls._pname, Params)

        # get params from extra base classes
        otherbases = [getattr(x, cls._pname)
                      for x in bases[1:] if hasattr(x, cls._pname)]

        # Subclass and store the newly derived params class
        clsparams = baseparams._subclass(name, newparams, *otherbases)
        setattr(cls, cls._pname, clsparams)

        return cls

    def _init_pre(cls, obj, *args, **kwargs):
        pname = cls._pname

        # Create params and set the values from the kwargs
        paramscls = getattr(cls, pname)
        params = paramscls(kwargs)
        setattr(obj, pname, params)

        # Add a 1-letter alias if requested, respecting 1 leading underscore
        # Only if more than 1 letter is available (after the underscore)
        pname_leadunder = pname.startswith('_')
        if cls._pshort and len(pname) > (1 + pname_leadunder):
            setattr(obj, pname[0 + pname_leadunder], params)

        return super(MetaParams, cls)._init_pre(obj, *args, **kwargs)


def metaparams(_pname='params', _pshort=False):
    '''Decorator to make a class "Params"-enabled

    Args:
        _pname (def: 'params'):
            Name of the attribute to look for the 2/3 tuples and use to
            set/store the Params subclasses/instances

        _pshort (def: False):
            Install a 1-letter alias of the Params instance (if the original
            name is longer than 1 and respecting a leading underscore if any)
    '''
    def real_decorator(cls):

        # Subclass MetaParams with the passed pname/pshort values
        metadct = dict(_pname=_pname, _pshort=_pshort)
        newmeta = type(str('xxxxx'), (MetaParams,), metadct)

        # Extract a 'params' definition from the class if any so it can be
        # reparsed later during class creation
        pattr = getattr(cls, _pname, ())
        if pattr:
            delattr(cls, _pname)

        # Subclass with the new metaclass from above and the params definition
        clsdct = {_pname: pattr}
        newcls = newmeta(cls.__name__, (cls,), clsdct)

        return newcls

    return real_decorator


class ParamsBase(MetaParams.as_metaclass()):
    '''
    Base class with ``MetaParams`` already applied to it.

    Subclasses of this will already be params-enabled with the params attribute
    name expected to be ``params`` and no short aias defined.
    '''
    pass


if __name__ == '__main__':

    class A(ParamsBase):
        params = (
            ('juan', 33),
            ('xx', 5),
        )

        def __init__(self, **kwargs):
            print('remaining kwargs', kwargs)

    a = A(xx=52)

    print('kwdefaults', a.xx._kwdefaults())
    print('kwvalues', a.xx._kwvalues())
