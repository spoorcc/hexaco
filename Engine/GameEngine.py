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
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a game Engine """

import unittest
from mock import MagicMock

from GameObject import GameObject
from GameObjectFactory import GameObjectFactory

class GameEngine(object):
    """The engine containing all gameobjects and tiles (following the singleton pattern)
    """

    _instance = None 

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """ Initializes all the member variables """
        self.objects = []
        self.tiles = []
        self.gameObjectFactory = GameObjectFactory(self)
        self.callbacks_for_new_object = []

    def callback_for_new_object(self, method_to_call ):
        """ Methods registered here will be called when a new object is created """

        if callable(method_to_call):
            self.callbacks_for_new_object.append( method_to_call )

    def initialize_objects(self):
        """ All objects in the world will be initialized here """

        self.create_map( 5 )

        ant = self.gameObjectFactory.create_ant()
        ant.components['position'].pos.set_position_xyz( 3, -3, 0)
        self.add_game_object( ant )

    def add_game_object(self, game_object):
        """ Add a game object and call all the methods registered to this event with the game_obj handle """

        if type(game_object) is GameObject:
            self.objects.append( game_object )

            for method in self.callbacks_for_new_object:
                method( game_object )

    def get_game_object( self, object_id):
        print cls
        return cls._instance.objects( object_id )            

    def create_map(self, rings):

        # Create the center tile
        tile_obj = self.gameObjectFactory.create_tile()
        self.add_game_object( tile_obj )

        for ring in range( rings  ):
            for side in range( 6 ):  # Hexagon has 6 sides
                for tile in range( ring ):
                    tile_obj = self.gameObjectFactory.create_tile()
                    tile_obj.components['position'].pos.set_position_rst( ring, side, tile )

                    self.add_game_object( tile_obj )                

    def update(self):

        for obj in self.objects:

            # Execute move actions
            if 'move' in obj.components:
                pass

                

###################################################################
#
# Test Code
#
###################################################################

class TestGameEngine(unittest.TestCase):
    """Test object for GameEngine"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.gameEng = GameEngine()

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called before each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        self.gameEng.objects = []

    #######################################################

    def test_add_game_object_valid(self):
        """ Simple test"""

        obj = GameObject(self)
        self.gameEng.add_game_object(obj)

        self.assertEqual( len(self.gameEng.objects ), 1 )

    def test_add_game_object_invalid(self):
        """ Simple test"""
        
        self.gameEng.add_game_object( "not an object" )

        self.assertEqual( len(self.gameEng.objects ), 0 )

    def test_add_game_object_callback(self):
        """ Test if callbacks are called """

        myMock = MagicMock()
        myMock.foo = MagicMock()

        obj = GameObject(self)

        self.gameEng.callback_for_new_object( myMock.foo )
        self.gameEng.add_game_object(obj)

        myMock.foo.assert_called_with( obj )

    def test_create_map_one_tile(self):
        """ Test if a map is created of 1 tile when ring 1 is selected """

        tile = self.gameEng.gameObjectFactory.create_tile()

        self.gameEng.gameObjectFactory.create_tile = MagicMock()
        self.gameEng.gameObjectFactory.create_tile.return_value = tile
        
        self.gameEng.create_map( 1 )
        
        self.assertEqual( len(self.gameEng.gameObjectFactory.create_tile.mock_calls), 1 )

    def test_create_map_seven_tiles(self):
        """ Test if a map is created of 7 tile when ring 2 is selected """

        tile = self.gameEng.gameObjectFactory.create_tile()

        self.gameEng.gameObjectFactory.create_tile = MagicMock()
        self.gameEng.gameObjectFactory.create_tile.return_value = tile
        
        self.gameEng.create_map( 2 )
        
        self.assertEqual( len(self.gameEng.gameObjectFactory.create_tile.mock_calls), 7 )    

if __name__ == '__main__':
    unittest.main(verbosity=1)
