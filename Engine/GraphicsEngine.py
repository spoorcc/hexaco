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

########################################################################

Description
-----------
Base class for a Graphics Engine """

from Tkinter import *
import Tkinter

from math import sin, cos, radians, sqrt
from copy import deepcopy

from GameObject import GameObject
from Components import RenderComponent
from Components import PositionComponent

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

        self.set_window_size( 800, 600 )
        self.set_hex_radius( 10 )
        
        self.setupWindow()

        assert( self.size[0] == 800 )
        assert( self.size[1] == 600 )
                
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

    def set_window_size( self, width, height ):

        self.size = [width, height]
        self.centerScreenCoordinate = [ self.size[0]/2, self.size[1]/2]     
    
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
            coordinates_placed = self.move_object( deepcopy(rend_comp.polygon), x, y )

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
                
            pos_comp  = obj.components['position']
            rend_comp = obj.components['render']

            # Find out where to draw
            [x, y] = self.game_coordinates_to_screen_coordinates( pos_comp.pos.x, pos_comp.pos.y, pos_comp.pos.z )
          
            # Find out what to draw there
            coordinates_placed = self.move_object( deepcopy(rend_comp.polygon), x, y )

            # Move the object
            self.win.coords( rend_comp.renderID, *coordinates_placed  )
            
                  
        self.master.update_idletasks() # redraw
        #self.master.update() # process events
         
