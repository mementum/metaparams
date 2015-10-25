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


class MetaFrame(type):
    '''This Metaclass intercepts instance creation/initialization enabling use
    cases like modification of args, kwargs and/or scanning of the object post
    init
    '''

    def _new_pre(cls, *args, **kwargs):
        '''Called before the object is created.

        Params:
          - cls: The class which is going to be instantiated
          - args: To be passed to ``__new__`` for class instantiation
          - kwargs: To be passed to ``__new__`` for class instantiation

        Returns:
          cls, args, kwargs: as a tuple

        The return values need not be the same that were passed
        '''
        return cls, args, kwargs

    def _init_pre(cls, obj, *args, **kwargs):
        '''Called after object creation and before the object is init'ed

        Params:
          - cls: The class which has been instantiated
          - obj: The class instance which has been created
          - args: To be passed to ``__init__`` for object initialization
          - kwargs: To be passed to ``__init__`` for object initialization

        Returns:
          obj, args, kwargs: as a tuple

        The return values need not be the same that were passed
        '''
        return obj, args, kwargs

    def _init_post(cls, obj, *args, **kwargs):
        '''Called after object initialization

        Params:
          - cls: The class which has been instantiated
          - obj: The class instance which has been created
          - args: Which were passed to ``__init__`` for object initialization
          - kwargs: Which were passed to ``__init__`` for object initialization

        Returns:
          obj, args, kwargs: as a tuple

        The return values need not be the same that were passed. But modifying
        ``args`` and/or ``kwargs`` no longer plays a role because the object
        has already been created and initialized
        '''
        return obj, args, kwargs

    def __call__(cls, *args, **kwargs):
        '''Creates an initializes an instance of cls calling the pre-new,
        pre-init/post-init hooks with the passed/returned ``args`` / ``kwargs``
        '''
        # Before __new__ (object not yet created)
        cls, args, kwargs = cls._new_pre(*args, **kwargs)

        # Create the object
        obj = cls.__new__(cls, *args, **kwargs)

        # Before __init__
        obj, args, kwargs = cls._init_pre(obj, *args, **kwargs)

        # Init the object
        obj.__init__(*args, **kwargs)

        # After __init__
        obj, args, kwargs = cls._init_post(obj, *args, **kwargs)

        # Return the created & init'ed object
        return obj

    # This is from Armin Ronacher from Flask simplified later by six
    @staticmethod
    def with_metaclass(meta, *bases):
        """Create a base class with a metaclass."""
        # This requires a bit of explanation: the basic idea is to make a dummy
        # metaclass for one level of class instantiation that replaces itself
        # with the actual metaclass.
        class metaclass(meta):

            def __new__(cls, name, this_bases, d):
                return meta(name, bases, d)
        return type.__new__(metaclass, str('tmpcls'), (), {})


class MetaFrameBase(MetaFrame.with_metaclass(MetaFrame, object)):
    '''Enables inheritance without having to specify/declare a metaclass'''
    pass
