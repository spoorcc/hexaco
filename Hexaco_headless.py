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

from Engine import GameEngine
from Engine.GameSettings import TURNS

# Create the engines
GAME_ENGINE = GameEngine()

# Initialize all engines
GAME_ENGINE.initialize()

i = TURNS or -1
i = 5000

print ("Starting main game loop")

while i is not 0:

    i -= 1
    GAME_ENGINE.update()

print ("Done with main game loop")
stats = GAME_ENGINE.get_stats()

print(max(stats,key=lambda item:item[1]))
