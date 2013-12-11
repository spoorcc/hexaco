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

 Hexagonal Position Test Class

########################################################################

"""
import unittest
from ..HexagonalPosition import HexagonalPosition

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

    def test_set_position_rst_cent_pos(self):
        """Test if center position can be set"""

        result = self.pos.set_position_rst( 0, 0, 0)

        self.assertTrue( result )

        self.assertEqual( self.pos.x, 0)
        self.assertEqual( self.pos.y, 0)
        self.assertEqual( self.pos.z, 0)

    def test_set_position_rst_invalid_ring(self):
        """Test if invalid ring value is not accepted"""

        result = self.pos.set_position_rst( -1, 0, 0)

        self.assertFalse( result )

        self.assertEqual( self.pos.x, 0)
        self.assertEqual( self.pos.y, 0)
        self.assertEqual( self.pos.z, 0)

    def test_set_position_rst_invalid_side(self):
        """Test if invalid side value is not accepted"""

        result = self.pos.set_position_rst( 0, 7, 0)

        self.assertFalse( result )

        self.assertEqual( self.pos.x, 0)
        self.assertEqual( self.pos.y, 0)
        self.assertEqual( self.pos.z, 0)

    def test_set_position_rst_invalid_tile(self):
        """Test if invalid tile value is not accepted"""

        result = self.pos.set_position_rst( 1, 2, 3)

        self.assertFalse( result )

        self.assertEqual( self.pos.x, 0)
        self.assertEqual( self.pos.y, 0)
        self.assertEqual( self.pos.z, 0)

    def test_calc_xyz_from_rst_r1s0t0(self):
        """Test if ring 1 side 0 tile 0 results in x1 y-1 z0"""

        [x, y, z] = self.pos.calc_xyz_from_rst( 1, 0, 0) # pylint: disable=C0103

        self.assertEqual( x,  1)
        self.assertEqual( y, -1)
        self.assertEqual( z,  0)

    def test_calc_xyz_from_rst_r3s2t1(self):
        """Test if ring 3 side 2 tile 1 results in x-1 y3 z-2"""

        [x, y, z] = self.pos.calc_xyz_from_rst( 3, 2, 1) # pylint: disable=C0103

        self.assertEqual( x, -1)
        self.assertEqual( y,  3)
        self.assertEqual( z, -2)    

    ####################################################################

    def test_get_distance_same(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, 0, 0 )

        self.assertEqual( distance, 0)

    def test_get_distance_0_0_0__1_m1_0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 1, -1, 0 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__2_m2_0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 2, -2, 0 )

        self.assertEqual( distance, 2)

    def test_get_distance_0_0_0__m1_1_0(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( -1, 1, 0 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__0_1_m1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, 1, -1 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__0_m1_1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 0, -1, 1 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__m1_0_1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( -1, 0, 1 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__1_0_m1(self):
        """Measure distance between two known points"""

        self.pos.set_position_xyz(0, 0, 0 )
        distance = self.pos.get_distance_to( 1, 0, -1 )

        self.assertEqual( distance, 1)

    def test_get_distance_0_0_0__2_m1_m1(self):
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
