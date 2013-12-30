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

 Pheromone Engine Test Class

########################################################################

Description
-----------
"""

import unittest
from mock import MagicMock

from ..PheromoneEngine import PheromoneEngine
from Engine.GameObject import GameObject
from Engine.Components.PositionComponent import PositionComponent
from Engine.Components.PheromoneSenseComponent import PheromoneSenseComponent
from Engine.Components.PheromoneComponent import PheromoneComponent

class TestPheromoneEngine(unittest.TestCase):
    """Test object for PheromoneEngine"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.phero_eng = PheromoneEngine()
        cls.obj_id = 0

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def dummy_phero_holder(self):
        """Returns a dummy pheromone holder"""
        obj = GameObject(self)
        obj.object_id = self.obj_id
        obj.components['pheromone_holder'] = PheromoneComponent(obj)
        obj.components['position'] = PositionComponent(obj)

        self.obj_id += 1

        return obj

    def dummy_phero_actor(self):
        """Returns a dummy pheromone actor"""
        obj = GameObject(self)
        obj.object_id = self.obj_id
        obj.components['pheromone_actor'] = PheromoneSenseComponent(obj)
        obj.components['position'] = PositionComponent(obj)

        self.obj_id += 1

        return obj

    def setUp(self):
        "This method is called befire each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        self.phero_eng.holders = []
        self.phero_eng.actors = []

    #######################################################

    def test_singleton_property(self):
        """ Test if the singleton pattern is hold """
        phero_eng_1 = PheromoneEngine()
        phero_eng_2 = PheromoneEngine()

        self.assertEqual(id(phero_eng_1), id(phero_eng_2))

    def test_add_holder_valid(self):
        """ Test if adding a valid object succeeds """

        obj = MagicMock()
        obj.components = {}
        obj.object_id = 115
        obj.components['pheromone_holder'] = PheromoneComponent(obj)

        self.phero_eng.add_component(obj)

        obj_id = self.phero_eng.holders[0]

        self.assertEqual(obj_id, 115)

    def test_add_actor_valid(self):
        """ Test if adding a valid object succeeds """

        obj = MagicMock()
        obj.components = {}
        obj.object_id = 115
        obj.components['pheromone_actor'] = PheromoneSenseComponent(obj)

        self.phero_eng.add_component(obj)

        obj_id = self.phero_eng.actors[0]

        self.assertEqual(obj_id, 115)

    def test_add_game_object_invalid(self):
        """ Test if adding an invalid object fails """

        self.phero_eng.add_component("not an object")
        self.assertEqual(len(self.phero_eng.holders), 0)
        self.assertEqual(len(self.phero_eng.actors), 0)

    def test_get_levels_xyz_1_neigbour(self):
        """ Test if the pherome levels of all available neighbours are got """

        tile_1 = self.dummy_phero_holder()
        tile_1.components['position'].pos.set_position_xyz(0, 0, 0)
        tile_1.components['pheromone_holder'].level = 1.0

        tile_2 = self.dummy_phero_holder()
        tile_2.components['position'].pos.set_position_xyz(1, -1, 0)
        tile_2.components['pheromone_holder'].level = 3.0

        self.phero_eng.add_component(tile_1)
        self.phero_eng.add_component(tile_2)

        levels = self.phero_eng.get_levels_xyz((0, 0, 0))

        self.assertListEqual(levels, (3.0, None, None, None, None, None))

    def test_get_levels_xyz_2_neigbours(self):
        """ Test if the pherome levels of all available neighbours are got """

        tile_1 = self.dummy_phero_holder()
        tile_1.components['position'].pos.set_position_xyz(0, 0, 0)
        tile_1.components['pheromone_holder'].level = 1.0

        tile_2 = self.dummy_phero_holder()
        tile_2.components['position'].pos.set_position_xyz(1, -1, 0)
        tile_2.components['pheromone_holder'].level = 3.0

        tile_3 = self.dummy_phero_holder()
        tile_3.components['position'].pos.set_position_xyz(1, 0, -1)
        tile_3.components['pheromone_holder'].level = 4.0

        self.phero_eng.add_component(tile_1)
        self.phero_eng.add_component(tile_2)

        levels = self.phero_eng.get_levels_xyz((0, 0, 0))

        self.assertListEqual(levels, (3.0, 4.0, None, None, None, None))

    def test_get_levels_xyz_6_neigbours(self):
        """ Test if the pherome levels of all available neighbours are got """

        center_tile = self.dummy_phero_holder()
        center_tile.components['position'].pos.set_position_xyz(0, 0, 0)
        center_tile.components['pheromone_holder'].level = 1.0

        center_pos = center_tile.components['position'].pos

        for i in range(6):
            tile = self.dummy_phero_holder()

            tile.components['position'].pos = \
                center_pos.get_neighbour(direction=i)

            tile.components['pheromone_holder'].level = float(i)
            self.phero_eng.add_component(tile)

        levels = self.phero_eng.get_levels_xyz(center_pos.xyz())

        self.assertListEqual(levels, (0.0, 1.0, 2.0, 3.0, 4.0, 5.0))

    def test_deposit_pheromone(self):
        """ Test if an object can deposit pheromones on a
        pheromone holder """

        unittest.expectedFailure("Tested behaviour a \
                                 long way from being done")

        self.phero_eng.add_component(self.dummy_phero_actor)
        self.phero_eng.add_component(self.dummy_phero_holder)

        self.dummy_phero_actor.deposit = 1.0

        self.dummy_phero_holder.level = 0.0
        self.dummy_phero_holder.decay = 0.0

        self.phero_eng.update_map()

        self.assertEqual(self.dummy_phero_holder.level, 1.0)

if __name__ == '__main__':
    unittest.main(verbosity=1)