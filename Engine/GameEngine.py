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

 Game Engine Class

########################################################################

Description
-----------
Base class for a game Engine """

from Engine.GameObject import GameObject
from Engine.GameObjectFactory import GameObjectFactory


class GameEngine(object):
    """The engine containing all gameobjects and tiles
    (following the singleton pattern)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """ Initializes all the member variables """
        self.objects = dict()
        self.game_object_factory = GameObjectFactory(self)
        self.callbacks_for_new_object = []

    def callback_for_new_object(self, method_to_call):
        """ Methods registered here will be called
            when a new object is created """

        if callable(method_to_call):
            self.callbacks_for_new_object.append(method_to_call)

    def set_hex_radius(self, hex_radius):
        """ Set the hex radius """
        self.game_object_factory.hex_radius = hex_radius

    def initialize_objects(self):
        """ All objects in the world will be initialized here """

        self.create_map(4)

        ant = self.game_object_factory.create_ant()
        ant.components['position'].pos.set_position_xyz(0, 0, 0)
        self.add_game_object(ant)

    def add_game_object(self, game_object):
        """ Add a game object and call all the methods registered
            to this event with the game_obj handle """

        if type(game_object) is GameObject:
            self.objects[str(game_object.objectID)] = game_object

            for method in self.callbacks_for_new_object:
                method(game_object)

    def get_game_object(self, object_id):
        """ Returns an handle to the game object identified by the
        unique object_id """
        return self._instance.objects[str(object_id)]

    def create_map(self, rings):
        """ Creates a map consisting of a number of rings """

        # Create the center tile
        tile_obj = self.game_object_factory.create_tile()
        self.add_game_object(tile_obj)

        for ring in range(rings):
            for side in range(6):  # Hexagon has 6 sides
                for tile in range(ring):
                    tile_obj = self.game_object_factory.create_tile()
                    pos = tile_obj.components['position'].pos
                    pos.set_position_rst(ring, side, tile)

                    self.add_game_object(tile_obj)

    def update(self):
        """ Updates all the components in the proper order
        , called as part of the main game loop """
        for obj_id, obj in self.objects.iteritems():
            self.update_ai(obj)
            self.update_move(obj)

    def update_ai(self, obj):
        """ Update all the think actions of each game_object"""

        try:
            # Execute move actions
            if 'ai' in obj.components:

                pos_comp = obj.components['position']

                if pos_comp.center_of_tile():
                    print "redirecting"
                    pos_comp.orientation = (pos_comp.orientation + 1) % 6


        except:
            print "Error while trying to let objects think"

    def update_move(self, obj ):
        """ Update all objects with a move component """

        try:
            # Execute move actions
            if 'move' in obj.components:

                move_comp = obj.components['move']
                pos_comp = obj.components['position']

                # Only do the move computations if there is a movement
                if move_comp.speed != 0.0:
                    speed_mat = move_comp.get_xyz_speed(pos_comp.orientation)

                    pos_comp.pos.x += speed_mat[0]
                    pos_comp.pos.y += speed_mat[1]
                    pos_comp.pos.z += speed_mat[2]
        except:
            print "Error while trying to move objects"
