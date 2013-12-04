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

 Game Object Factory Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Class for constructing Game Objects """

import unittest
from GameObject import GameObject
from RenderComponent import RenderComponent
from MoveComponent import MoveComponent

class GameObjectFactory(object):
    """The ObjectFactory which construcs game objects
    """

    def __init__(self, parent):
        self.parent = parent

    def create_object(self):

        return GameObject(None)

    def create_tile(self):

        obj = GameObject(None)
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#00ff00"
        obj.components['render'].fill = "#ffff00"
        obj.components['render'].polygon = [10,50,70,50,70,70,50,70]
        obj.components['render'].XYspeed = [0.01, 0.01]

        return obj
        

###################################################################
#
# Test Code
#
###################################################################

class TestGameObjectFactory(unittest.TestCase):
    """Test object for GameObjectFactory"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.gameObjFact = GameObjectFactory(None)

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

    def test_create_object(self):
        """ Simple test"""

        obj = self.gameObjFact.create_object()
        self.assertEqual( type(obj), GameObject )

if __name__ == '__main__':
    unittest.main(verbosity=1)
