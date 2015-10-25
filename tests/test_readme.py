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


from metaparams import metaparams, MetaParams, ParamsBase


@metaparams()
class A(object):

    params = (
        ('p1', True, 'doc'),
        ('p2', 99),
    )

    def __init__(self):
        pass

a = A()

# Defined params are reachable below the attribute params
print(a.params.p1)
print(a.params.p2)

# Modification of default values can be checked
assert a.params._isdefault('p1')

# Inheriting with modification an extension
class B(A):

    params = (
        ('p1', False,),  # changed default value of p1
        ('p3', None),  # new parameter
    )

    def __init__(self):
        pass

b = B()

# Defined params are reachable below the attribute params
print(b.params.p1)
print(b.params.p2)
print(b.params.p3)

# Modification of default values can be checked
assert b.params._isdefault('p1')

# Over the class we can also check defaults
# B has different default value for p1 than A
assert b.params.p1 != A.params._default('p1')


# The name of the attribute 'params' can be changed
# and a shorter alias (PEP-8 ...) added
@metaparams(_pname='kargs', _pshort=True)
class A(object):

    kargs = (
        ('p1', True, 'doc'),
        ('p2', 99),
    )

    def __init__(self):
        pass

a = A()

# Defined params are reachable below the attribute params
print(a.kargs.p1)
print(a.kargs.p2)

print(a.k.p1)
print(a.k.p2)

# Modification of default values can be checked
assert a.kargs._isdefault('p1')


# The metaclass works also so ... but it's a metaclass

class A(MetaParams.as_metaclass(_pname='kargs', _pshort=True)):

    kargs = (
        ('p1', True, 'doc'),
        ('p2', 99),
    )

    def __init__(self):
        pass

a = A()

# Defined params are reachable below the attribute params
print(a.kargs.p1)
print(a.kargs.p2)

print(a.k.p1)
print(a.k.p2)

# Modification of default values can be checked
assert a.kargs._isdefault('p1')


# And finally an already cooked base class with no customization
class A(ParamsBase):

    params = (
        ('p1', True, 'doc'),
        ('p2', 99),
    )

    def __init__(self):
        pass

a = A()

# Defined params are reachable below the attribute params
print(a.params.p1)
print(a.params.p2)

# Modification of default values can be checked
assert a.params._isdefault('p1')
