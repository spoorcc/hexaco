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

from ..GameObject import GameObject
from ..GameObjectFactory import GameObjectFactory

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
        "This method is called before each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_create_game_object_returns_object(self):
        """ Simple test"""

        obj = self.gameObjFact.create_game_object()
        self.assertEqual( type(obj), GameObject )

    def test_give_point_on_circle(self):

        coordinates = self.gameObjFact.give_point_on_circle( 30, 1 )

        self.assertAlmostEqual( coordinates[0], 0.866, 3 )
        self.assertAlmostEqual( coordinates[1], 0.5, 3 )

    def test_create_hexagon_radius_one(self):

        hexagon = self.gameObjFact.create_hexagon( 1 )
        expected = [ 1.0,  0.0,   \
                     0.5,  0.866, \
                    -0.5,  0.866, \
                    -1.0,  0.0,   \
                    -0.5, -0.866, \
                     0.5, -0.866]

        for i in range( len(hexagon) ):
            self.assertAlmostEqual( hexagon[i], expected[i] , 3, \
                      "%.3f != %.3f @ %d" % (hexagon[i], expected[i], i) )


    def test_create_hexagon_radius_twenty(self):

        hexagon = self.gameObjFact.create_hexagon( 20 )
        expected = [ 20.0,   0.0,   \
                     10.0,  17.321, \
                    -10.0,  17.321, \
                    -20.0,   0.0,   \
                    -10.0, -17.321, \
                     10.0, -17.321]

        for i in range( len(hexagon) ):
            self.assertAlmostEqual( hexagon[i], expected[i] , 3, \
                      "%.3f != %.3f @ %d" % (hexagon[i], expected[i], i) )

    def test_create_game_object_unique_ids(self):

        obj1 = self.gameObjFact.create_game_object()
        obj2 = self.gameObjFact.create_game_object()

        self.assertNotEqual( obj1.objectID, obj2.objectID )       

if __name__ == '__main__':
    unittest.main(verbosity=1)
