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

 Component Test Class
 
########################################################################

Description
-----------
 """

import unittest
from ..Component import Component

###################################################################
#
# Test Code
#
###################################################################

class TestComponent(unittest.TestCase):

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.comp = Component(None)

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

        self.assertEqual( type( self.comp), Component )

if __name__ == '__main__':
    unittest.main(verbosity=2)
