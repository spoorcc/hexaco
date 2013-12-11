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

 Render Component Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Base class for a Render component """

from Component import Component

class RenderComponent( Component ):
    """A Render component has a color and a shape
    """

    def __init__(self, parent):
        self.parent = parent
        self.visible = True
        self.color = "#ffff00"
        self.fill = "#ffffff"
        self.width = 0.5
        self.polygon = [ 0, 0, 10, 0, 10, 10, 0, 10 ]
        self.renderID = -1
      
