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

from metaparams import ParamsBase


def test_run(main=False):

    class B(ParamsBase):
        params = (
            ('p1', True),
            ('p2', 99, 'With docstring'),
        )

        def __init__(self, a1=None):
            pass

    b = B(p2=33)

    check_p1 = b.params.p1
    check_p1_default = b.params.p1 == b.params._default('p1')
    check_p1_doc = b.params._doc('p1') == ''

    check_p2 = b.params.p2 == 33
    check_p2_default = not b.params.p2 == b.params._default('p2')
    check_p2_doc = b.params._doc('p2') == 'With docstring'

    assert check_p1
    assert check_p1_default
    assert check_p1_doc
    assert check_p2
    assert check_p2_default
    assert check_p2_doc

    class C(B):

        params = (
            ('p1', False),
            ('p3', None, 'None here'),
        )

    c = C()

    check_p1 = not c.params.p1  # changed to False
    check_p1_default = c.params.p1 == c.params._default('p1')
    check_p1_doc = c.params._doc('p1') == ''

    check_p2 = c.params.p2 == 99
    check_p2_default = c.params.p2 == c.params._default('p2')
    check_p2_doc = c.params._doc('p2') == 'With docstring'

    check_p3 = c.params.p3 is None
    check_p3_default = c.params.p3 == c.params._default('p3')
    check_p3_doc = c.params._doc('p3') == 'None here'

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
