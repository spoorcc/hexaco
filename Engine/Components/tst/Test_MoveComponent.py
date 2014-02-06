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

 Move Component Test Class

########################################################################

Description
-----------
 """

import unittest
from ..MoveComponent import MoveComponent
from ..PositionComponent import PositionComponent

###################################################################
#
# Test Code
#
###################################################################


class TestMoveComponent(unittest.TestCase):

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.movComp = MoveComponent(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called before each test case"
        self.movComp.speed = 0.0

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_defaultSpeed(self):

        self.assertEqual(self.movComp.speed, 0.0)

    def test_xyz_speed_or0(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(0)

        self.assertEqual(xyz_speed, [2.0, -2.0, 0.0])

    def test_xyz_speed_or1(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(1)

        self.assertEqual(xyz_speed, [2.0, 0.0, -2.0])

    def test_xyz_speed_or2(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(2)

        self.assertEqual(xyz_speed, [0.0, 2.0, -2.0])

    def test_xyz_speed_or3(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(3)

        self.assertEqual(xyz_speed, [-2.0, 2.0, 0.0])

    def test_xyz_speed_or4(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(4)

        self.assertEqual(xyz_speed, [-2.0, 0.0, 2.0])

    def test_xyz_speed_or5(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed(5)

        self.assertEqual(xyz_speed, [0.0, -2.0, 2.0])

    def test_update(self):

        self.movComp.speed = 5.0

        pos = [-2.0, 0.0, 2.0]
        pos_comp = PositionComponent(None)
        pos_comp.set_position_xyz(pos)

        self.movComp.components['position'] = pos_comp

        deltas = self.movComp.get_xyz_speed(pos_comp.orientation)

        expected = [pos[i] + deltas[i] for i in range(3)]

        self.assertEqual(expected, pos_comp.xyz())

if __name__ == '__main__':
    unittest.main(verbosity=2)
