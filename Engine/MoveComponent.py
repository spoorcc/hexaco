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

 Move Component Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a move component """

import unittest
from Component import Component

class MoveComponent( Component ):
    """A Move component 
    """

    def __init__(self, parent):
        self.parent = parent
        self.speed = 0.0

        

    def get_xyz_speed(self, orientation):

        speed_mat = [ [1,-1,0], [1,0,-1], [0,1,-1], [-1,1,0], [-1,0,1], [0,-1,1] ]

        xyz_speed = speed_mat[ orientation ]

        return [x*self.speed for x in xyz_speed] 

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
        "This method is called befire each test case"
        self.movComp.speed = 0.0

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_defaultSpeed(self):

        self.assertEqual( self.movComp.speed, 0.0 )

    def test_xyz_speed_or0(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 0 )

        self.assertEqual( xyz_speed, [ 2.0, -2.0, 0.0 ]  )

    def test_xyz_speed_or1(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 1 )

        self.assertEqual( xyz_speed, [ 2.0, 0.0, -2.0 ]  )

    def test_xyz_speed_or2(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 2 )

        self.assertEqual( xyz_speed, [ 0.0, 2.0, -2.0 ]  )

    def test_xyz_speed_or3(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 3 )

        self.assertEqual( xyz_speed, [ -2.0, 2.0, 0.0 ]  )

    def test_xyz_speed_or4(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 4 )

        self.assertEqual( xyz_speed, [ -2.0, 0.0, 2.0 ]  )                      
        
    def test_xyz_speed_or5(self):

        self.movComp.speed = 2.0
        xyz_speed = self.movComp.get_xyz_speed( 5 )

        self.assertEqual( xyz_speed, [ 0.0, -2.0, 2.0 ]  )
                        
if __name__ == '__main__':
    unittest.main(verbosity=2)
