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

 Hexagonal Position Class

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

from Engine.LibHexagonalPosition import *
from Engine.GameSettings import MAPSIZE


class HexagonalPosition(object):
    """A position on the hexagonal field
        Works with three axis coordinate system see source file header
        for in depth description
    """

    def __init__(self, parent):
        """ Default initialization function """
        self.parent = parent
        self.x = 0 # pylint: disable=C0103
        self.y = 0 # pylint: disable=C0103
        self.z = 0 # pylint: disable=C0103

        self.xyz = (0, 0, 0)

        self.ring = 0
        self.side = 0
        self.tile = 0

    ####################################################################

    def set_position_xyz(self, x, y, z, max_coord=MAPSIZE):  # pylint: disable=C0103
        """Sets the position in X Y Z coordinates,
        Updates the ring, side and tile variables
        Returns a boolean if it was a valid position
        """

        # See file header for explanation of coordinate system
        # The sum must be zero to be a valid coordinate
        if((x + y + z) == 0):
            self.x, self.y, self.z = x, y, z  # pylint: disable=C0103
            self.xyz = (x, y, z)
            (self.ring, self.side, self.tile) = \
                calc_ring_side_tile_from_xyz(self.xyz)
            return True
        else:
            return False

    def set_position_rst(self, ring, side, tile):
        """Sets the position in Ring Side Tile coordinates,
        Updates the x, y and z variables
        Returns a boolean if it was a valid position
        """

        if not( type(ring) == type(side) == type(tile) is int):
            return False

        if ring < 0:
            return False

        if ( ring > 0 and tile > ring ):
            return False

        if  side < 0  or side > 5:
            return False

        [self.x, self.y, self.z] = calc_xyz_from_rst( ring, side, tile )
        self.xyz = (self.x, self.y, self.z)
        return True
