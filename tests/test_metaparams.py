#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-18 Daniel Rodriguez
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

from metaparams import ParamsBase, metaparams, MetaParams


py36 = sys.version_info[0:2] >= (3, 6)


def test_run(main=False):

    # Testing standard behaviour
    class A(ParamsBase):
        params = dict(
            p1=True,
            p2=dict(value=99, doc='With docstring'),
        )

    a = A()

    check_p1 = a.params.p1
    check_p1_default = a.params.p1 == a.params._defvalue('p1')
    check_p1_doc = a.params._doc('p1') == ''

    check_p2 = a.params.p2 == 99
    check_p2_default = a.params.p2 == a.params._defvalue('p2')
    check_p2_doc = a.params._doc('p2') == 'With docstring'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc

    # Testing keyword arguments
    if py36:
        class B(metaclass=MetaParams, _pname='xx', _pshort=True):
            xx = dict(
                # a=True,
                p1=True,
                p2=dict(value=99, doc='With docstring'),
            )

            def __init__(self, a1=None):
                pass
    else:
        @metaparams(_pname='xx', _pshort=True)
        class B:
            xx = dict(
                # a=True,
                p1=True,
                p2=dict(value=99, doc='With docstring'),
            )

            def __init__(self, a1=None):
                pass

    b = B(p2=33)

    check_p1 = b.xx.p1
    check_p1_default = b.xx.p1 == b.xx._defvalue('p1')
    check_p1_doc = b.xx._doc('p1') == ''

    check_p2 = b.xx.p2 == 33
    check_p2_default = not b.xx.p2 == b.xx._defvalue('p2')
    check_p2_doc = b.xx._doc('p2') == 'With docstring'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc

    # Testing inheritance
    class C(B):
        xx = dict(
            p1=False,
            p3=dict(value=None, doc='None here'),
            p4=dict(required=True, type=int),
            p5=dict(value='a', transform=lambda x: x.upper()),
        )

    # Testing inheritance
    try:
        c = C()
    except ValueError:
        pass
    except:
        raise

    try:
        c = C(p4=25.0)
    except TypeError:
        pass
    except:
        raise

    c = C(p4=25, p5='c')

    check_p1 = not c.xx.p1  # changed to False
    check_p1_default = c.xx.p1 == c.xx._defvalue('p1')
    check_p1_doc = c.xx._doc('p1') == ''

    check_p2 = c.xx.p2 == 99
    check_p2_default = c.xx.p2 == c.xx._defvalue('p2')
    check_p2_doc = c.xx._doc('p2') == 'With docstring'

    check_p3 = c.xx.p3 is None
    check_p3_default = c.xx.p3 == c.xx._defvalue('p3')
    check_p3_doc = c.xx._doc('p3') == 'None here'

    check_p4_value = c.xx.p4 == 25
    check_p5_value = c.xx.p5 == 'C'

    check_defkwargs = C.xx._defkwargs() == OrderedDict(
        [('p1', False), ('p2', 99), ('p3', None), ('p4', None), ('p5', 'a')]
    )

    check_kwargs = c.xx._kwargs() == {
        'p1': False, 'p2': 99, 'p3': None, 'p4': 25, 'p5': 'C'
    }

    check_p4_required = C.xx._isrequired('p4')
    check_p5_notrequired = not C.xx._isrequired('p5')

    # Need to sort because dict order is not guaranteed in Python < 3.7
    # (guaranteed as implementation detail in CPython 3.6)
    check_items = sorted(list(c.xx._items())) == [
        ('p1', False), ('p2', 99), ('p3', None), ('p4', 25), ('p5', 'C')
    ]

    c.xx._reset()
    check_reset = c.xx._kwargs() == C.xx._defkwargs()
    check_reset_2 = dict(c.xx._items()) == C.xx._defkwargs()
    check_reset_3 = list(c.xx._keys()) == list(C.xx._defkeys())
    check_reset_4 = list(c.xx._values()) == list(C.xx._defvalues())

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc
    assert check_p3
    assert check_p3_default
    assert check_p3_doc
    assert check_p4_value
    assert check_p5_value
    assert check_defkwargs
    assert check_kwargs
    assert check_p4_required
    assert check_p5_notrequired
    assert check_items
    assert check_reset
    assert check_reset_2
    assert check_reset_3
    assert check_reset_4

    # Testing keyword arguments
    if py36:
        class D(ParamsBase, _pshort=False, _pinst=True):
            params = dict(
                p1=True,
            )

    else:
        @metaparams(_pinst=True)
        class D:
            params = dict(
                p1=True,
            )

    d = D()
    assert(d.params.p1)

if __name__ == '__main__':
    test_run(main=True)
