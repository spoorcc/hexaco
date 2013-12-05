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

from RenderComponent import RenderComponent
from MoveComponent import MoveComponent

from math import sin, cos, radians

class GraphicsEngine(Frame):
    """The engine containing all drawable objects
    """

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.objects = []
        self.moves = {}
        self.tiles = []
        self.size = [800, 400]
        self.setupWindow()
        self.hexRadius = 20
        self.xOff = sin( radians(30) ) * self.hexRadius
        self.yOff = cos( radians(30) ) * self.hexRadius
        

    def setupWindow(self):
        
        # Create black backgrounded window
        self.win = Tkinter.Canvas( self.master, width=self.size[0], height=self.size[1], background="#000000")
        self.win.create_text( 25, 6, text="Hexaco", font="Arial 10", fill="#ff0000")
        self.turnText = self.win.create_text( 250, 6, text="No turn", font="Arial 10", fill="#ff0000")        
        self.win.pack(fill=BOTH, expand=1)
       
    
    def setTurnText( self, turnText ):

        self.win.itemconfigure(self.turnText, text=turnText)

    def add_component(self, gameObject ):

        try:            
            rend_comp = gameObject.components['render']

            coordinates_placed = self.move_object( rend_comp.polygon, self.size[0]/2, self.size[1]/2)
            obj_to_render = self.win.create_polygon( coordinates_placed, outline=rend_comp.color, width=rend_comp.width, fill=rend_comp.fill, tag=gameObject.name )
            
            self.objects.append( obj_to_render )
               
        except AttributeError:
            print "Render component of has wrong attributes"
            print gameObject
        except: 
            print "Something went wrong"


    def move_object(self, coordinates, delta_x, delta_y ):
        # For each coordinate 
        for j in range( len(coordinates) ):

            # X-coordinate
            if j%2 == 0:
                coordinates[j] += delta_x
            # Y-coordinate  
            else:
                coordinates[j] += delta_y      

        return coordinates

    def game_coordinates_to_screen_coordinates( self, x, y, z ):

        screen_x, screen_y = self.size[0]/2, self.size[1]/2

        screen_x += self.xOff * 3 * y
        screen_y += self.yOff * 2 * x

        return [screen_x, screen_y]    
                    
    def updateScreen(self):

        for i in range( len(self.objects) ):
            pos = self.win.coords( self.objects[i] )
            
            self.win.coords(  self.objects[i], *pos  )
                  
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

    def test_add_game_object_valid(self):
        """ Simple test"""

        obj = MagicMock()
        obj.components = {}
        obj.components['render'] = RenderComponent(obj)
        
        self.graphEng.add_component(obj)
        
        self.assertEqual( len(self.graphEng.objects ), 1 )

    def test_add_game_object_invalid(self):
        """ Simple test"""
        
        self.graphEng.add_component( "not an object" )
        self.assertEqual( len(self.graphEng.objects ), 0 )

    def test_move_object(self):

        coordinates = [100, 100, 50, 50]
        actual = self.graphEng.move_object( coordinates, 10, 5 )

        self.assertEqual( actual, [110, 105, 60, 55] )

    def test_game_coordinates_to_screen_coordinates_center( self ):

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( 0,0,0 )
  
        self.assertEqual( [x,y], [self.graphEng.size[0]/2, self.graphEng.size[1]/2] )

    def test_game_coordinates_to_screen_coordinates_1_0_m1( self ):

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( 1, 0, -1 )

        expected = [self.graphEng.size[0]/2, self.graphEng.size[1]/2]
        expected[1] +=  2 * self.graphEng.yOff

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_2_0( self ):

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( -2, 2, 0 )

        expected = [self.graphEng.size[0]/2, self.graphEng.size[1]/2]

        expected[0] +=  3 * self.graphEng.hexRadius
        expected[1] +=  -4 * self.graphEng.yOff

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )

    def test_game_coordinates_to_screen_coordinates_m2_3_1( self ):

        [x,y] =self.graphEng.game_coordinates_to_screen_coordinates( -2, 3, 1 )

        expected = [self.graphEng.size[0]/2, self.graphEng.size[1]/2]

        expected[0] +=   9 * self.graphEng.xOff
        expected[1] +=  -4 * self.graphEng.yOff

        self.assertAlmostEqual( x, expected[0], 3 )
        self.assertAlmostEqual( y, expected[1], 3 )        
            

if __name__ == '__main__':
    unittest.main(verbosity=1)
