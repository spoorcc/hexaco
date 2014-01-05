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

 Position Component test Class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Class for a position component """

import unittest
from .. import PositionComponent


class TestPositionComponent(unittest.TestCase):
    """ Tests the position component """

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.posComp = PositionComponent(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called before each test case"
        self.posComp.pos.x = 0.0
        self.posComp.pos.y = 0.0
        self.posComp.pos.z = 0.0

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_default_position(self):
        """ Test if default position of position component is in at 0,0,0"""

        self.assertEqual(self.posComp.pos.x, 0.0)
        self.assertEqual(self.posComp.pos.y, 0.0)
        self.assertEqual(self.posComp.pos.z, 0.0)

    def test_default_orientation(self):
        """ Test that default orientation is in 0 direction """

        self.assertEqual(self.posComp.orientation, 0)

    def test_center_of_tile_valid(self):
        """ Test if for valid center of tile position
        the value true is returned """

        self.assertTrue(self.posComp.center_of_tile())

        self.posComp.pos.x = -1.0
        self.posComp.pos.z = 1.0

        self.assertTrue(self.posComp.center_of_tile())

    def test_center_of_tile_invalid(self):
        """ Test if for invalid center of tile position
        the value false is returned """

        self.posComp.pos.x =  0.01
        self.posComp.pos.y = -0.01
        self.assertFalse(self.posComp.center_of_tile())

    def test_center_of_tile_series(self):
        """ Test for large series of center of tiles
        if the expected amount of trues is returned """

        counter = 0

        self.posComp.pos.x = -1.0
        self.posComp.pos.y = 1.0

        for i in range(2555):

            if self.posComp.center_of_tile():
                counter += 1

            self.posComp.pos.x += 0.01
            self.posComp.pos.y -= 0.01

        self.assertEqual(counter, 26)

    def test_is_float_int_using_floats(self):
        """ Test for number of floats if the they are
        correctly considered as ints """

        self.assertTrue(self.posComp.is_float_int(-4.0))
        self.assertTrue(self.posComp.is_float_int(0.0))
        self.assertTrue(self.posComp.is_float_int(1.0))
        self.assertTrue(self.posComp.is_float_int(-1.0))
        self.assertTrue(self.posComp.is_float_int(0.0001))
        self.assertTrue(self.posComp.is_float_int(-0.0009))

    def test_is_float_int_using_non_floats(self):
        """ Test for number of floats if the they are
        correctly considered as non-ints """

        self.assertFalse(self.posComp.is_float_int(0.5))
        self.assertFalse(self.posComp.is_float_int(1.1))
        self.assertFalse(self.posComp.is_float_int(-0.3))
        self.assertFalse(self.posComp.is_float_int(-0.5))

    def test_set_position_xyz(self):
        """ Test if setting the position is propagated to the position """

        self.posComp.set_position_xyz((3, -3, 0))

        self.assertEqual(self.posComp.pos.xyz, (3, -3, 0))

if __name__ == '__main__':
    unittest.main(verbosity=2)
