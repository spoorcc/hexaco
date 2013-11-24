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

 Tile Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a Tile object """

import unittest
from HexagonalPosition import HexagonalPosition

class Tile(object):
    """A single Tile on a hexagonal field
        Has a position and a walkable.
    """

    def __init__(self, parent):
        self.parent = parent
        self.pos = HexagonalPosition( self )
        self.walkable = True

    def get_shape():
        """ Returns a vectored graphic to plot as icon to show """
        pass

    def update():
        """ Is called after each turn to let the object perform an action """
        pass

###################################################################
#
# Test Code
#
###################################################################

class TestTile(unittest.TestCase):
    """Test object for Tile"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.tile = Tile(None)

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

    def test_defaultPosition(self):
        """ The tile must be initialized at the origin """

        self.assertEqual( self.tile.pos.x, 0 )
        self.assertEqual( self.tile.pos.y, 0 )
        self.assertEqual( self.tile.pos.z, 0 )

    def test_defaultWakability(self):
        """ A tile must be wakable by default """

        self.assertTrue( self.tile.walkable )        


if __name__ == '__main__':
    unittest.main(verbosity=1)
