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


from metaparams import metaparams


def test_run(main=False):

    # Testing standard behaviour
    @metaparams()
    class A(object):
        params = (
            ('p1', True),
            ('p2', 99, 'With docstring'),
        )

        def __init__(self):
            pass

    class B(A):
        params = (
            ('p2', 83),
        )

    assert A.params._doc('p1') == A.params._doc('p1')
    assert A.params._doc('p2') == A.params._doc('p2')

    class C(B):
        params = (
            ('p1', False, 'Value changed to False'),
        )

    assert A.params._doc('p1') != C.params._doc('p1')
    print('A.params._doc("p1"):', A.params._doc('p1'))
    print('C.params._doc("p1"):', C.params._doc('p1'))

    assert A.params._doc('p2') == C.params._doc('p2')


if __name__ == '__main__':
    test_run(main=True)
