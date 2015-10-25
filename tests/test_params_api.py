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

from metaparams import Params


def test_run(main=False):

    newp = (
        ('p1', True, 'doc'),
        ('p2', 99)
    )

    P = Params._subclass('a', newp)
    p = P(dict())

    assert p.p1
    assert p.p1 == p._value('p1')
    assert p.p1 == p._default('p1')
    assert p._doc('p1') == 'doc'

    assert p.p2 == 99
    assert p.p2 == p._value('p2')
    assert p.p2 == p._default('p2')
    assert p._doc('p2') == ''

    p = P(dict(p2=33))

    assert p.p1
    assert p.p1 == p._value('p1')
    assert p.p1 == p._default('p1')
    assert p._doc('p1') == 'doc'

    assert p.p2 == 33
    assert p.p2 == p._value('p2')
    assert not p.p2 == p._default('p2')
    assert p._doc('p2') == ''

    # Do some inheritance
    newp3 = (
        ('p3', None, 'None here'),
    )

    P3 = Params._subclass('P3', newp3)

    PX = P._subclass('PX', (), P3)
    p = PX(dict())

    assert p.p1
    assert p.p1 == p._value('p1')
    assert p.p1 == p._default('p1')
    assert p._doc('p1') == 'doc'

    assert p.p2 == 99
    assert p.p2 == p._value('p2')
    assert p.p2 == p._default('p2')
    assert p._doc('p2') == ''

    assert p.p3 is None
    assert p.p3 == p._value('p3')
    assert p.p3 == p._default('p3')
    assert p._doc('p3') == 'None here'


if __name__ == '__main__':
    test_run(main=True)
