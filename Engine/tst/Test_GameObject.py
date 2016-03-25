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

 Game Object Test Class

########################################################################

Description
-----------
"""

import unittest
from ..GameObject import GameObject
from ..Components.Component import Component


###################################################################
#
# Test Code
#
###################################################################

class TestGameObject(unittest.TestCase):
    """Test object for GameObject"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.gameObj = GameObject(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"
        pass

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_defaultName(self):
        """ The object must have "Default" as default name"""

        self.assertEqual(self.gameObj.name, "Default")

    def test_addComponent_default(self):
        """ Adding a component should be handled by the object """

        comp = Component(None)
        self.gameObj.add_component('some_comp', comp)

        self.assertEqual(self.gameObj.components['some_comp'], comp)

    def test_addComponent_non_valid(self):
        """ Adding a component should be handled by the object """

        with self.assertRaises(TypeError):
            self.gameObj.add_component('some_comp', 'not a component')

    def test_add_component_adds_components_handle(self):
        """ Components should be able to call other components
            within the same object """

        comp_a = Component(None)
        comp_b = Component(None)

        self.gameObj.add_component('a', comp_a)
        self.gameObj.add_component('b', comp_b)

        self.assertEqual(comp_a.components['b'], comp_b)
        self.assertEqual(comp_b.components['a'], comp_a)

if __name__ == '__main__':
    unittest.main(verbosity=1)
