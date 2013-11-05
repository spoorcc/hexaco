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

 Moving Game Object Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a moving game object """

import unittest
from GameObject import GameObject

class MovingGameObject(GameObject):
    """A single Gameobject on a hexagonal field
        Has a position and a visible attribute. It can move and step to neighbouring tiles
    """

    def __init__(self, parent):
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.name = "Default"
        self.pos = HexagonalPosition( self )
        self.visible = True

	def 

###################################################################
#
# Test Code
#
###################################################################

class TestMovingGameObject(unittest.TestCase):

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.gameObj = GameObject(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_defaultName(self):

        self.assertEqual( self.gameObj.name, "Default" )

    def test_defaultPosition(self):

        self.assertEqual( self.gameObj.pos.x, 0 )
        self.assertEqual( self.gameObj.pos.y, 0 )
        self.assertEqual( self.gameObj.pos.z, 0 )
        
    def test_defaultVisibility(self):        
		
		self.assertTrue( self.gameObj.visible )


if __name__ == '__main__':
    unittest.main(verbosity=2)
