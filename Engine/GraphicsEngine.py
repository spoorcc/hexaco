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

 Graphics Engine Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a Graphics Engine """

from Tkinter import *
import Tkinter

import unittest
from mock import MagicMock

from GameObject import GameObject
from RenderComponent import RenderComponent
from PositionComponent import PositionComponent

from math import sin, cos, radians, sqrt

class GraphicsEngine(Frame):
    """The engine managing all drawing to screen
    """

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GraphicsEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.objects = []
        self.size = [800, 600]
        self.set_hex_radius( 10 )        
        self.setupWindow()
                
    def setupWindow(self):
        
        # Create black backgrounded window
        self.win = Tkinter.Canvas( self.master, width=self.size[0], height=self.size[1], background="#000000")
        self.win.create_text( 25, 6, text="Hexaco", font="Arial 10", fill="#ff0000")
        self.turnText = self.win.create_text( 250, 6, text="No turn", font="Arial 10", fill="#ff0000")        
        self.win.pack(fill=BOTH, expand=1)

    def set_hex_radius( self, hexRadius ):
        """ Sets the hexRadius and calculates the offsets needed for rendering"""

        self.hexRadius = hexRadius
        
        self.hex_width = self.hexRadius * 2.0
        self.screen_x_offset = 3 * self.hex_width / 4

        self.hex_height = sqrt(3)/2 * self.hex_width
        self.screen_y_offset = self.hex_height / 2     
    
    def setTurnText( self, turnText ):
        self.win.itemconfigure(self.turnText, text=turnText)

    def get_game_object( self, objectID ):
        """ This method gets called by the graphics engine to get an
        gameobject by ID, it must be replaced by the correct method """
        raise Exception("get_game_object method should be replaced with the correct method")

    def add_component(self, gameObject ):
        """ If a component has a render and a move component it is added
        to the list of objects to render """
        try:            
            rend_comp = gameObject.components['render']
            pos = gameObject.components['position'].pos

            # Find out where to draw
            [x, y] = self.game_coordinates_to_screen_coordinates( pos.x, pos.y, pos.z )

            # Find out what to draw there
            coordinates_placed = self.move_object( rend_comp.polygon, x, y )

            # Find out how to draw, and draw it
            rend_comp.renderID = self.win.create_polygon( coordinates_placed, outline=rend_comp.color, width=rend_comp.width, fill=rend_comp.fill, tag=gameObject.name )
                     
            self.objects.append( gameObject.objectID )
               
        except AttributeError:
            print "Render/Position component of has wrong attributes"
        except: 
            print "Something went wrong"
        

    def move_object(self, coordinates, delta_x, delta_y ):
        """ Updates a list of coordinates assuming [x0,y0,x1,y1,...xN,yN]"""
         
        for i in range( len(coordinates) ): # For each coordinate
            if i%2 == 0:  # X-coordinate
                coordinates[i] += delta_x
            else:         # Y-coordinate  
                coordinates[i] += delta_y      

        return coordinates

    def game_coordinates_to_screen_coordinates( self, x, y, z ):
        """ Translates the game 3-axis coordinates to screen coordinates
        placing the center coordinates 0,0,0 in the center of the screen """

        screen_x, screen_y = self.size[0]/2, self.size[1]/2

        screen_x += self.screen_x_offset * y
        screen_y -= self.screen_y_offset * (2 * x + y)

        return [screen_x, screen_y]    
                    
    def updateScreen(self):

        for objectID in self.objects:

            try:
                obj = self.get_game_object( objectID )
                
            except:
                print "Could not find object"    
            """    
            pos  = obj.components['position']
            rend = obj.components['render']

            # Find out where to draw
            [x, y] = self.game_coordinates_to_screen_coordinates( pos.x, pos.y, pos.z )

            # Find out what to draw there
            coordinates_placed = self.move_object( rend.polygon, x, y )

            # Move the object
            self.win.coords( rend.renderID, *coordinates_placed  )
"""
            
                  
        self.master.update_idletasks() # redraw
        #self.master.update() # process events
           

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
        cls.graphEng.size = [800, 600]
        cls.centerScreenCoordinate = [ cls.graphEng.size[0]/2, cls.graphEng.size[1]/2]
        
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
        self.graphEng.objects = []

    #######################################################

    def test_test_class_constants(self):
        """ Assure the constants used by the test class are correct """

        self.assertEqual( self.graphEng.size, [800, 600] )
        self.assertEqual( self.centerScreenCoordinate, [400, 300] )

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

        self.assertEqual( self.centerScreenCoordinate, [ 400, 300] )
        
        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( 0,0,0 )
  
        self.assertEqual( [x,y], self.centerScreenCoordinate )

    def test_game_coordinates_to_screen_coordinates_1_0_m1( self ):
        """ Test if x1 y0 z-1 ends in the correct position """

        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( 1, 0, -1 )

        expected = self.centerScreenCoordinate

        expected[0] +=  0 * self.graphEng.screen_x_offset 
        expected[1] += -1 * self.graphEng.screen_y_offset

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_2_0( self ):
        """ Test known game to screen coordinates x -2 y 2 z 0"""
        
        [x,y] = self.graphEng.game_coordinates_to_screen_coordinates( -2, 2, 0 )

        expected = self.centerScreenCoordinate

        expected[0] +=  2 * self.graphEng.screen_x_offset
        expected[1] +=  2 * self.graphEng.screen_y_offset

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_3_m1( self ):
        """ Test known game to screen coordinates x -2 y 3 z -1"""

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( -2, 3, -1 )

        expected = self.centerScreenCoordinate

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

        dummyGameObject = GameObject( None )
        dummyGameObject.components['position'] = PositionComponent(None)
        dummyGameObject.components['render'] = RenderComponent(None)

        gameEng.get_game_object.return_value = dummyGameObject

        

        self.graphEng.get_game_object = gameEng.get_game_object
        
        # Add an object to the object list
        self.graphEng.objects.append( 45 )
        self.assertEqual( len( self.graphEng.objects), 1 )

        # Trigger the function that should redraw
        self.assertRaises( KeyError, self.graphEng.updateScreen() )

        
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
