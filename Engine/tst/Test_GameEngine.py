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

 Game Engine Test Class

########################################################################

Description
-----------
 """

import unittest
from mock import MagicMock, patch

from ..GameObject import GameObject
from ..GameEngine import GameEngine
from Engine.Components.AiComponent import AiComponent
from Engine.Components.MoveComponent import MoveComponent
from Engine.Components.PositionComponent import PositionComponent


class Testgame_engine(unittest.TestCase):  # pylint: disable=R0904
    """Test object for game_engine"""

    @classmethod
    def setUpClass(cls):  # pylint: disable=C0103
        "This method is called once, when starting the tests"
        cls.game_eng = GameEngine()

        cls.dummyObj = cls.game_eng.game_object_factory.create_game_object()

        cls.dummyMovObj = GameObject(None)
        cls.dummyMovObj.components['move'] = MoveComponent(None)

        cls.dummyMovPosObj = GameObject(None)
        cls.dummyMovPosObj.components['move'] = MoveComponent(None)
        cls.dummyMovPosObj.components['position'] = PositionComponent(None)

        cls.dummyAiObj = GameObject(None)
        cls.dummyAiObj.components['ai'] = AiComponent(None)

        cls.dummyAiPosObj = GameObject(None)
        cls.dummyAiPosObj.components['ai'] = AiComponent(None)
        cls.dummyAiPosObj.components['position'] = PositionComponent(None)

    @classmethod
    def tearDownClass(cls):  # pylint: disable=C0103
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):  # pylint: disable=C0103
        "This method is called before each test case"
        self.game_eng = GameEngine()

    def tearDown(self):  # pylint: disable=C0103
        "This method is called after each test case"
        self.game_eng.objects = {}

    #######################################################

    def test_add_game_object_valid(self):
        """ Test if adding a valid game object succeeds """

        obj = GameObject(self)
        self.game_eng.add_game_object(obj)

        self.assertEqual(len(self.game_eng.objects), 1)

    def test_add_game_obj_mult_val_objs(self):
        """ Test if adding multiple valid game objects succeeds """

        for i in range(5):
            obj = self.game_eng.game_object_factory.create_tile()
            self.game_eng.add_game_object(obj)

        self.assertEqual(len(self.game_eng.objects), 5)

    def test_add_game_object_invalid(self):
        """ Test if a invalid game object is not added """

        self.game_eng.add_game_object("not an object")

        self.assertEqual(len(self.game_eng.objects), 0)

    def test_add_game_object_callback(self):
        """ Test if callbacks are called """

        my_mock = MagicMock()
        my_mock.foo = MagicMock()

        obj = GameObject(self)

        self.game_eng.callback_for_new_object(my_mock.foo)
        self.game_eng.add_game_object(obj)

        my_mock.foo.assert_called_with(obj)

    def test_create_map_one_tile(self):
        """ Test if a map is created of 1 tile when ring 1 is selected """

        tile = self.game_eng.game_object_factory.create_tile()

        self.game_eng.game_object_factory.create_tile = MagicMock()
        self.game_eng.game_object_factory.create_tile.return_value = tile

        self.game_eng.create_map(1)

        calls = len(self.game_eng.game_object_factory.create_tile.mock_calls)
        self.assertEqual(calls, 1)

    def test_create_map_seven_tiles(self):
        """ Test if a map is created of 7 tile when ring 2 is selected """

        tile = self.game_eng.game_object_factory.create_tile()

        self.game_eng.game_object_factory.create_tile = MagicMock()
        self.game_eng.game_object_factory.create_tile.return_value = tile

        self.game_eng.create_map(2)

        calls = len(self.game_eng.game_object_factory.create_tile.mock_calls)
        self.assertEqual(calls, 7)

    def test_get_game_object_call(self):
        """ Test if getting the game object returns an object """

        obj = self.game_eng.game_object_factory.create_game_object()

        self.game_eng.add_game_object(obj)

        fetched_obj = self.game_eng.get_game_object(obj.object_id)

        self.assertEqual(fetched_obj, obj)

    def test_update(self):
        """ Test the update call """

        obj = self.game_eng.game_object_factory.create_ant()

        self.game_eng.add_game_object(obj)

    def test_initialize_objects(self):
        """ Test if any objects are created """

        self.game_eng.initialize_objects()

        self.assertTrue(len(self.game_eng.objects) > 0)

if __name__ == '__main__':
    unittest.main(verbosity=1)
