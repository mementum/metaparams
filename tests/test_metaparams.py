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

from metaparams import MetaParams


def test_run(main=False):

    # Testing standard behaviour
    class A(MetaParams.as_metaclass(object)):
        params = (
            ('p1', True),
            ('p2', 99, 'With docstring'),
        )

        def __init__(self):
            pass

    a = A()

    check_p1 = a.params.p1
    check_p1_default = a.params.p1 == a.params._default('p1')
    check_p1_doc = a.params._doc('p1') == ''

    check_p2 = a.params.p2 == 99
    check_p2_default = a.params.p2 == a.params._default('p2')
    check_p2_doc = a.params._doc('p2') == 'With docstring'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc

    # Testing keyword arguments
    class B(MetaParams.as_metaclass(_pname='xx', _pshort=True)):

        xx = (
            ('p1', True),
            ('p2', 99, 'With docstring'),
        )

        def __init__(self, a1=None):
            pass

    b = B(p2=33)

    check_p1 = b.xx.p1
    check_p1_default = b.xx.p1 == b.xx._default('p1')
    check_p1_doc = b.xx._doc('p1') == ''

    check_p2 = b.xx.p2 == 33
    check_p2_default = not b.xx.p2 == b.xx._default('p2')
    check_p2_doc = b.xx._doc('p2') == 'With docstring'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc

    # Testing inheritance
    class C(B):

        xx = (
            ('p1', False),
            ('p3', None, 'None here'),
        )

        def __init(self):
            pass

    # Testing inheritance
    c = C()

    check_p1 = not c.xx.p1  # changed to False
    check_p1_default = c.xx.p1 == c.xx._default('p1')
    check_p1_doc = c.xx._doc('p1') == ''

    check_p2 = c.xx.p2 == 99
    check_p2_default = c.xx.p2 == c.xx._default('p2')
    check_p2_doc = c.xx._doc('p2') == 'With docstring'

    check_p3 = c.xx.p3 is None
    check_p3_default = c.xx.p3 == c.xx._default('p3')
    check_p3_doc = c.xx._doc('p3') == 'None here'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc
    assert check_p3
    assert check_p3_default
    assert check_p3_doc


if __name__ == '__main__':
    test_run(main=True)
