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
from PositionComponent import PositionComponent

from math import sin, cos, radians

class GameObjectFactory(object):
    """The ObjectFactory which construcs game objects
    """

    def __init__(self, parent):
        self.parent = parent
        self.hexRadius = 20
        self.nextObjectId = 0

    def create_object(self):

        return GameObject(None)

    def create_game_object(self):

		obj = GameObject(None)
		obj.objectID = self.nextObjectId

		self.nextObjectId += 1

		return obj

    def create_ant(self):

        obj = self.create_game_object()
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#880000"
        obj.components['render'].fill = "#001100"

        x = 0.4 * self.hexRadius
        obj.components['render'].polygon = [0, -x, x, x, -x, x ]
        obj.components['render'].XYspeed = [0.01, 0.01]

        obj.components['position'] = PositionComponent(obj)

        obj.components['move'] = MoveComponent(obj)
        
        return obj

    def create_tile(self):

        obj = self.create_game_object()
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#005500"
        obj.components['render'].fill = "#220000"
        obj.components['render'].polygon = self.create_hexagon( self.hexRadius )
        obj.components['render'].XYspeed = [0.01, 0.01]

        obj.components['position'] = PositionComponent(obj)
        
        return obj

    def give_point_on_circle(self, degrees, radius ):
        return [ radius * cos( radians(degrees) ), radius * sin( radians(degrees) )]
        
    def create_hexagon(self, radius ):

        coordinates = []
        for i in range(0,6):
            coordinates = coordinates + self.give_point_on_circle( i * 60, radius )

        return coordinates
        
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

    def test_give_point_on_circle(self):

        coordinates = self.gameObjFact.give_point_on_circle( 30, 1 )

        self.assertAlmostEqual( coordinates[0], 0.866, 3 )
        self.assertAlmostEqual( coordinates[1], 0.5, 3 )

    def test_create_hexagon_radius_one(self):

        hexagon = self.gameObjFact.create_hexagon( 1 )
        expected = [ 1.0, 0.0, 0.5, 0.866, -0.5, 0.866, -1.0, 0.0, -0.5, -0.866, 0.5, -0.866]

        for i in range( len(hexagon) ):
            self.assertAlmostEqual( hexagon[i], expected[i] , 3, "%.3f != %.3f @ %d" % (hexagon[i], expected[i], i) )


    def test_create_hexagon_radius_twenty(self):

        hexagon = self.gameObjFact.create_hexagon( 20 )
        expected = [ 20.0, 0.0, 10.0, 17.321, -10.0, 17.321, -20.0, 0.0, -10.0, -17.321, 10.0, -17.321]

        for i in range( len(hexagon) ):
            self.assertAlmostEqual( hexagon[i], expected[i] , 3, "%.3f != %.3f @ %d" % (hexagon[i], expected[i], i) )

if __name__ == '__main__':
    unittest.main(verbosity=1)
