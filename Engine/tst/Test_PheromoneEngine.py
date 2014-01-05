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

from Engine.LibHexagonalPosition import get_neighbour_xyz

from ..PheromoneEngine import PheromoneEngine
from Engine.GameObject import GameObject
from Engine.Components import PositionComponent
from Engine.Components import PheromoneHolderComponent
from Engine.Components import PheromoneActorComponent


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
        obj.components['pheromone_holder'] = PheromoneHolderComponent(obj)
        obj.components['position'] = PositionComponent(obj)

        self.obj_id += 1

        return obj

    def dummy_phero_actor(self):
        """Returns a dummy pheromone actor"""
        obj = GameObject(self)
        obj.object_id = self.obj_id
        obj.components['pheromone_actor'] = PheromoneActorComponent(obj)
        obj.components['position'] = PositionComponent(obj)

        self.obj_id += 1

        return obj

    def setUp(self):
        "This method is called befire each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        self.phero_eng.__init__()

    #######################################################

    def test_singleton_property(self):
        """ Test if the singleton pattern is hold """
        phero_eng_1 = PheromoneEngine()
        phero_eng_2 = PheromoneEngine()

        self.assertEqual(id(phero_eng_1), id(phero_eng_2))

    def test_add_holder_valid(self):
        """ Test if adding a valid object succeeds """

        holder = self.dummy_phero_holder()
        self.phero_eng.add_component(holder)

        self.assertEqual(len(set(self.phero_eng.holders)), 1)

    def test_add_multiple_holders_valid(self):
        """ Test if adding multiple valid object succeeds """

        count = 6

        for i in range(count):
            holder = self.dummy_phero_holder()
            holder.components['position'].set_position_xyz((i, -i, 0))
            self.phero_eng.add_component(holder)

        self.assertEqual(len(set(self.phero_eng.holders)), count)

    def test_add_actor_valid(self):
        """ Test if adding a valid object succeeds """

        actor = self.dummy_phero_actor()
        self.phero_eng.add_component(actor)

        self.assertEqual(len(set(self.phero_eng.actors)), 1)

    def test_add_multiple_actors_valid(self):
        """ Test if adding multiple valid object succeeds """

        count = 50

        for i in range(count):
            actor = self.dummy_phero_actor()
            self.phero_eng.add_component(actor)

        self.assertEqual(len(self.phero_eng.actors), count)

    def test_add_game_object_invalid(self):
        """ Test if adding an invalid object fails """

        self.phero_eng.add_component("not an object")
        self.assertEqual(len(self.phero_eng.holders), 0)
        self.assertEqual(len(self.phero_eng.actors), 0)

    def test_get_levels_xyz_1_neigbour(self):
        """ Test if the pherome levels of all available neighbours are got """

        tile_1 = self.dummy_phero_holder()
        tile_1.components['position'].set_position_xyz((0, 0, 0))
        tile_1.components['pheromone_holder'].levels["food"] = 1.0
        tile_1.components['pheromone_holder'].levels["home"] = 10.0

        tile_2 = self.dummy_phero_holder()
        tile_2.components['position'].set_position_xyz((1, -1, 0))
        tile_2.components['pheromone_holder'].levels["food"] = 3.0
        tile_2.components['pheromone_holder'].levels["home"] = 30.0

        self.phero_eng.add_component(tile_1)
        self.phero_eng.add_component(tile_2)

        self.phero_eng.get_game_object = MagicMock()
        self.phero_eng.get_game_object.return_value = tile_2

        levels = self.phero_eng.get_levels_xyz((0, 0, 0))

        self.assertListEqual(levels["food"],
                             [3.0, None, None, None, None, None])

        self.assertListEqual(levels["home"],
                             [30.0, None, None, None, None, None])

    def test_get_levels_xyz_2_neigbours(self):
        """ Test if the pherome levels of all available neighbours are got """

        tile_1 = self.dummy_phero_holder()
        tile_1.components['position'].set_position_xyz((0, 0, 0))
        tile_1.components['pheromone_holder'].levels["food"] = 1.0
        tile_1.components['pheromone_holder'].levels["home"] = 10.0

        tile_2 = self.dummy_phero_holder()
        tile_2.components['position'].set_position_xyz((1, -1, 0))
        tile_2.components['pheromone_holder'].levels["food"] = 3.0
        tile_2.components['pheromone_holder'].levels["home"] = 30.0

        tile_3 = self.dummy_phero_holder()
        tile_3.components['position'].set_position_xyz((1, 0, -1))
        tile_3.components['pheromone_holder'].levels["food"] = 4.0
        tile_3.components['pheromone_holder'].levels["home"] = 40.0

        self.phero_eng.add_component(tile_1)
        self.phero_eng.add_component(tile_2)
        self.phero_eng.add_component(tile_3)

        objects = {tile_1.object_id: tile_1,
                   tile_2.object_id: tile_2,
                   tile_3.object_id: tile_3}

        def get_game_object(arg):
            """ Returns object """
            return objects[arg]

        self.phero_eng.get_game_object = MagicMock(side_effect=get_game_object)

        levels = self.phero_eng.get_levels_xyz((0, 0, 0))

        self.assertListEqual(levels["food"],
                             [3.0, 4.0, None, None, None, None])

        self.assertListEqual(levels["home"],
                             [30.0, 40.0, None, None, None, None])

    def test_get_levels_xyz_6_neigbours(self):
        """ Test if the pherome levels of all available neighbours are got """

        center_tile = self.dummy_phero_holder()
        center_tile.components['position'].set_position_xyz((0, 0, 0))
        center_tile.components['pheromone_holder'].level = 1.0

        center_pos = center_tile.components['position'].pos
        objects = dict()

        for i in range(6):
            tile = self.dummy_phero_holder()

            neighbour = get_neighbour_xyz(center_pos.xyz, direction=i)
            tile.components['position'].set_position_xyz(neighbour)

            tile.components['pheromone_holder'].levels["food"] = float(i)
            tile.components['pheromone_holder'].levels["home"] = float(i) * 10
            self.phero_eng.add_component(tile)

            objects[tile.object_id] = tile

        def get_game_object(arg):
            """ Returns object """
            return objects[arg]

        self.phero_eng.get_game_object = MagicMock(side_effect=get_game_object)

        levels = self.phero_eng.get_levels_xyz(center_pos.xyz)

        self.assertListEqual(levels["food"],
                             [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])

        self.assertListEqual(levels["home"],
                             [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])

    @unittest.expectedFailure
    def test_deposit_pheromone(self):
        """ Test if an object can deposit pheromones on a
        pheromone holder """

        self.phero_eng.add_component(self.dummy_phero_actor)
        self.phero_eng.add_component(self.dummy_phero_holder)

        self.dummy_phero_actor.deposit["home"] = 1.0

        self.dummy_phero_holder.levels["home"] = 0.0
        self.dummy_phero_holder.decay = 0.0

        self.phero_eng.update_map()

        self.assertEqual(self.dummy_phero_holder.level, 1.0)

    def test_update_actors(self):
        """ Test if the actor gets the proper levels """

        # Store objects locally, to mock out the game engine
        objects = dict()

        center_tile = self.dummy_phero_holder()
        center_tile.components['position'].set_position_xyz((0, 0, 0))
        center_tile.components['pheromone_holder'].level = 1.0

        objects[center_tile.object_id] = center_tile

        center_pos = center_tile.components['position'].pos

        # Create a map of one ring surrounding the center tile
        for i in range(6):
            tile = self.dummy_phero_holder()

            neighbour = get_neighbour_xyz(center_pos.xyz, direction=i)
            tile.components['position'].set_position_xyz(neighbour)

            tile.components['pheromone_holder'].levels["food"] = float(i)
            tile.components['pheromone_holder'].levels["home"] = float(i) * 10
            self.phero_eng.add_component(tile)

            objects[tile.object_id] = tile

        def get_game_object(arg):
            """ Returns object """
            return objects[arg]

        # Mock out the game_engine method
        self.phero_eng.get_game_object = MagicMock(side_effect=get_game_object)

        actor = self.dummy_phero_actor()

        objects[actor.object_id] = actor

        self.phero_eng.add_component(actor)

        self.phero_eng.update_actors()

        levels = actor.components["pheromone_actor"].neighbour_levels

        self.assertListEqual(levels["food"],
                             [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])

        self.assertListEqual(levels["home"],
                             [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])

    def test_update_actors_actor_on_non_int_coords(self):
        """ Test if the actor gets the proper levels even
         if on non-int coords"""

        # Store objects locally, to mock out the game engine
        objects = dict()

        center_tile = self.dummy_phero_holder()
        center_tile.components['position'].set_position_xyz((0, 0, 0))
        center_tile.components['pheromone_holder'].level = 1.0

        objects[center_tile.object_id] = center_tile

        center_pos = center_tile.components['position'].pos

        # Create a map of one ring surrounding the center tile
        for i in range(6):
            tile = self.dummy_phero_holder()

            neighbour = get_neighbour_xyz(center_pos.xyz, direction=i)
            tile.components['position'].set_position_xyz(neighbour)

            tile.components['pheromone_holder'].levels["food"] = float(i)
            tile.components['pheromone_holder'].levels["home"] = float(i) * 10
            self.phero_eng.add_component(tile)

            objects[tile.object_id] = tile

        def get_game_object(arg):
            """ Returns object """
            return objects[arg]

        # Mock out the game_engine method
        self.phero_eng.get_game_object = MagicMock(side_effect=get_game_object)

        actor = self.dummy_phero_actor()
        actor.components['position'].set_position_xyz((-0.6, 0.6, 0.0))

        objects[actor.object_id] = actor

        self.phero_eng.add_component(actor)

        self.phero_eng.update_actors()

        levels = actor.components["pheromone_actor"].neighbour_levels

        self.assertListEqual(levels["food"],
                             [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])

        self.assertListEqual(levels["home"],
                             [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])

if __name__ == '__main__':
    unittest.main(verbosity=1)
