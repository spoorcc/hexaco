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

 Collision Engine Class

########################################################################

Description
-----------
Class for a Collision Engine """


class CollisionEngine(object):
    """The engine managing all pheromones on the map
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Called when creating new instance, return existing instance
        otherwise create new one, singleton pattern """
        if not cls._instance:
            cls._instance = super(CollisionEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.colliders = []

    def add_component(self, game_object):
        """ If a object has a collider and a position component it is added
        to the list of objects to update """

        try:
            if 'collision' in game_object.components and \
                    'position' in game_object.components:
                self.colliders.append(game_object)
        except AttributeError:
            pass

    def update(self):
        """ Check for collisions """

        collide = dict()
        collisions = []

        for obj in self.colliders:

            xyz = obj.components['position'].xyz()
            key = "%+.1f%+.1f%+.1f" % (xyz[0], xyz[1], xyz[2])

            obj.components['collision'].objects_collided_with = []

            if key in collide:
                collide[key].append(obj)
                collisions.append(key)
            else:
                collide[key] = [obj]

        for key in collisions:

            self.inform_collided(collide[key])

    def inform_collided(self, collided):
        """ Informs the objects that have collided """

        for obj in collided:
            collided_with = [col for col in collided if col is not obj]
            obj.components['collision'].objects_collided_with = collided_with
