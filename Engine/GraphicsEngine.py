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
from RenderComponent import RenderComponent
from MoveComponent import MoveComponent

class GraphicsEngine(Frame):
    """The engine containing all drawable objects
    """

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.objects = []
        self.moves = []
        self.tiles = []

        self.setupWindow()   

    def setupWindow(self):
        
        # Create black backgrounded window
        self.win = Tkinter.Canvas( self.master, width=800, height=400, background="#000000")
        self.win.create_text( 25, 6, text="Hexaco", font="Arial 10", fill="#ff0000")
        self.turnText = self.win.create_text( 250, 6, text="No turn", font="Arial 10", fill="#ff0000")        
        self.win.pack(fill=BOTH, expand=1)
    
    def setTurnText( self, turnText ):

        self.win.itemconfigure(self.turnText, text=turnText)

    def add_component(self, gameObject ):

        try:
            rend_comp = gameObject.components['render']
            
            self.objects.append( self.win.create_polygon( rend_comp.polygon , outline=rend_comp.color, width=1, fill="white") )
               
        except AttributeError:
            print "Something went wrong"
            pass        

    def add_render_component(self, renderComponent):

        if type(renderComponent) is RenderComponent:
            #self.objects.append( renderComponent )
            self.objects.append( self.win.create_polygon( 0, 0, 10, 200, 100, 200, outline="#ffff00", width=1) )
            
    def updateScreen(self):

        for i in range( len(self.objects) ):

            pos = self.win.coords(self.objects[i])

            #pos[0] += self.moves[i].XYspeed[0]
            #pos[1] += self.moves[i].XYspeed[1]

            pos[0] += 0.01
            pos[1] += 0.01
   
            self.win.coords( self.objects[i], pos[0], pos[1])
      
        self.master.update_idletasks() # redraw
        self.master.update() # process events
           

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
        pass

    #######################################################

    def test_add_game_object_valid(self):
        """ Simple test"""

        obj = RenderComponent(self)
        self.graphEng.add_render_component(obj)

        self.assertEqual( len(self.graphEng.objects ), 1 )

    def test_add_game_object_invalid(self):
        """ Simple test"""
        
        self.graphEng.add_render_component( "not an object" )

        self.assertEqual( len(self.graphEng.objects ), 0 )

if __name__ == '__main__':
    unittest.main(verbosity=1)
