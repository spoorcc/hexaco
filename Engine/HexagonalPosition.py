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
 including Unit test class

 * Run file separate to run unit tests

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
          \________/ x0 y0 z0  \_______/_____+Y     \________/
          /        \ r0 s0 t0  /       \            /        \
         /          \         /         \          /          \
 _______/ x0 y-1 z1  \_______/ x-1 y1 z0 \________/ x-2 y3 z-1 \________
        \ r1 s5 t0   /       \ r1 s3 t0  /        \ r3 s2 t2   /
         \          /         \         /          \          /
          \________/ x-1 y0 z1 \_______/ x-2 y2 z0  \________/
          /       /\ r1 s4 t0  /       \ r2 s3 t0   /        \
         /       /  \         /         \          /          \
 _______/      +Z    \_______/           \________/            \________
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

###################################################################
#
# Test Code
#
###################################################################

class TestHexPos(unittest.TestCase): # pylint: disable=R0904
    """Unit test class of Hexagonal Position"""

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.pos = HexagonalPosition(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"

        self.pos.x, self.pos.y, self.pos.z = 0, 0, 0 # pylint: disable=C0103

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_set_position_xyz_cent_pos(self):
        """Tests if center position can be set"""

        result = self.pos.set_position_xyz( 0, 0, 0)

        self.assertEqual( self.pos.x, 0 )
        self.assertEqual( self.pos.y, 0 )
        self.assertEqual( self.pos.z, 0 )

        self.assertTrue( result )

    def test_set_position_xyz_valid_pos(self):
        """Tests if some position can be set"""

        result = self.pos.set_position_xyz( -2, 3, -1)

        self.assertEqual( self.pos.x, -2 )
        self.assertEqual( self.pos.y, 3 )
        self.assertEqual( self.pos.z, -1 )

        self.assertTrue( result )

    def test_set_position_xyz_inv_pos(self):
        """Tests if invalid position will result in no change"""

        result = self.pos.set_position_xyz( -1, 0, 0)

        self.assertEqual( self.pos.x, 0 )
        self.assertEqual( self.pos.y, 0 )
        self.assertEqual( self.pos.z, 0 )

        self.assertFalse( result )

    # Pylint warns about a to long name but it is needed to keep it
    # a logical name and it is mearily a test case
    def test_set_position_xyz_mult_inv_args(self): # pylint: disable=C0103
        """Tests if invalid position arguments will result in no change"""

        result = self.pos.set_position_xyz( "This",  "is", " wrong" )

        self.assertFalse( result )

        self.assertEqual( self.pos.x, 0 )
        self.assertEqual( self.pos.y, 0 )
        self.assertEqual( self.pos.z, 0 )

    def test_set_position_xyz_inv_arg(self):
        """Tests if single invalid position argument will result in no change"""

        result = self.pos.set_position_xyz( 0,  0, " wrong" )

        self.assertFalse( result )

        self.assertEqual( self.pos.x, 0 )
        self.assertEqual( self.pos.y, 0 )
        self.assertEqual( self.pos.z, 0 )

    ####################################################################

    def test_get_distance_same(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, 0, 0 )

        self.assertEqual( distance, 0)

    def test_get_distance_x0y0z0_x1ym1z0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 1, -1, 0 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_x2ym2z0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 2, -2, 0 )

        self.assertEqual( distance, 2)

    def test_get_distance_x0y0z0_xm1y1z0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( -1, 1, 0 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_x0y1zm1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, 1, -1 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_x0ym1z1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, -1, 1 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_xm1y0z1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( -1, 0, 1 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_x1y0zm1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 1, 0, -1 )

        self.assertEqual( distance, 1)

    def test_get_distance_x0y0z0_x2ym1zm1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 2, -1, -1 )

        self.assertEqual( distance, 2)

    ####################################################################

    def test_get_neighbour_topleft_from_xm1y3zm2(self):
        """The position is asked for its top neighbour which should be
         returned"""

        self.pos.set_position_xyz(-1, 3, -2 )
        neighbour = self.pos.get_neighbour( HexagonalPosition.TOPLEFT )

        self.assertEqual( neighbour.x, 0)
        self.assertEqual( neighbour.y, 2)
        self.assertEqual( neighbour.z, -2)

    def test_get_neighbour_topleft(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.TOPLEFT )

        self.assertEqual( neighbour.x, 1)
        self.assertEqual( neighbour.y, -1)
        self.assertEqual( neighbour.z, 0)

    def test_get_neighbour_top(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.TOP )

        self.assertEqual( neighbour.x, 1)
        self.assertEqual( neighbour.y, 0)
        self.assertEqual( neighbour.z, -1)

    def test_get_neighbour_topright(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.TOPRIGHT )

        self.assertEqual( neighbour.x, 0)
        self.assertEqual( neighbour.y, 1)
        self.assertEqual( neighbour.z, -1)

    def test_get_neighbour_bottomright(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.BOTTOMRIGHT )

        self.assertEqual( neighbour.x, -1)
        self.assertEqual( neighbour.y, 1)
        self.assertEqual( neighbour.z, 0)

    def test_get_neighbour_bottom(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.BOTTOM )

        self.assertEqual( neighbour.x, -1)
        self.assertEqual( neighbour.y, 0)
        self.assertEqual( neighbour.z, 1)

    def test_get_neighbour_bottomleft(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour = self.pos.get_neighbour( HexagonalPosition.BOTTOMLEFT )

        self.assertEqual( neighbour.x, 0)
        self.assertEqual( neighbour.y, -1)
        self.assertEqual( neighbour.z, 1)

    ####################################################################

    def test_ring_from_xyz_center(self):
        """ Tests only the ring calculation function for center pos"""

        self.pos.set_position_xyz(0, 0, 0)
        self.assertEqual( self.pos.ring, 0)

    def test_ring_from_xyz_single(self):
        """Tests the ring calculation function with two arguments"""

        self.pos.set_position_xyz(-1, 1, 0)
        self.assertEqual( self.pos.ring, 1)

    def test_ring_from_xyz_multi(self):
        """ Tests only the ring calculation function with
        all three coordinates """

        self.pos.set_position_xyz(-3, 4, -1)
        self.assertEqual( self.pos.ring, 4)

    ####################################################################

    def test_side_from_xyz_center(self):
        """ Tests only the side calculation function for center pos"""

        self.pos.set_position_xyz(0, 0, 0)
        self.assertEqual( self.pos.side, 0)

    def test_side_from_xyz_x1y1zm2(self):
        """ Tests only the side calculation function for known pos"""

        self.pos.set_position_xyz(1, 1, -2)
        self.assertEqual( self.pos.side, 1)

    def test_side_from_xyz_x3ym2zm1(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(3, -2, -1)
        self.assertEqual( self.pos.side, 0)

    def test_side_from_xyz_xm3y2z1(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(-3, 2, 1)
        self.assertEqual( self.pos.side, 3)

    def test_side_from_xyz_x1y2zm3(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(1, 2, -3)
        self.assertEqual( self.pos.side, 1)

    def test_side_from_xyz_xm1ym2z3(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(-1, -2, 3)
        self.assertEqual( self.pos.side, 4)

    def test_side_from_xyz_x1ym3z2(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(1, -3, 2)
        self.assertEqual( self.pos.side, 5)

    def test_side_from_xyz_xm1y3zm2(self):
        """ Tests only the side clculation function for known pos"""

        self.pos.set_position_xyz(-1, 3, -2)
        self.assertEqual( self.pos.side, 2)

    ####################################################################

    def test_calc_rst_r0s0t0(self):
        """Tests ring/side/tile calculation with center position"""

        self.pos.set_position_xyz(0, 0, 0)

        self.assertEqual( 0, self.pos.ring )
        self.assertEqual( 0, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s0t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(1, -1, 0)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 0, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s1t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(1, 0, -1)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 1, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s2t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(0, 1, -1)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 2, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s3t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(-1, 1, 0)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 3, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s4t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(-1, 0, 1)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 4, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r1s5t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(0, -1, 1)

        self.assertEqual( 1, self.pos.ring )
        self.assertEqual( 5, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

    def test_calc_rst_r3s2t1(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(-1, 3, -2)

        self.assertEqual( 3, self.pos.ring )
        self.assertEqual( 2, self.pos.side )
        self.assertEqual( 1, self.pos.tile )

    def test_calc_rst_r3s2t2(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(-2, 3, -1)

        self.assertEqual( 3, self.pos.ring )
        self.assertEqual( 2, self.pos.side )
        self.assertEqual( 2, self.pos.tile )


    def test_calc_rst_r3s3t0(self):
        """Test ring/side/tile calculation with a known result """

        self.pos.set_position_xyz(0, 3, -3)

        self.assertEqual( 3, self.pos.ring )
        self.assertEqual( 2, self.pos.side )
        self.assertEqual( 0, self.pos.tile )

# When this file is called as main, autorun the unittests
if __name__ == '__main__':
    unittest.main(verbosity=1)
