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

 Render Component Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a Render component """

import unittest
from Component import Component

class RenderComponent( Component ):
    """A Move component has a position
    """

    def __init__(self, parent):
        self.parent = parent
        self.visible = True
        self.color = "#ffff00"
        self.polygon = [ 0, 0, 15, 40, 40, 15 ]

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
        cls.rndrComp = RenderComponent(None)

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

    def test_defaultVisibility(self):

        self.assertTrue( self.rndrComp.visible )

        
if __name__ == '__main__':
    unittest.main(verbosity=2)