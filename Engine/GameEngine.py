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
        self.objects = dict()
        self.gameObjectFactory = GameObjectFactory(self)
        self.callbacks_for_new_object = []

    def callback_for_new_object(self, method_to_call ):
        """ Methods registered here will be called when a new object is created """

        if callable(method_to_call):
            self.callbacks_for_new_object.append( method_to_call )

    def initialize_objects(self):
        """ All objects in the world will be initialized here """

        self.create_map( 4 )

        ant = self.gameObjectFactory.create_ant()
        ant.components['position'].pos.set_position_xyz( 3, -3, 0)
        self.add_game_object( ant )

    def add_game_object(self, game_object):
        """ Add a game object and call all the methods registered to this event with the game_obj handle """

        if type(game_object) is GameObject:
            self.objects[ str(game_object.objectID) ] =  game_object

            for method in self.callbacks_for_new_object:
                method( game_object )

    def get_game_object( self, object_id):
        return self._instance.objects[ str(object_id) ]

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

        for obj_id, obj in self.objects.iteritems():
            self.update_ai( obj )
            self.update_move( obj )

    def update_ai(self, obj ):

        try:
            # Execute move actions
            if 'ai' in obj.components:

                pos_comp = obj.components['position']

                print "x: %f y: %f z: %f" % (pos_comp.pos.x, pos_comp.pos.y, pos_comp.pos.z)
                   
                if pos_comp.center_of_tile():
                    print "redirecting"
                    pos_comp.orientation = (pos_comp.orientation + 1 ) % 6
                
                
        except:
            print "Error while trying to let objects think"                        

    def update_move(self, obj ):

        try:
            # Execute move actions
            if 'move' in obj.components:

                move_comp = obj.components['move']
                pos_comp = obj.components['position']

                # Only do the move computations if there is a movement
                if move_comp.speed != 0.0:
                    speed_mat = move_comp.get_xyz_speed( pos_comp.orientation )
                    
                    pos_comp.pos.x += speed_mat[0]
                    pos_comp.pos.y += speed_mat[1]
                    pos_comp.pos.z += speed_mat[2]                    
        except:
            print "Error while trying to move objects"                

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
        self.gameEng.objects = {}

    #######################################################

    def test_add_game_object_valid(self):
        """ Test if adding a valid game object succeeds """

        obj = GameObject(self)
        self.gameEng.add_game_object(obj)

        self.assertEqual( len(self.gameEng.objects ), 1 )

    def test_add_game_object_multiple_valid_objects(self):
        """ Test if adding multiple valid game objects succeeds """

        for i in range( 5 ): 
            obj = self.gameEng.gameObjectFactory.create_tile()
            self.gameEng.add_game_object(obj)

        self.assertEqual( len(self.gameEng.objects ), 5 )

    def test_add_game_object_invalid(self):
        """ Test if a invalid game object is not added """
        
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

    def test_get_game_object_call(self):
        """ Test if getting the game object returns an object """

        obj = self.gameEng.gameObjectFactory.create_game_object()
        
        self.gameEng.add_game_object( obj )

        fetchedObj = self.gameEng.get_game_object( obj.objectID )

        self.assertEqual( fetchedObj, obj )

    def test_update(self):
        """ Test the update call """

        obj = self.gameEng.gameObjectFactory.create_ant()

        self.gameEng.add_game_object( obj )

        

if __name__ == '__main__':
    unittest.main(verbosity=1)
