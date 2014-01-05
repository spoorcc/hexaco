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
from Engine import PheromoneEngine

import Tkinter

from time import sleep

ROOT = Tkinter.Tk()

HEX_RADIUS = 12

# Create the engines
GAME_ENGINE = GameEngine()
GRAPHICS_ENGINE = GraphicsEngine(master=ROOT)
PHEROMONE_ENGINE = PheromoneEngine()

# Set all constants
GRAPHICS_ENGINE.set_hex_radius(HEX_RADIUS)
GAME_ENGINE.set_hex_radius(HEX_RADIUS)

# Alert other engines when a new game_object is added
GAME_ENGINE.callback_for_new_object(GRAPHICS_ENGINE.add_component)
GAME_ENGINE.callback_for_new_object(PHEROMONE_ENGINE.add_component)

GRAPHICS_ENGINE.get_game_object = GAME_ENGINE.get_game_object
PHEROMONE_ENGINE.get_game_object = GAME_ENGINE.get_game_object

# Initialize all engines
GAME_ENGINE.initialize_objects()

i = 0

print "Starting main game loop"

while 1:

    i += 1
    GRAPHICS_ENGINE.set_turn_text(i)
    PHEROMONE_ENGINE.update_actors()
    GAME_ENGINE.update()
    PHEROMONE_ENGINE.update_holders()
    GRAPHICS_ENGINE.updateScreen()
    sleep(0.)
