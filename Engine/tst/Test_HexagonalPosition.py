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


class TestHexPos(unittest.TestCase):  # pylint: disable=R0904
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

        self.pos.set_position_xyz(0, 0, 0)

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_set_position_xyz_cent_pos(self):
        """Tests if center position can be set"""

        result = self.pos.set_position_xyz(0, 0, 0)

        self.assertEqual(self.pos.x, 0)
        self.assertEqual(self.pos.y, 0)
        self.assertEqual(self.pos.z, 0)

        self.assertTrue(result)

    def test_set_position_xyz_valid_pos(self):
        """Tests if some position can be set"""

        result = self.pos.set_position_xyz(-2, 3, -1)

        self.assertEqual(self.pos.x, -2.0)
        self.assertEqual(self.pos.y, 3.0)
        self.assertEqual(self.pos.z, -1.0)

        self.assertTrue(result)

    def test_set_position_xyz_inv_pos(self):
        """Tests if invalid position will result in no change"""

        result = self.pos.set_position_xyz(-1, 0, 0, 1e-3)

        self.assertEqual(self.pos.x, 0.0)
        self.assertEqual(self.pos.y, 0.0)
        self.assertEqual(self.pos.z, 0.0)

        self.assertFalse(result)

    ####################################################################

    def test_set_position_rst_cent_pos(self):
        """Test if center position can be set"""

        result = self.pos.set_position_rst(0, 0, 0)

        self.assertTrue(result)

        self.assertEqual(self.pos.x, 0)
        self.assertEqual(self.pos.y, 0)
        self.assertEqual(self.pos.z, 0)

    def test_set_position_rst_invalid_ring(self):
        """Test if invalid ring value is not accepted"""

        result = self.pos.set_position_rst(-1, 0, 0)

        self.assertFalse(result)

        self.assertEqual(self.pos.x, 0)
        self.assertEqual(self.pos.y, 0)
        self.assertEqual(self.pos.z, 0)

    def test_set_position_rst_invalid_side(self):
        """Test if invalid side value is not accepted"""

        result = self.pos.set_position_rst(0, 7, 0)

        self.assertFalse(result)

        self.assertEqual(self.pos.x, 0)
        self.assertEqual(self.pos.y, 0)
        self.assertEqual(self.pos.z, 0)

    def test_set_position_rst_invalid_tile(self):
        """Test if invalid tile value is not accepted"""

        result = self.pos.set_position_rst(1, 2, 3)

        self.assertFalse(result)

        self.assertEqual(self.pos.x, 0)
        self.assertEqual(self.pos.y, 0)
        self.assertEqual(self.pos.z, 0)