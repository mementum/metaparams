#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2018 Daniel Rodriguez
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
import collections
import textwrap
import sys

from metaframe import MetaFrame, MetaFrameBase

__all__ = ['metaparams', 'MetaParams', 'Params', 'ParamsBase']

# Keyword arguments for class definition (or for the decorator)
KWARG_PNAME = '_pname'  # name the params class will have in the host class
PARAM_NAME = 'params'
_ERROR_NAME = 'Params defined in base class : "{}" - cannot rename to "{}"'
_ERROR_NAMES = 'Multiple base clases with different params definitions: "{}"'

KWARG_PSHORT = '_pshort'  # if a shorthand params -> p  will be set in host
PARAM_SHORT = True

KWARG_PINST = '_pinst'  # if a p.name -> p_name attr will be set in the host
PARAM_INST = False

# Names and default values for the dictionary entry defining each parameter
NAME_VAL = 'value'
VALUE_VAL = None
NAME_REQUIRED = 'required'
VALUE_REQUIRED = False
NAME_DOC = 'doc'
VALUE_DOC = ''
NAME_TYPE = 'type'
VALUE_TYPE = None
NAME_TRANSFORM = 'transform'
VALUE_TRANSFORM = None
NAME_ARGPARSE = 'argparse'
VALUE_ARGPARSE = True

# Default order expected for params when defined using tuples
TUPLE_NAME_ORDER = (NAME_VAL, NAME_REQUIRED, NAME_DOC, NAME_TYPE,
                    NAME_TRANSFORM, NAME_ARGPARSE)

TUPLE_VALUE_ORDER = (VALUE_VAL, VALUE_REQUIRED, VALUE_DOC, VALUE_TYPE,
                     VALUE_TRANSFORM, VALUE_ARGPARSE)

NAME_DOCARGS = 'Args'

PARAMS = {}  # keeps the complete definition or a param
DEFAULTS = {}  # keeps params names and default values
CLS = {}
PSETTING = collections.defaultdict(dict)


class ParamsMeta(type):
    def __new__(meta, name, bases, dct, **kwargs):
        # Normalize the info passed by the parent classes of the host
        pbases = dct.pop('pbases', [{}])

        pdct = {}  # params dictionary for class creation
        for pbase in pbases[:-1]:  # all bases definitions except last (new)
            pbasedct = PARAMS.get(pbase, pbase)  # get params cls if reg'ed

            # Add or update each element. In base clases we have either a dict
            # or a params subclass. Both support the [] operator and iteration
            for k in pbasedct:
                if k in pdct:  # other base(s) have added/update the key before
                    pdct[k].update(pbasedct[k])
                else:
                    pdct[k] = pbasedct[k]  # set it for the 1st element

        nparams = pbases[-1]  # last is new declaration
        if not isinstance(nparams, dict):  # support non-dict declaration
            # (name, val, [doc, [required, [type, [transform, [argparse]]]]])
            # or
            # (name, val, [required, [doc, [type, [transform, [argparse]]]]])
            ndct = {}  # to hold a complete definition in dict form

            # Generate dict entries for each parameter in the tuple definition
            for np in nparams:
                pn, pv, *pothers = np
                ndctpn = {NAME_VAL: pv}
                for nord, vord in zip(TUPLE_NAME_ORDER, TUPLE_VALUE_ORDER):
                    px, *pothers = pothers
                    ndctpn[nord] = px
                    if not pothers:
                        break

                # Support (val, doc, [req ...]) and (val, req, [doc ...])
                try:
                    req_or_doc = ndctpn[NAME_REQUIRED]
                except KeyError:
                    pass  # only value was specified ..
                else:
                    if isinstance(req, str):
                        # Doc was given, swap with required (or default value)
                        ndctpn[NAME_REQUIRED] = ndctpn.get(NAME_DOC,
                                                           VALUE_REQUIRED)
                        ndctpn[NAME_DOC] = req_or_doc

                ndct[pn] = ndctpn  # add parsed tuple definition to larger dict

            nparams = ndct

        else:
            for k, v in nparams.items():  # convert items which are not dicts
                if not isinstance(v, dict):
                    nparams[k] = {NAME_VAL: v}

        # Update the global params dict with the new definition
        for k, v in nparams.items():  # guaranteed to be a dict
            if k in pdct:  # other base(s) have added/update the key before
                pdct[k].update(v)
            else:
                pdct[k] = v  # set it for the 1st eim

        for k, v in pdct.items():
            if False:
                if not isinstance(v, dict):  # shorthand, expand to full syntax
                    v = {NAME_VAL: v}
                else:
                    pass

            v.setdefault(NAME_VAL, VALUE_VAL)

            # Set other defaults (if needed) for extra info attributes
            v.setdefault(NAME_REQUIRED, VALUE_REQUIRED)
            v.setdefault(NAME_DOC, VALUE_DOC)
            v.setdefault(NAME_TYPE, VALUE_TYPE)
            v.setdefault(NAME_TRANSFORM, VALUE_TRANSFORM)
            v.setdefault(NAME_ARGPARSE, VALUE_ARGPARSE)

            pdct[k] = v  # store the complete param definition

        # Now ... auto-document
        ptmpl = ['  - {}:']
        ptmpl += ['(default: {})']
        ptmpl += ['(required: {})']
        ptmpl += ['(type: {})']
        ptmpl += ['(transform: {})']
        ptmpl += ['(argparse: {})']
        ptmpl += ['\n{}']
        ptmpl = ' '.join(ptmpl)

        doc = [NAME_DOCARGS, '\n']
        for k, v in pdct.items():
            vdoc = textwrap.indent(textwrap.fill(v[NAME_DOC]), prefix='    ')
            t = ptmpl.format(
                k,
                v[NAME_VAL],
                v[NAME_REQUIRED],
                v[NAME_TYPE],
                v[NAME_TRANSFORM],
                v[NAME_ARGPARSE],
                vdoc + ('\n' if vdoc else ''))
            doc += [t]

        dct['__doc__'] = '\n'.join(doc)

        # Create an ad-hoc Params subclass with collected values (and defaults)
        # dct contains the definition of methods, etc, ... expand with slots
        dct['__slots__'] = list(pdct.keys())

        # Generate a module_class name for indentification purposes
        cls = super().__new__(meta, name, bases, dct)

        # Register the defaults and the complete dict for the created class
        PARAMS[cls] = pdct  # register the defaults for the class
        # First with Python 3.6 it is possible to use the comprehension
        # DEFAULTS[cls] = OrderedDict(k, v[NAME_VAL] for k, v in pdct.items())
        # And with 3.7
        # DEFAULTS[cls] = {k: v[NAME_VAL] for k, v in pdct.items()}
        # Meanwhile
        DEFAULTS[cls] = defscls = {}
        for k, v in pdct.items():
            defscls[k] = v[NAME_VAL]

        return cls  # return the new subclass

    # These 3 defined here to make them work as class methods of Params
    # subclasses. They MUST not be marked as @classmethod, because they would
    # then become classmethods of the metaclass and not of the class
    def __len__(cls):
        return len(DEFAULTS[cls])

    def __iter__(cls):
        return iter(DEFAULTS[cls])

    def __getitem__(cls, name):
        return DEFAULTS[cls][name]

    def __str__(cls):
        return str(PARAMS[cls])


# Error messages for exceptions raised during instantiation
_ERR_REQ = 'Required parameter "{}" in params "{}" not provided'
_ERR_TYPE = 'Wrong type "{}" for param "{}" / type "{}" in params "{}"'
_ERR_TR = 'Error transforming param "{}" with value "{}" in params "{}"'


class Params(metaclass=ParamsMeta):
    # Intended to generate subclasses dynamically for ParamsBase subclasses
    __slots__ = []  # params are declared once. no other attributes allowed

    # The parameters are expressed as dictionaries. The entries are either
    # key: val
    # or
    # key: dict(), where the keys may be: 'val', 'required', 'doc')
    # default values set to: required=False, val=None, doc=''
    def __init__(self, **kwargs):
        clsname = self.__class__.__name__
        # loop over the defined parameters and the default values
        for name, val in PARAMS[self.__class__].items():
            if name not in kwargs:
                # name is not provided, check if it's a required parameter
                if val[NAME_REQUIRED]:
                    errmsg = _ERR_REQ.format(name, clsname)
                    raise ValueError(errmsg)

                # Not provided, not required, use the default value
                setattr(self, name, val[NAME_VAL])

            else:  # name is provided in kwargs
                v = kwargs[name]
                # See if type check is needed
                t = val[NAME_TYPE]
                if t and not isinstance(v, t):
                    errmsg = _ERR_TYPE.format(type(v), name, t, clsname)
                    raise TypeError(errmsg)

                # Check if transformation is needed and apply it
                tr = val[NAME_TRANSFORM]
                if tr:
                    try:
                        v = tr(v)
                    except Exception as e:
                        errmsg = _ERR_TR.format(name, v, clsname)
                        raise ValueError(errmsg)

                # everything worked out, set the parameter
                setattr(self, name, v)

    def __str__(self):
        return str(self._kwargs())

    @classmethod
    def __iter__(cls):
        return iter(DEFAULTS[cls])

    @classmethod
    def __len__(cls):
        return len(DEFAULTS[cls])

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        setattr(self, key, val)

    @classmethod
    def _remaining(cls, **kwargs):
        '''Returns the keywords arguments which are not consumed by this Params
        class'''
        return {k: v for k, v in kwargs.items() if k not in cls}

    @classmethod
    def _defkwargs(cls):
        '''Returns a dict with the default values of the params'''
        return DEFAULTS[cls].copy()

    @classmethod
    def _defkeys(cls):
        '''Returns the define param names as an iterable'''
        return DEFAULTS[cls].keys()

    @classmethod
    def _defitems(cls):
        '''Returns the names and default values for the params as an iterable
        of pairs'''
        return DEFAULTS[cls].items()

    @classmethod
    def _defvalues(cls):
        '''Returns the default values for the params as an iterable'''
        return DEFAULTS[cls].values()

    @classmethod
    def _defvalue(cls, name):
        '''Returns the default value for the parameter ``name```'''
        return DEFAULTS[cls][name]

    @classmethod
    def _keys(cls):
        '''Returns the parameter names as an iterable'''
        return DEFAULTS[cls].keys()  # keys are unique, unlike values

    def _values(self):
        '''Returns the parameter actual values as an iterable'''
        return (getattr(self, k) for k in self)

    def _value(self, name):
        '''Returns the actual value for parameter ``name``'''
        return getattr(self, name)

    def _items(self):
        '''Returns the names and actual values for the params as an iterable
        of pairs'''
        return ((k, getattr(self, k)) for k in self)

    def _kwargs(self):
        '''Returns a dict with the actual values of the params'''
        return {k: getattr(self, k) for k in self}

    def _isdefault(self, name):
        '''Returns a boolean indicating if param ``name`` has the default
        value'''
        return getattr(self, name) == DEFAULTS[self.__class__][name]

    @classmethod
    def _isrequired(cls, name):
        '''Returns a boolean indicating if param ``name`` is required'''
        return PARAMS[cls][name][NAME_REQUIRED]

    @classmethod
    def _doc(cls, name=None):
        '''Returns the doc string for param ``name`` or the complete docstring
        if no name is given'''
        if not name:
            return cls.__doc__

        return PARAMS[cls][name][NAME_DOC]

    @classmethod
    def _get(cls, name, prop, **kwargs):
        '''A param definition can contain additional key:value entries in the the
        dictionary which are not used by the params machinery.

        The value can be retrieved by calling this method

          - ``name`` - param to query
          - ``prop`` - name of the property entry in the definition
          - ``default`` - Optional, **must be a named argument**

            If provided, ``default`` value will be returned if ``prop`` was
            not in the definition of the parameter ``name``

            If not provided and ``prop`` was not in the param definition a
            ``KeyError`` exception will be raised
        '''
        p = PARAMS[cls][name]
        if 'default' in kwargs:
            return p.get(prop, kwargs['default'])  # if no prop return default

        return p[prop]  # Let it raise exception if not preset

    def _reset(self, name=None):
        '''Reset parameter ``name`` if given, else reset all to the default
        values'''
        if name:
            setattr(self, k, self._defvalue(name))
        else:
            for k, v in self._defitems():
                setattr(self, k, v)

    def _update(self, *args, **kwargs):
        '''Update the current values of the params with

          - dict-like or other params (passed without expansion as *args)
          - **kwargs: keywords arguments
        '''
        # individual args are dict-like or tuples/lists of pairs
        for arg in args:
            try:
                items = dict(**arg)
            except TypeError:  # ** not supported
                items = iter(arg)  # iterable with pairs ((a, b), (c, d)...)
                # Do this to let other exceptions be raised
                while True:
                    try:
                        k, v = next(items)
                    except StopIteration:
                        break

                    setattr(self, k, v)
            else:
                for k, v in items.items():
                    setattr(self, k, v)

        # Now process kwargs (could recurse self._update(kwargs.items()))
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def _argparse(cls, parser, group=None, skip=True, minus=True):
        '''Autogenerate command line switches for an argparse parser.

        If ``group`` is given (``str``), use it to create a group under which
        the switches will be added.

        If ``skip`` is ``True``, parameters with a name with an ending
        ending underscore will be not be added to the command line switches.

        if ``minus`` is ``True``, then ``_`` (underscores) in the param name
        will be replaced with ``-`` (minus) to improve readability.
        '''
        if group:
            parser = parser.add_argument_group(title=group)

        for p in cls:
            if skip and p[-1] == '_':
                continue

            pkwargs = dict(
                help=cls._doc(p),
                required=cls._isrequired(p),
                default=cls._defvalue(p),
            )
            if minus:
                p = p.replace('_', '-')

            parser.add_argument('--' + p, **pkwargs)

    @classmethod
    def _parseargs(cls, args, skip=True):
        '''Use an object ``args`` containing parsed arguments and use the values to
        update the values of the defined parameters

        If ``skip`` is ``True``, parameters with a name with an ending
        ending underscore will be not be sought in ``args``

        **Note**: There is no need to have a ``minus`` parameter as in the
        method ``_argparse``, because the ``Argparse`` object automatically
        replaces ``-`` (minus) with ``_`` (underscore), because the former is
        not a valid character for Python identifiers.
        '''
        updater = {}
        for p in cls:
            if skip and p[-1] == '_':
                continue

            if hasattr(args, p):
                updater[p] = getattr(args, p)

        return updater

    @classmethod
    def _create(cls, args, skip=True):
        '''Use an object ``args`` containing parsed arguments and use the values to
        update the values of the defined parameters

        If ``skip`` is ``True``, parameters with a name with an ending
        ending underscore will be not be sought in ``args``

        **Note**: There is no need to have a ``minus`` parameter as in the
        method ``_argparse``, because the ``Argparse`` object automatically
        replaces ``-`` (minus) with ``_`` (underscore), because the former is
        not a valid character for Python identifiers.
        '''
        hostcls = CLS[cls]
        return hostcls(**cls._parseargs(args, skip=skip))


class MetaParams(MetaFrame):
    '''Metaclass or Paramsbase, which cooperates with gathers information
    during class creation to first dynamically attach subclassess of ``Params``
    and later instantiate it during the instantiation of the own subclasses
    '''

    def __new__(meta, name, bases, dct, **kwargs):
        # In Python >= 3.6, kwargs can be specified for a class definition
        # Else if the decorator is used the dynamic created sub-metaclass will
        # have the above attributes set via a dictionary and kwargs will be
        # empty. Hence the kwargs.get(name, class_attribute) notation which
        # tries first to get it from kwargs and defaults to the class attribute
        # if not found
        bcls = []
        if hasattr(meta, KWARG_PNAME):  # decorator meta for leftmost base
            pname = getattr(meta, KWARG_PNAME)
            pshort = getattr(meta, KWARG_PSHORT)
            pinst = getattr(meta, KWARG_PINST)
        elif bases:
            bcls = [b for b in bases if b in PSETTING]  # get bases with params

            if bcls:  # bases with params exist
                bpnames = [PSETTING[b][KWARG_PNAME] for b in bcls]
                bpset = set(bpnames)
                if len(bpset) > 1:  # more than 1 name defined
                    raise NameError(_ERROR_NAMES.format(','.join(bpnames)))

                # get leftmost base and defined name (there is 1 in the set)
                b, pnamedef = bcls[0], bpset.pop()
            else:
                b, pnamedef = None, PARAM_NAME  # no params base, use defaults

            # Get what would be wished name or default
            pname = kwargs.get(KWARG_PNAME, pnamedef)
            if pname != pnamedef:  # collission from base and kwargs
                raise NameError(_ERROR_NAME.format(pnamedef, pname))

            # Get the defaults from the base class if any or global defs
            # override if the class declaration says something else
            pshortdef = PSETTING[b].get(KWARG_PSHORT, PARAM_SHORT)
            pshort = kwargs.get(KWARG_PSHORT, pshortdef)

            pinstdef = PSETTING[b].get(KWARG_PINST, PARAM_INST)
            pinst = kwargs.get(KWARG_PINST, pinstdef)

        else:  # no bases defined, used provided kwargs or defaults
            pname = kwargs.get(KWARG_PNAME, PARAM_NAME)
            pshort = kwargs.get(KWARG_PSHORT, PARAM_SHORT)
            pinst = kwargs.get(KWARG_PSHORT, PARAM_INST)

        pbases = []  # collect params definitions from bases
        for b in bases:
            bpattr = getattr(b, pname, object)
            try:
                if not issubclass(bpattr, (Params, dict)):
                    continue
            except TypeError:  # bpattr is not a class (also for None Py < 3.6)
                continue

            pbases.append(bpattr)

        pbases.append(dct.get(pname, {}))  # collect new definition

        modname = dct.get('__module__', '').replace('.', '_')
        pclsname = '_'.join((modname, name, pname))
        pcls = type(pclsname, (Params,), {'pbases': pbases})
        dct[pname] = pcls

        # Update documentation
        doc = dct.get('__doc__', None) or ''
        dct['__doc__'] = doc + '\n' + pcls.__doc__  # doc to host

        cls = super().__new__(meta, name, bases, dct)  # create class

        # Keep actual settings in register for new class
        PSETTING[cls][KWARG_PNAME] = pname
        PSETTING[cls][KWARG_PSHORT] = pshort
        PSETTING[cls][KWARG_PINST] = pinst

        CLS[pcls] = cls  # reverse binding to host class

        # pclsname = '_'.join((cls.__module__.replace('.', '_'), name, pname))
        # setattr(cls, pname, pcls)  # install params class as class attribute

        return cls

    def _new_do(cls, *args, **kwargs):
        pname = PSETTING[cls][KWARG_PNAME]
        pshort = PSETTING[cls][KWARG_PSHORT]
        pinst = PSETTING[cls][KWARG_PINST]

        params = getattr(cls, pname)(**kwargs)  # create a params instance

        kwargs = params._remaining(**kwargs)  # get the params not consumed

        # create class instance with the parameters not consumed by params
        self, args, kwargs = super()._new_do(*args, **kwargs)

        setattr(self, pname, params)  # install params instance in instance
        if pshort and len(pname) > 1:  # install shortcut if requested
            # respect leading _
            shortname = pname[0:1 + (pname[0] == '_')]
            setattr(self, shortname, params)

        if pinst and pshort:
            for p, v in params._items():
                setattr(self, '{}_{}'.format(shortname, p), v)

        return self, args, kwargs  # return the expected values


class ParamsBase(metaclass=MetaParams):
    '''Base class to create subclasses which support the params pattern'''
    pass


def metaparams(*args, **kwargs):
    '''Decorator to make a class "Params"-enabled
    Args:
        _pname (def: 'params'):
            Name of the attribute to look for the 2/3 tuples and use to
            set/store the Params subclasses/instances
        _pshort (def: True):
            Install a 1-letter alias of the Params instance (if the original
            name is longer than 1 and respecting a leading underscore if any)
    '''
    # done here to support removing the () call with the args checks below
    # if func defintion had kwargs _pname/_pshort the check would not succeed
    _pname = kwargs.get(KWARG_PNAME, PARAM_NAME)
    _pshort = kwargs.get(KWARG_PSHORT, PARAM_SHORT)
    _pinst = kwargs.get(KWARG_PINST, PARAM_INST)

    def real_decorator(cls):
        # Subclass MetaParamsBase with the passed pname/pshort values
        metadct = {
            KWARG_PNAME: _pname,
            KWARG_PSHORT: _pshort,
            KWARG_PINST: _pinst,
        }
        newmeta = type('xxxxx', (MetaParams,), metadct)
        # Remove any params definition and let it be parsed by the subclass
        pattr = getattr(cls, _pname, {})
        if pattr:
            delattr(cls, _pname)

        # Subclass with the new metaclass from above and the params definition
        newcls = newmeta(cls.__name__, (cls,), {_pname: pattr})
        mod = sys.modules.get(cls.__module__, None)
        if mod is not None:  # install in mod (if possible) to make it pickable
            setattr(mod, cls.__name__, newcls)

        return newcls

    if len(args):  # any non-named arg must be cls and it passed by Python
        return real_decorator(*args)  # no kwargs ... kick real decorator

    return real_decorator  # kwargs present and processed. Let cls be processed
