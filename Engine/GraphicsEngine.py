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

from math import sqrt
from copy import deepcopy

from Engine.GameSettings import HEX_RADIUS, WINDOW_SIZE


class GraphicsEngine(object, Frame):
    """The engine managing all drawing to screen
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ There shoud only be one GraphicsEngine, so return
        the existing instance if a new one is requested """
        if not cls._instance:
            cls._instance = super(GraphicsEngine, cls).__new__(
                                  cls, *args, **kwargs)
        return cls._instance

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.objects = []

        self.win = None
        self.turn_text = None

        self.hex_radius = HEX_RADIUS

        self.hex_width = None
        self.screen_x_offset = None

        self.hex_height = None
        self.screen_y_offset = None

        self.center_screen_coordinate = None

        self.set_window_size(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.set_hex_radius(HEX_RADIUS)
        self.setup_window()

        assert(self.size[0] == WINDOW_SIZE[0])
        assert(self.size[1] == WINDOW_SIZE[1])

    def setup_window(self):
        """ Creates the specific Tkinter components"""

        # Create black backgrounded window
        self.win = Tkinter.Canvas(self.master,
                                  width=self.size[0],
                                  height=self.size[1],
                                  background="#000000")

        self.win.create_text(25, 6,
                             text="Hexaco",
                             font="Arial 10",
                             fill="#ff0000")

        self.turn_text = self.win.create_text(250, 6,
                                              text="No turn",
                                              font="Arial 10",
                                              fill="#ff0000")

        self.win.pack(fill=BOTH, expand=1)

    def set_hex_radius(self, hex_radius=HEX_RADIUS):
        """ Sets the hex_radius and calculates the offsets
        needed for rendering"""

        self.hex_radius = hex_radius

        self.hex_width = self.hex_radius * 2.0
        self.screen_x_offset = 3 * self.hex_width / 4

        self.hex_height = sqrt(3)/2 * self.hex_width
        self.screen_y_offset = self.hex_height / 2

    def set_window_size(self, width, height):
        """ Sets the size of the window """

        self.size = [width, height]
        self.center_screen_coordinate = [self.size[0]/2, self.size[1]/2]

    def set_turn_text(self, turn_text):
        """Set the text of the turn field"""
        self.win.itemconfigure(self.turn_text, text=turn_text)

    def add_component(self, gameObject):
        """ If a component has a render and a move component it is added
        to the list of objects to render """
        try:
            rend = gameObject.components['render']
            pos = gameObject.components['position'].pos

            # Find out where to draw
            [s_x, s_y] = self.game_to_screen_coordinates(pos.x, pos.y, pos.z)

            # Find out what to draw there
            coords_placed = self.place_object(rend.polygon,
                                             s_x, s_y)

            # Find out how to draw, and draw it
            rend.renderID = self.win.create_polygon(coords_placed,
                                                    outline=rend.color,
                                                    width=rend.width,
                                                    fill=rend.fill,
                                                    tag=gameObject.name)

            self.objects.append([rend, pos])

        except AttributeError:
            print "Render/Position component of has wrong attributes"
        except:
            print "Something went wrong"

    def place_object(self, coordinates, delta_x, delta_y):
        """ Updates a list of coordinates assuming [x0,y0,x1,y1,...xN,yN]"""

        #moved_coordinates = []

        #for i in range(len(coordinates)):  # For each coordinate
        #    if i % 2 == 0:  # X-coordinate
        #        moved_coordinates += [coordinates[i] + delta_x]
        #    else:         # Y-coordinate
        #        moved_coordinates += [coordinates[i] + delta_y]

        moved_coordinates = [coord + (delta_y if i%2 else delta_x) for i, coord in enumerate(coordinates)]

        return moved_coordinates


    def place_object_xyz(self, coordinates, x, y, z):
        """ Updates a list of coordinates assuming [x0,y0,x1,y1,...xN,yN]"""

        screen_x = self.size[0]/2 + self.screen_x_offset * y
        screen_y = self.size[1]/2 - self.screen_y_offset * (2 * x + y)
        moved_coordinates = [coord + (screen_y if i%2 else screen_x) for i, coord in enumerate(coordinates)]

        return moved_coordinates

    def game_to_screen_coordinates(self, x, y, z):
        """ Translates the game 3-axis coordinates to screen coordinates
        placing the center coordinates 0,0,0 in the center of the screen """

        screen_x = self.size[0]/2 + self.screen_x_offset * y
        screen_y = self.size[1]/2 - self.screen_y_offset * (2 * x + y)

        return [screen_x, screen_y]

    def updateScreen(self):

        for [rend_comp, pos] in self.objects:

            # Find out where to draw
            coordinates_placed = self.place_object_xyz(rend_comp.polygon,pos.x, pos.y, pos.z)

            # Move the object
            self.win.coords(rend_comp.renderID, *coordinates_placed)

            self.win.itemconfig(rend_comp.renderID,
                                fill=rend_comp.fill,
                                state=(DISABLED if rend_comp.visible else HIDDEN))

        self.master.update_idletasks()  # redraw
        self.master.update() # process events
