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

 Game Object Factory Test Class

########################################################################

Description
-----------
"""

import unittest

from ..GameObject import GameObject
from ..GameObjectFactory import GameObjectFactory


class TestGameObjectFactory(unittest.TestCase):
    """Test object for GameObjectFactory"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.gameObjFact = GameObjectFactory(None)

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
        pass

    #######################################################

    def test_create_game_object_rets_obj(self):
        """ Test if creating a game object returns an object"""

        obj = self.gameObjFact.create_game_object()
        self.assertEqual(type(obj), GameObject)

    def test_create_game_obj_unique_ids(self):
        """ Two objects created should never have the same object_id"""

        obj1 = self.gameObjFact.create_game_object()
        obj2 = self.gameObjFact.create_game_object()

        self.assertNotEqual(obj1.object_id, obj2.object_id)

if __name__ == '__main__':
    unittest.main(verbosity=1)
