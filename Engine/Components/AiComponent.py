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
        self.interested_in = ANT_DEFAULTS["BEHAVIOUR"]["interested_in"]

        self.chances = ANT_DEFAULTS["BEHAVIOUR"]
        self.pheromone_deposit_delta = ANT_DEFAULTS["DEPOSIT"]["delta"]

        self.deposit_defaults = ANT_DEFAULTS["DEPOSIT"]

        class Stats(object): pass

        self.stats = Stats()
        self.stats.found_food = 0
        self.stats.carrying_food = 0
        self.stats.returned_food = 0

    def update(self):
        """ Takes the information and updates the actions """
        pos_comp = self.components['position']

        if pos_comp.center_of_tile():
            self.act_on_collisions()
            self.update_pheromone_deposit_levels(self.pheromone_deposit_delta)
            pos_comp.orientation = self.choose_orientation()

    def choose_orientation(self):
        dice = random()

        orientation = -1

        if dice <= self.chances["listen_to_pheromone"]:
            orientation = self.get_direction_using_pheromone()
        else:
            orientation = randint(0, 5)

        return orientation

    def update_pheromone_deposit_levels(self, delta):

        deposit_levels = self.components['pheromone_actor'].deposit

        for kind in deposit_levels:
            if kind == self.interested_in:
                deposit_levels[kind] = 0
            else:
                deposit_levels[kind] = max(deposit_levels[kind] - delta, 0)

    def reset_pheromone_deposit_levels(self):

        deposit_levels = self.components['pheromone_actor'].deposit

        for kind in deposit_levels:
            if kind == self.interested_in:
                deposit_levels[kind] = 0
            else:
                deposit_levels[kind] = self.deposit_defaults[kind]

    def act_on_collisions(self):

        collidees = self.components['collision'].objects_collided_with

        for collidee in collidees:

            if 'food' in collidee.components:
                self.found_food(collidee)

            if 'nest' in collidee.components:
                self.found_nest()

    def found_food(self, food_obj):

        if self.interested_in == "food":

            food_comp = food_obj.components['food']
            food = food_comp.take_food(ANT_DEFAULTS["FEEDING"]["speed"])

            self.stats.found_food += food
            self.stats.carrying_food += food

            if food > 0:
                self.interested_in = "home"
                self.components["render"].fill = "#000066"

        self.reset_pheromone_deposit_levels()

    def found_nest(self):

        if self.interested_in == "home":
            self.interested_in = "food"
            self.components["render"].fill = "#000000"

            self.stats.returned_food += self.stats.carrying_food
            self.stats.carrying_food = 0
        self.reset_pheromone_deposit_levels()

    def get_direction_using_pheromone(self):

        pher_act_comp = self.components['pheromone_actor']
        direction = pher_act_comp.direction_of_highest()
        return direction[self.interested_in]
