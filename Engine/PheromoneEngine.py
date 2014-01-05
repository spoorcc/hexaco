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

 Pheromone Engine Class

########################################################################

Description
-----------
Class for a Pheromone Engine """

from math import sqrt
from Engine.LibHexagonalPosition import get_neighbour_xyz


class PheromoneEngine(object):
    """The engine managing all pheromones on the map
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Called when creating new instance, return existing instance
        otherwise create new one, singleton pattern """
        if not cls._instance:
            cls._instance = super(PheromoneEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.holders = dict()
        self.actors = []

    def add_component(self, game_object):
        """ If a object has a pheromone and a position component it is added
        to the list of objects to update """

        try:
            if 'pheromone_holder' in game_object.components and \
                    'position' in game_object.components:
                xyz = game_object.components['position'].xyz()
                key = "%+.0f%+.0f%+.0f" % (xyz[0], xyz[1], xyz[2])
                self.holders[key] = game_object.object_id
                print "Added holder @ %s" % key

            if 'pheromone_actor' in game_object.components and \
                    'position' in game_object.components:
                self.actors.append(game_object.object_id)
        except AttributeError:
            pass

    def pheromone_levels_to_color(self, levels):
        """ Returns a TKinter rgb color string """

        red = sqrt(levels["home"])
        green = 10
        blue = sqrt(levels["food"])
        return "#%02x%02x%02x" % (red, green, blue)

    def get_game_object(self, object_id):
        """ This method should be overloaded """
        raise NotImplementedError

    def get_holder(self, xyz):
        """ Get a pheromone holder using the coordinate """
        key = "%+.0f%+.0f%+.0f" % (xyz[0], xyz[1], xyz[2])
        key = key.replace("-0", "+0")
        obj_id = self.holders[key]
        holder = self.get_game_object(obj_id)
        return holder.components['pheromone_holder']

    def get_levels_xyz(self, xyz):
        """ Returns all levels of the adjacent tiles of position x, y ,z """

        pheromone_levels = {"food": [], "home": []}

        for direction in range(6):

            nghbr_xyz = get_neighbour_xyz(xyz, direction)

            try:
                holder = self.get_holder(nghbr_xyz)
                levels = holder.levels
                pheromone_levels["food"].append(levels["food"])
                pheromone_levels["home"].append(levels["home"])
            except KeyError:
                pheromone_levels["food"].append(None)
                pheromone_levels["home"].append(None)

        return pheromone_levels

    def update_actors(self):
        """ Update the objects that need pheromone data """

        for object_id in self.actors:

            try:
                actor = self.get_game_object(object_id)

            except NotImplementedError:
                print "get_game_object method must be overloaded"

            except KeyError:
                del self.actors[object_id]
                print """Could not find pheromone_actor,
                       removed from update list of PheromoneEngine """

            pos_comp = actor.components['position']

            if pos_comp.center_of_tile():
                ph_comp = actor.components['pheromone_actor']
                ph_comp.neighbour_levels = self.get_levels_xyz(pos_comp.xyz())

    def update_holders(self):
        """ Update the objects that take pheromones """

        for hold_pos in self.holders:

            try:
                object_id = self.holders[hold_pos]
                holder = self.get_game_object(object_id)
                ph_hold_comp = holder.components['pheromone_holder']
                ph_hold_comp.update()

                color = self.pheromone_levels_to_color(ph_hold_comp.levels)
                holder.components['render'].fill = color

            except NotImplementedError:
                print "get_game_object method must be overloaded"

            except KeyError:
                del self.holders[object_id]
                print """Could not find pheromone_actor,
                       removed from update list of PheromoneEngine """

        for object_id in self.actors:

            try:
                actor = self.get_game_object(object_id)
                xyz = actor.components['position'].xyz()

            except NotImplementedError:
                print "get_game_object method must be overloaded"

            except KeyError:
                del self.actors[object_id]
                print """Could not find pheromone_actor,
                       removed from update list of PheromoneEngine """

            pos_comp = actor.components['position']

            if pos_comp.center_of_tile():
                ph_deposit = actor.components['pheromone_actor'].deposit

                xyz = pos_comp.xyz()
                holder = self.get_holder(xyz)

                for ph_dep in ph_deposit:

                    try:
                        holder.levels[ph_dep] += ph_deposit[ph_dep]
                    except KeyError:
                        print "Holder has no %s level" % ph_dep
