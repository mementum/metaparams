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

    # Check list retrieval api
    p = PX(dict(p2=88))

    names = p._names()
    assert len(names) == 3
    assert names[0] == 'p1'
    assert names[1] == 'p2'
    assert names[2] == 'p3'

    values = p._values()
    assert len(values) == 3
    assert values[0] == p.p1
    assert values[1] == p.p2
    assert values[2] == p.p3

    values = p._values('p2', 'p3')
    assert len(values) == 2
    assert values[0] == p.p2
    assert values[1] == p.p3

    defs = p._defaults()
    assert len(defs) == 3
    assert defs[0] == p._default('p1')
    assert defs[1] == p._default('p2')
    assert defs[2] == p._default('p3')

    defs = p._defaults('p2', 'p3')
    assert len(defs) == 2
    assert defs[0] == p._default('p2')
    assert defs[1] == p._default('p3')

    docs = p._docs()
    assert len(docs) == 3
    assert docs[0] == p._doc('p1')
    assert docs[1] == p._doc('p2')
    assert docs[2] == p._doc('p3')

    docs = p._docs('p2', 'p3')
    assert len(docs) == 2
    assert docs[0] == p._doc('p2')
    assert docs[1] == p._doc('p3')

    # Check kw retrieval api
    kwvalues = p._kwvalues()
    assert len(kwvalues) == 3
    kvalues = [(x, getattr(p, x)) for x in p._names()]
    assert list(kwvalues.items()) == kvalues

    kwvalues = p._kwvalues('p2', 'p3')
    assert len(kwvalues) == 2
    kvalues = [(x, getattr(p, x)) for x in p._names()[1:]]
    assert list(kwvalues.items()) == kvalues

    kwdefaults = p._kwdefaults()
    assert len(kwdefaults) == 3
    kdefaults = [(x, p._default(x)) for x in p._names()]
    assert list(kwdefaults.items()) == kdefaults

    kwdefaults = p._kwdefaults('p2', 'p3')
    assert len(kwdefaults) == 2
    kdefaults = [(x, p._default(x)) for x in p._names()[1:]]
    assert list(kwdefaults.items()) == kdefaults

    kwdocs = p._kwdocs()
    assert len(kwdocs) == 3
    kdocs = [(x, p._doc(x)) for x in p._names()]
    assert list(kwdocs.items()) == kdocs

    kwdocs = p._kwdocs('p2', 'p3')
    assert len(kwdocs) == 2
    kdocs = [(x, p._doc(x)) for x in p._names()[1:]]
    assert list(kwdocs.items()) == kdocs


if __name__ == '__main__':
    test_run(main=True)
