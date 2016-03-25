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

 Main Hexaco

########################################################################

Description
-----------
Creates all software components and manages the main game loop """

from Engine import GraphicsEngine
from Engine import GameEngine
from Engine.GameSettings import TURNS

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from time import sleep

ROOT = Tk()

# Create the engines
GAME_ENGINE = GameEngine()
GRAPHICS_ENGINE = GraphicsEngine(master=ROOT)

# Set all constants
GRAPHICS_ENGINE.set_hex_radius()

# Alert other engines when a new game_object is added
GAME_ENGINE.callback_for_new_object(GRAPHICS_ENGINE.add_component)

# Initialize all engines
GAME_ENGINE.initialize()

i = TURNS or -1

print ("Starting main game loop")

while i is not 0:

    i -= 1
    GRAPHICS_ENGINE.set_turn_text(i)

    GAME_ENGINE.update()

    GRAPHICS_ENGINE.updateScreen()
    sleep(0.)
