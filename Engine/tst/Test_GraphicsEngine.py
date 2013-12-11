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

 Graphics Engine Test Class

########################################################################

Description
-----------
"""

import unittest
from mock import MagicMock

from math import sin, cos, radians, sqrt
from copy import deepcopy

from ..GraphicsEngine import GraphicsEngine
from ..GameObject import GameObject
from ..Components import RenderComponent
from ..Components import PositionComponent
      

###################################################################
#
# Test Code
#
###################################################################

class TestGraphicsEngine(unittest.TestCase):
    """Test object for GameEngine"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.graphEng = GraphicsEngine(None)
        cls.graphEng.set_window_size( 800, 600 )
                
    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"
        self.graphEng = GraphicsEngine(None)
        self.graphEng.set_window_size( 800, 600 )

        self.dummyGameObject = GameObject( None )
        self.dummyGameObject.components['position'] = PositionComponent(None)
        self.dummyGameObject.components['render'] = RenderComponent(None)


    def tearDown(self):
        "This method is called after each test case"
        self.graphEng.objects = []
        

    #######################################################

    def test_test_class_constants(self):
        """ Assure the constants used by the test class are correct """

        self.assertEqual( self.graphEng.size, [800, 600] )
        self.assertEqual( self.graphEng.centerScreenCoordinate, [400, 300] )

    def test_set_window_size( self ):
        """ Assure setting window size succeeds """

        gE = GraphicsEngine( None )
        gE.set_window_size( 800, 600)

        self.assertEqual( gE.size, [800, 600] )

    def test_game_coordinates_to_screen_coordinates_no_effects_on_size( self ):
        """ It is assumed this calculation has no side effects, this method tests this """

        [screenX, screenY] = self.graphEng.size
        
        [x, y] = self.graphEng.game_coordinates_to_screen_coordinates( 0, 0, 0 )
        
        self.assertEqual( self.graphEng.size, [screenX, screenY], "Screen size cahnged" )

    def test_add_game_object_valid(self):
        """ Test if adding a valid object succeeds """

        obj = MagicMock()
        obj.components = {}
        obj.components['render'] = RenderComponent(obj)
        obj.components['position'] = PositionComponent(obj)
        
        self.graphEng.add_component(obj)
        
        self.assertEqual( len(self.graphEng.objects ), 1 )

    def test_add_game_object_invalid(self):
        """ Test if adding an invalid object fails """
        
        self.graphEng.add_component( "not an object" )
        self.assertEqual( len(self.graphEng.objects ), 0 )

    def test_move_object(self):
        """ Test if moving an object succeeds with different x,y coordinates """
        
        coordinates = [100, 100, 50, 50]
        actual = self.graphEng.move_object( coordinates, 10, 5 )

        self.assertEqual( actual, [110, 105, 60, 55] )

    def test_game_coordinates_to_screen_coordinates_center( self ):
        """ Test if setting game coordinate 0, 0, 0 ends in the center """

        self.assertEqual( self.graphEng.centerScreenCoordinate, [ 400, 300] )
        
        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( 0,0,0 )
  
        self.assertEqual( [x,y], self.graphEng.centerScreenCoordinate )

    def test_game_coordinates_to_screen_coordinates_1_0_m1( self ):
        """ Test if x1 y0 z-1 ends in the correct position """

        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( 1, 0, -1 )

        expected = self.graphEng.centerScreenCoordinate

        expected[0] +=  0 * self.graphEng.screen_x_offset 
        expected[1] += -2 * self.graphEng.screen_y_offset

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_2_0( self ):
        """ Test known game to screen coordinates x -2 y 2 z 0"""
        
        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( -2, 2, 0 )

        expected = self.graphEng.centerScreenCoordinate

        expected[0] +=  2 * self.graphEng.screen_x_offset
        expected[1] +=  2 * self.graphEng.screen_y_offset

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_3_m1( self ):
        """ Test known game to screen coordinates x -2 y 3 z -1"""

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( -2, 3, -1 )

        expected = self.graphEng.centerScreenCoordinate

        expected[0] +=   3 * self.graphEng.screen_x_offset
        expected[1] +=   1 * self.graphEng.screen_y_offset

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_get_game_object_call(self):
        """ Test to verify the method can be overloaded by an other method, and is called """

        # Replace the method with the mock method
        gameEng = MagicMock()
        gameEng.get_game_object = MagicMock()
        self.graphEng.get_game_object = gameEng.get_game_object

        # Add an object to the object list
        self.graphEng.objects.append( 123 )
        self.assertEqual( len( self.graphEng.objects), 1 )

        # Trigger the function that should call get_game_object
        self.graphEng.updateScreen()

        gameEng.get_game_object.assert_called_with( 123 )
              
    def test_get_game_object_missing_components(self):
        """ Test to verify that the method updating the screen fails
        when the render or position component are missing """

        # Replace the method with the mock method
        gameEng = MagicMock()
        gameEng.get_game_object = MagicMock()
        
        gameEng.get_game_object.return_value = self.dummyGameObject

        # Set the function to call
        self.graphEng.get_game_object = gameEng.get_game_object
        
        # Add an object to the object list
        self.graphEng.objects.append( 45 )
        self.assertEqual( len( self.graphEng.objects), 1 )

        # Trigger the function that should redraw
        self.assertRaises( KeyError, self.graphEng.updateScreen() )

    def test_render_component_not_affected_by_drawing(self):
        """  """    

        polygon = self.dummyGameObject.components['render'].polygon
        polygon_copy = deepcopy( polygon )
        self.graphEng.add_component( self.dummyGameObject )

        self.assertEqual( self.dummyGameObject.components['render'].polygon, polygon_copy )
        
        

if __name__ == '__main__':
    unittest.main(verbosity=1)
