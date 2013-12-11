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

import unittest

class HexagonalPosition(object):
    """A position on the hexagonal field
        Works with three axis coordinate system see source file header
        for in depth description
    """

    TOPLEFT, TOP, TOPRIGHT, BOTTOMRIGHT, BOTTOM, BOTTOMLEFT = range(6)

    def __init__(self, parent):
        """ Default initialization function """
        self.parent = parent
        self.x = 0 # pylint: disable=C0103
        self.y = 0 # pylint: disable=C0103
        self.z = 0 # pylint: disable=C0103

        self.ring = 0
        self.side = 0
        self.tile = 0

    ####################################################################

    def set_position_xyz(self, x, y, z): # pylint: disable=C0103
        """Sets the position in X Y Z coordinates,
        Updates the ring, side and tile variables
        Returns a boolean if it was a valid position
        """

        if not( type(x) == type(y) == type(z) is int):
            return False

        # See file header for explanation of coordinate system
        # The sum must be zero to be a valid coordinate
        if( (x + y + z) == 0):
            self.x, self.y, self.z = x, y, z # pylint: disable=C0103
            self.calc_ring_side_tile()
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

        [self.x, self.y, self.z] = self.calc_xyz_from_rst( ring, side, tile )
        return True    

    def calc_xyz_from_rst( self, ring, side, tile ):

        if ring == 0:
            x = 0
            y = 0
            z = 0
        elif side == 0:
            x =  ring
            y = -ring + tile
            z =  -tile
        elif side == 1:
            x =  ring - tile
            y =  tile
            z = -ring
        elif side == 2:
            x =  -tile
            y =  ring
            z =  tile - ring
        elif side == 3:
            x = -ring
            y =  ring - tile
            z =  tile
        elif side == 4:
            x = -ring + tile
            y =  -tile
            z =  ring            
        else:
            x =  tile
            y = -ring
            z =  ring - tile

        return [x, y, z]

    def get_neighbour(self, direction):
        """Returns the neighbour as mentioned in the direction"""
        neighbour = HexagonalPosition(self.parent)

        if direction == self.TOPLEFT:
            neighbour.set_position_xyz( self.x+1, self.y-1, self.z)
        elif direction == self.TOP:
            neighbour.set_position_xyz( self.x+1, self.y, self.z-1)
        elif direction == self.TOPRIGHT:
            neighbour.set_position_xyz( self.x, self.y+1, self.z-1)
        elif direction == self.BOTTOMRIGHT:
            neighbour.set_position_xyz( self.x-1, self.y+1, self.z)
        elif direction == self.BOTTOM:
            neighbour.set_position_xyz( self.x-1, self.y, self.z+1)
        elif direction == self.BOTTOMLEFT:
            neighbour.set_position_xyz( self.x, self.y-1, self.z+1)

        return neighbour

    # TODO( Ben ) : Add type checking
    def get_distance_to(self, x, y, z): # pylint: disable=C0103
        """ Returns the distance """

        distance = 0

        d_x = x - self.x
        d_y = y - self.y
        d_z = z - self.z

        if ( abs(d_x) > abs(d_y)) and (abs(d_x) > abs(d_z)):
            distance = abs(d_x)
        else:

            if abs(d_y) > abs(d_z):
                distance = abs(d_y)
            else:
                distance = abs(d_z)

        return distance

    def calc_ring_from_xyz(self):

        """Calculate the highest absolute value to determine
        dominant direction and ring"""
        self.ring = max( (abs(self.x), abs(self.y), abs(self.z)) )

    # TODO( Ben ) : Write a full covering test case set
    # TODO( Ben ) : Instead of conditional branches use math
    def calc_side_from_xyz(self):
        """" Calculates on which side as seen from the center
        @(0,0,0) the position is located
        The calculation is now done by a lot of if-branches but should
        be converted to math, to reduce complexity"""

        temp_pos = (self.x, self.y, self.z)
        unknown, x, y, z = range(-1, 3) # pylint: disable=C0103

        # Catch the center tile case
        if self.x == self.y == self.z == 0 :
            self.side = self.TOPLEFT
            return

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
            if temp_pos[i] == temp_pos[(i+1)%3] :
                index_of_equal = i

            # Check if current value is absolute equal
            if abs(temp_pos[i]) == abs(temp_pos[(i+1)%3]):
                index_of_abs_equal = i

            # Check the highest value
            if abs(temp_pos[i]) == self.ring:
                index_of_abs_highest = i

        #If there are no equal coordinates
        if index_of_equal == index_of_abs_equal == unknown:
            if index_of_abs_highest == x:
                if index_of_highest == x:
                    side = self.TOPLEFT
                else:
                    side = self.BOTTOMRIGHT
            else:
                if index_of_abs_highest == y:
                    if index_of_highest == y:
                        side = self.TOPRIGHT
                    else:
                        side = self.BOTTOMLEFT
                else:
                    if index_of_highest == z:
                        side = self.BOTTOM
                    else:
                        side = self.TOP
        # If there are equal coordinates
        else:

            side = 2 * index_of_abs_equal + 1

            if index_of_equal == unknown:
                side -= 1

            #Flip side if coordinates are negative
            if temp_pos[index_of_abs_equal] < 0:
                side = (side + 3)%6

        self.side = side

    def calc_tile_from_xyz(self):
        """ Calculates the tile offset as seen from the tile on the same
        ring and same sector"""

        x, y, z = 0, 0, 0 # pylint: disable=C0103

        if self.side == self.TOPLEFT:
            x, y = self.ring, -self.ring # pylint: disable=C0103
        elif self.side == self.TOP:
            x, z = self.ring, -self.ring # pylint: disable=C0103
        elif self.side == self.TOPRIGHT:
            y, z = self.ring, -self.ring # pylint: disable=C0103
        elif self.side ==  self.BOTTOMRIGHT:
            x, y = -self.ring, self.ring # pylint: disable=C0103
        elif self.side == self.BOTTOM:
            x, z = -self.ring, self.ring # pylint: disable=C0103
        elif self.side == self.BOTTOMLEFT:
            y, z = -self.ring, self.ring # pylint: disable=C0103

        self.tile = self.get_distance_to(x, y, z)

    def calc_ring_side_tile( self): # pylint: disable=C0103
        """Calculates the ring, side and tile from XYZ coordinate.
        The position is on a hexagonal grid

        """

        self.calc_ring_from_xyz()
        self.calc_side_from_xyz()
        self.calc_tile_from_xyz()

        return (self.ring, self.side, self.tile)
