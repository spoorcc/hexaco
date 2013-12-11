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

from Component import Component

class MoveComponent( Component ):
    """A Move component 
    """

    def __init__(self, parent):
        self.parent = parent
        self.speed = 0.0

        

    def get_xyz_speed(self, orientation):

        speed_mat = [ [1,-1,0], [1,0,-1], [0,1,-1], [-1,1,0], [-1,0,1], [0,-1,1] ]

        xyz_speed = speed_mat[ orientation ]

        return [x*self.speed for x in xyz_speed] 
