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

 AI Component Class

########################################################################

Description
-----------
Class for a Artificial Intelligence component """

from Engine.Components.Component import Component
from Engine.Components.PheromoneActorComponent import PheromoneActorComponent
from random import random, randint


class AiComponent(Component):
    """An Ai component
    """

    def __init__(self, parent):
        self.parent = parent
        self.interested_in = "food"

        self.chances = {"listen_to_pheromone": 0.50,
                        "listen_to_random": 0.05}

    def update(self):
        """ Takes the information and updates the actions """
        pos_comp = self.components['position']

        if pos_comp.center_of_tile():

            if random() <= self.chances["listen_to_pheromone"]:
                pos_comp.orientation = \
                               self.get_direction_using_pheromone()
            else:
                pos_comp.orientation = randint(0, 5)

    def get_direction_using_pheromone(self):

        pher_act_comp = self.components['pheromone_actor']
        return pher_act_comp.direction_of_highest()[self.interested_in]


