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

 Game Object Factory Test Class

########################################################################

Description
-----------
"""

import unittest

from ..LibCommon import is_float_int, add_delta_to_pos_if_valid


class TestLibCommon(unittest.TestCase):
    """Test object for GameObjectFactory"""

    def test_is_float_int_using_floats(self):
        """ Test for number of floats if the they are
        correctly considered as ints """

        self.assertTrue(is_float_int(-4.0))
        self.assertTrue(is_float_int(0.0))
        self.assertTrue(is_float_int(1.0))
        self.assertTrue(is_float_int(-1.0))
        self.assertTrue(is_float_int(0.0001))
        self.assertTrue(is_float_int(-0.0009))

    def test_is_float_int_using_non_floats(self):
        """ Test for number of floats if the they are
        correctly considered as non-ints """

        self.assertFalse(is_float_int(0.5))
        self.assertFalse(is_float_int(1.1))
        self.assertFalse(is_float_int(-0.3))
        self.assertFalse(is_float_int(-0.5))

    def test_add_delta_to_pos_if_valid_valid(self):

        xyz = (0.0, 0.0, 0.0)
        deltas = (0.5, 0.0, -0.5)
        actual = add_delta_to_pos_if_valid(xyz, deltas, 100.0)

        expected = [xyz[i] + deltas[i] for i in range(len(xyz))]

        self.assertEqual(expected, actual)

    def test_add_delta_to_pos_if_valid_valid_big(self):

        xyz = (0.0, 0.0, 0.0)
        deltas = (-5.0, 5.0, 0.0)
        actual = add_delta_to_pos_if_valid(xyz, deltas, 5.01)

        expected = [xyz[i] + deltas[i] for i in range(len(xyz))]

        self.assertEqual(expected, actual)

    def test_add_delta_to_pos_if_valid_invalid(self):

        xyz = (0.0, 0.0, 0.0)
        deltas = (-5.0, 5.0, 0.0)
        actual = add_delta_to_pos_if_valid(xyz, deltas, 3.0)

        self.assertEqual(xyz, actual)

    def test_add_delta_to_pos_if_valid_invalid_delta(self):

        xyz = (0.0, 0.0, 0.0)
        deltas = (5.0, 5.0, 0.0)
        actual = add_delta_to_pos_if_valid(xyz, deltas, 8.0)

        self.assertEqual(xyz, actual)

if __name__ == '__main__':
    unittest.main(verbosity=1)
