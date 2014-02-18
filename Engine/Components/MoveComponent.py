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

 Move Component Class

########################################################################

Description
-----------
Base class for a move component """

from Engine.Components.Component import Component

from Engine.LibCommon import add_delta_to_pos_if_valid

from Engine.GameSettings import EPSILON


class MoveComponent(Component):
    """A Move component
    """

    def __init__(self, parent, speed=0.0):
        super(MoveComponent, self).__init__(parent)
        self.parent = parent
        self.speed = speed

    def get_xyz_speed(self, orientation):
        """ Get the speed in x y z coordinates """

        speed_mat = [[1.0, -1.0, 0.0],  # Top-left
                     [1.0, 0.0, -1.0],  # Top
                     [0.0, 1.0, -1.0],  # Top-right
                     [-1.0, 1.0, 0.0],  # Bottom-right
                     [-1.0, 0.0, 1.0],  # Bottom
                     [0.0, -1.0, 1.0]]  # Bottom-left

        xyz_speed = speed_mat[orientation]

        return [x*self.speed for x in xyz_speed]

    def update(self):
        """ Update all objects with a move component """

        pos_comp = self.components['position']

        # Only do the move computations if there is a movement
        if self.speed >= EPSILON:

            deltas = self.get_xyz_speed(pos_comp.orientation)
            xyz = pos_comp.xyz()

            try:
                xyz = add_delta_to_pos_if_valid(xyz, deltas)

            except ValueError:
                # Turn around if trying to walk off map
                pos_comp.orientation = (pos_comp.orientation + 3) % 6

            pos_comp.set_position_xyz(xyz)
