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
    """The engine containing all gameobjects and tiles
    """

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

        tile = self.gameObjectFactory.create_tile()
        self.add_game_object( tile )


    def add_game_object(self, game_object):
        """ Add a game object and call all the methods registered to this event with the game_obj handle """

        if type(game_object) is GameObject:
            self.objects.append( game_object )

            for method in self.callbacks_for_new_object:
                method( game_object )

    def create_map(self, rings):
		
        pass        
            

    def update(self):

        for i in range( len(self.objects) ):
            pass
            #self.objects[i].update()
        

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

if __name__ == '__main__':
    unittest.main(verbosity=1)
