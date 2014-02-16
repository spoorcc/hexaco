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

 Position Component Class

########################################################################

Description
-----------
Class for a position component """

from Engine.Components.Component import Component
from ..HexagonalPosition import HexagonalPosition

from Engine.LibCommon import is_float_int


class PositionComponent(Component):
    """A Move component has a position
    """

    def __init__(self, parent):
        super(PositionComponent, self).__init__(parent)
        self.parent = parent
        self.pos = HexagonalPosition(self)
        self.orientation = 0

    def xyz(self):
        """ Returns the xyz position as list"""

        return [self.pos.x, self.pos.y, self.pos.z]

    def set_position_xyz(self, xyz_pos):
        """ Sets the xyz position """

        return self.pos.set_position_xyz(xyz_pos[0],
                                         xyz_pos[1],
                                         xyz_pos[2])

    def center_of_tile(self):
        """ Returns a boolean which indicates if the current coordinate
        is in the center of a tile"""

        return (is_float_int(self.pos.x) and
                is_float_int(self.pos.y) and
                is_float_int(self.pos.z))
