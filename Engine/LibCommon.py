"""

    This file is part of HexACO.

    HexACO is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    HexACO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with HexACO.  If not, see <http://www.gnu.org/licenses/>.

########################################################################

Common library

########################################################################

Description
-----------
Module that contains common functionality """

from Engine.GameSettings import MAPSIZE, EPSILON


def highest_in_list(seq):
    """ Calculates the index of the last maximum
        value in an iterable item"""

    max_value = seq[0]
    max_index = 0

    for index, value in enumerate(seq):

        if value > max_value:
            max_value = value
            max_index = index

    return max_index


def is_float_int(number):
    """ Returns a boolean which indicates if a float is an integer"""
    return (abs(float('%.2f' % number)-float('%.f' % number)) < EPSILON)
    #return ( ceil(number) == number or floor(number) == number )
    #return ( self.round_float( number, 3 ) == float( int( number)))


def add_delta_to_pos_if_valid(xyz, deltas, max_coord=MAPSIZE-1.0):
    """ Update position with deltas """

    if sum(deltas) >= EPSILON:
        print "Sum of deltas not equal to zero x:%f y:%f z:%f" % (deltas[0],
                                                                  deltas[1],
                                                                  deltas[2])
        return xyz

    new_xyz = []

    for index, delta in enumerate(deltas):

        new_xyz.append(xyz[index] + delta)

        if abs(new_xyz[index]) >= max_coord - EPSILON:
            raise ValueError("""Trying to walk out of bounds %d :
                                           trying: %f
                                           max: %f""" % (index,
                                                         new_xyz[index],
                                                         max_coord))

    return new_xyz


def negate_list(lst):
    """ Returns the negatet list """

    lst = set(lst)
    return [i for i in lst if -1*i in lst]
