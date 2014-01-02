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
                key = "%d%d%d" % (xyz[0], xyz[1], xyz[2])
                self.holders[key] = game_object.object_id

            if 'pheromone_actor' in game_object.components and \
                    'position' in game_object.components:
                self.actors.append(game_object.object_id)
        except AttributeError:
            pass

    def get_game_object(self, object_id):
        """ This method should be overloaded """
        print "Whooops "

    def get_levels_xyz(self, xyz):
        """ Returns all levels of the adjacent tiles of position x, y ,z """

        levels = []

        for idx in range(6):

            levels.append(None)

        return levels

    def update_map(self):
        """ Update the objects that need pheromone data """

        for object_id in self.holders:

            try:
                holder = self.get_game_object(object_id)

            except:
                print "Could not find object"

            ph_comp = holder.components['pheromone_holder']
            pos_comp = holder.components['position']

            ph_comp.neighbour_levels = self.get_levels_xyz(pos_comp.xyz)
