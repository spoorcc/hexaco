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

 Hexagonal Position library

########################################################################

Description
-----------

Position based on three-axis coordinate system.
Each coordinate sums up to zero.
There are two systems, XYZ and ring, side and tile

 _______      +X      _______/ x1 y1 z-2 \________/ x0 y3 z-3  \________
        \       \    /       \ r2 s1 t1  /        \ r3 s2 t0   /
         \       \  /         \         /          \          /
          \_______\/ x1 y0 z-1 \_______/ x0 y2 z-2  \________/
          /        \ r1 s1 t0  /       \ r2 s2 t0   /        \
         /          \         /         \          /          \
 _______/ x1 y-1 z0  \_______/ x0 y1 z-1 \________/ x-1 y3 z-2 \________
        \ r1 s0  t0  /CENTER \ r1 s2 t0  /        \ r3 s2 t1   /
         \          /         \         /          \          /
x1 y-2 z1 \________/ x0 y0 z0  \_______/_____+Y     \________/
r2 s5 t1  /        \ r0 s0 t0  /       \            /        \
         /          \         /         \          /          \
 _______/ x0 y-1 z1  \_______/ x-1 y1 z0 \________/ x-2 y3 z-1 \________
        \ r1 s5 t0   /       \ r1 s3 t0  /        \ r3 s2 t2   /
         \          /         \         /          \          /
          \________/ x-1 y0 z1 \_______/ x-2 y2 z0  \________/
          /       /\ r1 s4 t0  /       \ r2 s3 t0   /        \
         /       /  \         /         \          /          \
 _______/      +Z    \_______/ x-2 y1 z1 \________/            \________
        \            /       \ r2  s3 t1 /        \            /
"""

from random import random, randint
from Engine.GameSettings import MAPSIZE


TOPLEFT, TOP, TOPRIGHT, BOTTOMRIGHT, BOTTOM, BOTTOMLEFT = range(6)


def calc_xyz_from_rst(ring, side, tile):
    """ Calculates the xyz coordinates from
     the ring side and tile coordinates """

    if ring == 0:
        x_pos = 0
        y_pos = 0
        z_pos = 0
    elif side == 0:
        x_pos = ring
        y_pos = -ring + tile
        z_pos = -tile
    elif side == 1:
        x_pos = ring - tile
        y_pos = tile
        z_pos = -ring
    elif side == 2:
        x_pos = -tile
        y_pos = ring
        z_pos = tile - ring
    elif side == 3:
        x_pos = -ring
        y_pos = ring - tile
        z_pos = tile
    elif side == 4:
        x_pos = -ring + tile
        y_pos = -tile
        z_pos = ring
    else:
        x_pos = tile
        y_pos = -ring
        z_pos = ring - tile

    return (x_pos, y_pos, z_pos)


def get_neighbour_xyz(xyz, direction):
    """Returns the neighbour as mentioned in the direction"""
    pos_x, pos_y, pos_z = xyz

    if direction == TOPLEFT:
        neighbour_xyz = (pos_x+1, pos_y-1, pos_z)
    elif direction == TOP:
        neighbour_xyz = (pos_x+1, pos_y, pos_z-1)
    elif direction == TOPRIGHT:
        neighbour_xyz = (pos_x, pos_y+1, pos_z-1)
    elif direction == BOTTOMRIGHT:
        neighbour_xyz = (pos_x-1, pos_y+1, pos_z)
    elif direction == BOTTOM:
        neighbour_xyz = (pos_x-1, pos_y, pos_z+1)
    elif direction == BOTTOMLEFT:
        neighbour_xyz = (pos_x, pos_y-1, pos_z+1)

    return neighbour_xyz


def get_distance_between(a_xyz, b_xyz):
    """ Returns the distance """

    distance = 0

    d_x = a_xyz[0] - b_xyz[0]
    d_y = a_xyz[1] - b_xyz[1]
    d_z = a_xyz[2] - b_xyz[2]

    if (abs(d_x) > abs(d_y)) and (abs(d_x) > abs(d_z)):
        distance = abs(d_x)
    elif abs(d_y) > abs(d_z):
        distance = abs(d_y)
    else:
        distance = abs(d_z)

    return distance


def calc_ring_from_xyz(xyz):
    """Calculate the highest absolute value to determine
    dominant direction and ring"""

    return max((abs(xyz[0]), abs(xyz[1]), abs(xyz[2])))


    # TODO( Ben ) : Write a full covering test case set
    # TODO( Ben ) : Instead of conditional branches use math
def calc_side_from_xyz(xyz, ring):
    """" Calculates on which side as seen from the center
    @(0,0,0) the position is located
    The calculation is now done by a lot of if-branches but should
    be converted to math, to reduce complexity"""

    temp_pos = xyz
    unknown, pos_x, pos_y, pos_z = range(-1, 3)

    side = TOPLEFT

    # Catch the center tile case
    if xyz[pos_x] == xyz[pos_y] == xyz[pos_z] == 0:
        return side

    #Calculate the lowest value to see which of two sides it is
    index_of_lowest = 0
    index_of_highest = 0
    index_of_equal = unknown
    index_of_abs_equal = unknown
    index_of_abs_highest = 0

    for i in range(3):

        #Check if current value is the lowest
        if temp_pos[i] < temp_pos[index_of_lowest]:
            index_of_lowest = i

        #Check if current value is the highest
        if temp_pos[i] > temp_pos[index_of_highest]:
            index_of_highest = i

        #Check if current value is equal
        # There can only be two equal values
        # Because the sum has to be 0
        # Equal values are always adjacent when seen as continous
        # ring memory so check if next neighbour
        # is equal and store the first index
        if temp_pos[i] == temp_pos[(i+1) % 3]:
            index_of_equal = i

        # Check if current value is absolute equal
        if abs(temp_pos[i]) == abs(temp_pos[(i+1) % 3]):
            index_of_abs_equal = i

        # Check the highest value
        if abs(temp_pos[i]) == ring:
            index_of_abs_highest = i

    #If there are no equal coordinates
    if index_of_equal == index_of_abs_equal == unknown:
        if index_of_abs_highest == pos_x:
            if index_of_highest == pos_x:
                side = TOPLEFT
            else:
                side = BOTTOMRIGHT
        else:
            if index_of_abs_highest == pos_y:
                if index_of_highest == pos_y:
                    side = TOPRIGHT
                else:
                    side = BOTTOMLEFT
            else:
                if index_of_highest == pos_z:
                    side = BOTTOM
                else:
                    side = TOP
    # If there are equal coordinates
    else:

        side = 2 * index_of_abs_equal + 1

        if index_of_equal == unknown:
            side -= 1

        #Flip side if coordinates are negative
        if temp_pos[index_of_abs_equal] < 0:
            side = (side + 3) % 6

    return side


def calc_tile_from_xyz(xyz, ring, side):
    """ Calculates the tile offset as seen from the tile on the same
    ring and same sector"""

    pos_x, pos_y, pos_z = 0, 0, 0

    if side == TOPLEFT:
        pos_x, pos_y = ring, -ring
    elif side == TOP:
        pos_x, pos_z = ring, -ring
    elif side == TOPRIGHT:
        pos_y, pos_z = ring, -ring
    elif side == BOTTOMRIGHT:
        pos_x, pos_y = -ring, ring
    elif side == BOTTOM:
        pos_x, pos_z = -ring, ring
    elif side == BOTTOMLEFT:
        pos_y, pos_z = -ring, ring

    tile = get_distance_between(xyz, (pos_x, pos_y, pos_z))

    return tile


def calc_ring_side_tile_from_xyz(xyz):
    """Calculates the ring, side and tile from XYZ coordinate.
    The position is on a hexagonal grid
    """

    ring = calc_ring_from_xyz(xyz)
    side = calc_side_from_xyz(xyz, ring)
    tile = calc_tile_from_xyz(xyz, ring, side)

    return (ring, side, tile)


def random_coordinate(max_coord=MAPSIZE):
    """ Returns random coordinate within max_coord """
    a = (2.0 * random() - 0.5) * max_coord
    b = (2.0 * random() - 0.5) * max_coord
    c = -(a + b)

    return [a, b, c]


def random_coordinate_center_of_tile(max_coord=MAPSIZE-1):
    """ Returns random coordinate within max_coord that
     is on center of a tile """

    xyz = [0, 0, 0]
    index = randint(0, 2)

    xyz[index] = randint(-max_coord, max_coord)

    max_coord = max_coord - abs(xyz[index])

    xyz[(index + 1) % 3] = randint(-max_coord, max_coord)
    xyz[(index + 2) % 3] = -xyz[index] - xyz[(index + 1) % 3]

    return xyz
