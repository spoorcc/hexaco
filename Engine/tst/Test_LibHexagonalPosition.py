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

 Hexagonal Position Library Test Class

########################################################################

"""
import unittest

from Engine.LibHexagonalPosition import *


class TestLibHexPos(unittest.TestCase):  # pylint: disable=R0904
    """Unit test class of Hexagonal Position library"""

    def test_calc_xyz_from_rst_000(self):
        """ Calc the xyz from ring side tile """

        actual = calc_xyz_from_rst(0, 0, 0)
        self.assertTupleEqual((0, 0, 0), tuple(actual))

    def test_get_distance_same(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (0, 0, 0))
        self.assertEqual(distance, 0)

    def test_get_distance_0_0_0__1_m1_0(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (1, -1, 0))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__2_m2_0(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (2, -2, 0))
        self.assertEqual(distance, 2)

    def test_get_distance_0_0_0__m1_1_0(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (-1, 1, 0))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__0_1_m1(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (0, 1, -1))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__0_m1_1(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (0, -1, 1))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__m1_0_1(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (-1, 0, 1))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__1_0_m1(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (1, 0, -1))
        self.assertEqual(distance, 1)

    def test_get_distance_0_0_0__2_m1_m1(self):
        """Measure distance between two known points"""

        distance = get_distance_between((0, 0, 0), (2, -1, -1))
        self.assertEqual(distance, 2)

    ####################################################################

    def test_get_neighbour_topleft_from_xm1y3zm2(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((-1, 3, -2), TOPLEFT)
        self.assertTupleEqual(neighbour_xyz, (0, 2, -2))

    def test_get_neighbour_topleft(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), TOPLEFT)
        self.assertTupleEqual(neighbour_xyz, (1, -1, 0))

    def test_get_neighbour_top(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), TOP)
        self.assertTupleEqual(neighbour_xyz, (1, 0, -1))

    def test_get_neighbour_topright(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), TOPRIGHT)
        self.assertTupleEqual(neighbour_xyz, (0, 1, -1))

    def test_get_neighbour_bottomright(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), BOTTOMRIGHT)
        self.assertTupleEqual(neighbour_xyz, (-1, 1, 0))

    def test_get_neighbour_bottom(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), BOTTOM)
        self.assertTupleEqual(neighbour_xyz, (-1, 0, 1))

    def test_get_neighbour_bottomleft(self):
        """The position is asked for its top neighbour which should be
         returned"""

        neighbour_xyz = get_neighbour_xyz((0, 0, 0), BOTTOMLEFT)
        self.assertTupleEqual( neighbour_xyz, (0, -1, 1))

    ####################################################################

    def test_ring_from_xyz_center(self):
        """ Tests only the ring calculation function for center pos"""

        ring = calc_ring_from_xyz((0, 0, 0))
        self.assertEqual(ring, 0)

    def test_ring_from_xyz_single(self):
        """Tests the ring calculation function with two arguments"""

        ring = calc_ring_from_xyz((-1, 1, 0))
        self.assertEqual(ring, 1)

    def test_ring_from_xyz_multi(self):
        """ Tests only the ring calculation function with
        all three coordinates """

        ring = calc_ring_from_xyz((-3, 4, -1))
        self.assertEqual(ring, 4)

    ####################################################################

    def test_side_from_xyz_center(self):
        """ Tests only the side calculation function for center pos"""

        xyz = (0, 0, 0)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 0)

    def test_side_from_xyz_x1y1zm2(self):
        """ Tests only the side calculation function for known pos"""

        xyz = (1, 1, -2)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 1)

    def test_side_from_xyz_x3ym2zm1(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (3, -2, -1)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 0)

    def test_side_from_xyz_xm3y2z1(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (-3, 2, 1)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 3)

    def test_side_from_xyz_x1y2zm3(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (1, 2, -3)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 1)

    def test_side_from_xyz_xm1ym2z3(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (-1, -2, 3)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 4)

    def test_side_from_xyz_x1ym3z2(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (1, -3, 2)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 5)

    def test_side_from_xyz_xm1y3zm2(self):
        """ Tests only the side clculation function for known pos"""

        xyz = (-1, 3, -2)
        ring = calc_ring_from_xyz(xyz)
        side = calc_side_from_xyz(xyz, ring)
        self.assertEqual(side, 2)

    ####################################################################

    def test_calc_rst_r0s0t0(self):
        """Tests ring/side/tile calculation with center position"""

        xyz = (0, 0, 0)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(0, ring)
        self.assertEqual(0, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s0t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (1, -1, 0)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(0, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s1t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (1, 0, -1)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(1, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s2t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (0, 1, -1)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(2, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s3t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (-1, 1, 0)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(3, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s4t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (-1, 0, 1)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(4, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r1s5t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (0, -1, 1)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(1, ring)
        self.assertEqual(5, side)
        self.assertEqual(0, tile)

    def test_calc_rst_r3s2t1(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (-1, 3, -2)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(3, ring)
        self.assertEqual(2, side)
        self.assertEqual(1, tile)

    def test_calc_rst_r3s2t2(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (-2, 3, -1)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(3, ring)
        self.assertEqual(2, side)
        self.assertEqual(2, tile)

    def test_calc_rst_r3s3t0(self):
        """Test ring/side/tile calculation with a known result """

        xyz = (0, 3, -3)
        (ring, side, tile) = calc_ring_side_tile_from_xyz(xyz)

        self.assertEqual(3, ring)
        self.assertEqual(2, side)
        self.assertEqual(0, tile)

# When this file is called as main, autorun the unittests
if __name__ == '__main__':
    unittest.main(verbosity=1)
