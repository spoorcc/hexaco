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

    def set_position_xyz(self, xpos, ypos, zpos):
        """ Sets the xyz position """

        return self.pos.set_position_xyz(xpos, ypos, zpos)

    def center_of_tile(self):
        """ Returns a boolean which indicates if the current coordinate
        is in the center of a tile"""
        return (self.is_float_int(self.pos.x) and
                self.is_float_int(self.pos.y) and
                self.is_float_int(self.pos.z))

    def is_float_int(self, number):
        """ Returns a boolean which indicates if a float is an integer"""
        return (abs(float('%.2f' % number)-float('%.f' % number)) < 0.001)
        #return ( ceil(number) == number or floor(number) == number )
        #return ( self.round_float( number, 3 ) == float( int( number)))
