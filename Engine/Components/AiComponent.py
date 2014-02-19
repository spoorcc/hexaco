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
from Engine.GameSettings import ANT_DEFAULTS

class AiComponent(Component):
    """An Ai component
    """

    def __init__(self, parent):
        self.parent = parent
        self.interested_in = "food"

        self.chances = {"listen_to_pheromone": 0.65,
                        "listen_to_random": 0.50}

        self.delta = 0.1

    def update(self):
        """ Takes the information and updates the actions """
        pos_comp = self.components['position']

        if pos_comp.center_of_tile():

            self.check_collisions()
            self.update_pheromone_deposit_levels(self.delta)

            dice = random()

            if dice <= self.chances["listen_to_pheromone"]:
                pos_comp.orientation = \
                               self.get_direction_using_pheromone()
            else:
                pos_comp.orientation = randint(0, 5)

    def update_pheromone_deposit_levels(self, delta):

        deposit_levels = self.components['pheromone_actor'].deposit

        if self.interested_in is "home":

            deposit_levels["food"] = max(deposit_levels["food"] - delta, 0)
            deposit_levels["home"] = 0

        else:
            deposit_levels["food"] = 0
            deposit_levels["home"] = max(deposit_levels["home"] - delta, 0)

    def check_collisions(self):

        collidees = self.components['collision'].objects_collided_with

        for collidee in collidees:

            if 'food' in collidee.components:
                self.found_food(collidee)

            if 'nest' in collidee.components:
                self.found_nest()

    def found_food(self, food_obj):

        if self.interested_in == "food":

            food = food_obj.components['food'].take_food(5)

            deposit_levels = self.components['pheromone_actor'].deposit
            deposit_levels["food"] = ANT_DEFAULTS["DEPOSIT_FOOD"]
            deposit_levels["home"] = 0

            if food > 0:
                self.interested_in = "home"

    def found_nest(self):

        if self.interested_in == "home":
            self.interested_in = "food"

            deposit_levels = self.components['pheromone_actor'].deposit

            deposit_levels["food"] = 0
            deposit_levels["home"] = ANT_DEFAULTS["DEPOSIT_HOME"]

    def get_direction_using_pheromone(self):

        pher_act_comp = self.components['pheromone_actor']
        return pher_act_comp.direction_of_highest()[self.interested_in]


