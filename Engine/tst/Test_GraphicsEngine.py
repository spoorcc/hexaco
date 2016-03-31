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

 Graphics Engine Test Class

########################################################################

Description
-----------
"""

import unittest
from sys import version_info
from mock import MagicMock

from copy import deepcopy

from ..GraphicsEngine import GraphicsEngine
from ..GameObject import GameObject
from ..Components import RenderComponent
from ..Components import PositionComponent


###################################################################
#
# Test Code
#
###################################################################

class TestGraphicsEngine(unittest.TestCase):
    """Test object for GameEngine"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.graph_eng = GraphicsEngine(None)
        cls.graph_eng.set_window_size(800, 600)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"
        self.graph_eng = GraphicsEngine(None)
        self.graph_eng.set_window_size(800, 600)

        self.dummy_game_object = GameObject(None)
        self.dummy_game_object.components['position'] = PositionComponent(None)
        self.dummy_game_object.components['render'] = RenderComponent(None)

    def tearDown(self):
        "This method is called after each test case"
        self.graph_eng.objects = []

    #######################################################

    @unittest.skipIf(version_info < (3, 0),
                     "singleton construction does not work in 2.7")
    def test_singleton_property(self):
        """ Test if the singleton pattern is hold """
        graph_eng_1 = GraphicsEngine(None)
        graph_eng_2 = GraphicsEngine(None)

        self.assertEqual(id(graph_eng_1), id(graph_eng_2))

    def test_test_class_constants(self):
        """ Assure the constants used by the test class are correct """

        self.assertEqual(self.graph_eng.size, [800, 600])
        self.assertEqual(self.graph_eng.center_screen_coordinate, [400, 300])

    def test_set_window_size(self):
        """ Assure setting window size succeeds """

        grph_eng = GraphicsEngine(None)
        grph_eng.set_window_size(800, 600)

        self.assertEqual(grph_eng.size, [800, 600])

    def test_game_2_screen_coords_case1(self):
        """ It is assumed this calculation has no side effects,
        this method tests this """

        [s_X, s_Y] = self.graph_eng.size

        [x, y] = self.graph_eng.game_to_screen_coordinates(0, 0, 0)

        self.assertEqual(self.graph_eng.size, [s_X, s_Y],
                         "Screen size changed")

    def test_add_game_object_valid(self):
        """ Test if adding a valid object succeeds """

        obj = MagicMock()
        obj.components = {}
        obj.object_id = 115
        obj.components['render'] = RenderComponent(obj)
        obj.components['position'] = PositionComponent(obj)

        self.assertEqual(len(self.graph_eng.objects), 0)
        self.graph_eng.add_component(obj)

        obj_actual = self.graph_eng.objects[0]

        self.assertEqual(obj_actual, [obj.components['render'], obj.components['position'].pos] )

    def test_add_game_object_invalid(self):
        """ Test if adding an invalid object fails """

        self.graph_eng.add_component("not an object")
        self.assertEqual(len(self.graph_eng.objects), 0)

    def test_place_object(self):
        """ Test if moving an object succeeds with
        different x,y coordinates """

        coordinates = [100, 100, 50, 50]
        actual = self.graph_eng.place_object(coordinates, 10, 5)

        self.assertEqual(actual, [110, 105, 60, 55])

    def test_game_to_screen_coordinates_center(self):
        """ Test if setting game coordinate 0, 0, 0 ends in the center """

        self.assertEqual(self.graph_eng.center_screen_coordinate,
                         [400, 300])

        [x, y] = self.graph_eng.game_to_screen_coordinates(0, 0, 0)

        self.assertEqual([x, y], self.graph_eng.center_screen_coordinate)

    def test_game_to_screen_coordinates_1_0_m1(self):
        """ Test if x1 y0 z-1 ends in the correct position """

        [x, y] = self.graph_eng.game_to_screen_coordinates(1, 0, -1)

        expected = self.graph_eng.center_screen_coordinate

        expected[0] += 0 * self.graph_eng.screen_x_offset
        expected[1] += -2 * self.graph_eng.screen_y_offset

        self.assertAlmostEqual(x, expected[0], 3)
        self.assertAlmostEqual(y, expected[1], 3)

    def test_game_to_screen_coordinates_m2_2_0(self):
        """ Test known game to screen coordinates x -2 y 2 z 0"""

        [x, y] = self.graph_eng.game_to_screen_coordinates(-2, 2, 0)

        expected = self.graph_eng.center_screen_coordinate

        expected[0] += 2 * self.graph_eng.screen_x_offset
        expected[1] += 2 * self.graph_eng.screen_y_offset

        self.assertAlmostEqual(x, expected[0], 3)
        self.assertAlmostEqual(y, expected[1], 3)

    def test_game_to_screen_coordinates_m2_3_m1(self):
        """ Test known game to screen coordinates x -2 y 3 z -1"""

        [x, y] = self.graph_eng.game_to_screen_coordinates(-2, 3, -1)

        expected = self.graph_eng.center_screen_coordinate

        expected[0] += 3 * self.graph_eng.screen_x_offset
        expected[1] += 1 * self.graph_eng.screen_y_offset

        self.assertAlmostEqual(x, expected[0], 3)
        self.assertAlmostEqual(y, expected[1], 3)

    def test_render_component_not_affected_by_drawing(self):
        """  """

        polygon = self.dummy_game_object.components['render'].polygon
        polygon_copy = deepcopy(polygon)
        self.graph_eng.add_component(self.dummy_game_object)

        rend_comp = self.dummy_game_object.components['render']
        self.assertEqual( rend_comp.polygon, polygon_copy)

    def test_set_turn_text(self):
        """ Test if the turn text is set """
        self.graph_eng.win = MagicMock()
        self.graph_eng.win.itemconfigure = MagicMock()

        self.graph_eng.set_turn_text("Some text")

        mthd = self.graph_eng.win.itemconfigure
        mthd.assert_called_with(self.graph_eng.turn_text, text="Some text")

if __name__ == '__main__':
    unittest.main(verbosity=1)
