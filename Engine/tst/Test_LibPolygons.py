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

from ..LibPolygons import *


class TestGameObjectFactory(unittest.TestCase):
    """Test object for GameObjectFactory"""

    def test_give_point_on_circle(self):
        """ Test if the correct coordinates are returned
            input angle 30 degrees and radius of 1 """

        coordinates = give_point_on_circle(30, 1)

        self.assertAlmostEqual(coordinates[0], 0.866, 3)
        self.assertAlmostEqual(coordinates[1], 0.5, 3)

    def test_create_hexagon_radius_one(self):
        """ Test if the correct x,y coordinates are returned
        when asking for a hexagon of radius 1 """

        hexagon = create_hexagon(1)
        # Coordinates [ x0, y0, x1, y1, ... xN, yN ]
        expected = [1.0,  0.0,
                    0.5,  0.866,
                    -0.5,  0.866,
                    -1.0,  0.0,
                    -0.5, -0.866,
                    0.5, -0.866]

        for i in range(len(hexagon)):
            self.assertAlmostEqual(hexagon[i], expected[i], 3,
                                   "%.3f != %.3f @ %d" % (hexagon[i],
                                                          expected[i], i))

    def test_create_hexagon_radius_20(self):
        """ Test if the correct x,y coordinates are returned
        when asking for a hexagon of radius 20 """

        hexagon = create_hexagon(20)

        # Coordinates [ x0, y0, x1, y1, ... xN, yN ]
        expected = [20.0,   0.0,
                    10.0,  17.321,
                    -10.0,  17.321,
                    -20.0,   0.0,
                    -10.0, -17.321,
                    10.0, -17.321]

        for i in range(len(hexagon)):
            self.assertAlmostEqual(hexagon[i], expected[i], 3,
                                   "%.3f != %.3f @ %d" % (hexagon[i],
                                                          expected[i], i))

if __name__ == '__main__':
    unittest.main(verbosity=1)
