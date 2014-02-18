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

Polygon library

########################################################################

Description
-----------
Module that returns geometrical shapes """

from math import sin, cos, radians


def create_triangle(size):
    """ Returns a triangle """

    polygon = [0, -size,
               size, size,
               -size, size]

    return polygon


def give_point_on_circle(degrees, radius):
    """ Returns the x,y coordinates of a point on a circle with its center
    at 0,0 and with the given radius """
    return [radius * cos(radians(degrees)), radius * sin(radians(degrees))]


def create_hexagon(radius):
    """ Returns the coordinates of a hexagon where the furthest points lay
    on a circle with its center at 0,0 and with the given radius.
    The coordinates are formatted as [ x0, y0, x1, y1, ... xN, yN ]"""

    coordinates = []
    for i in range(0, 6):
        coordinates += give_point_on_circle(i * 60, radius)

    return coordinates


def create_octagon(radius):
    """ Returns the coordinates of an octagon where the furthest points lay
    on a circle with its center at 0,0 and with the given radius.
    The coordinates are formatted as [ x0, y0, x1, y1, ... xN, yN ]"""

    coordinates = []
    for i in range(0, 8):
        coordinates += give_point_on_circle(i * 45, radius)

    return coordinates
