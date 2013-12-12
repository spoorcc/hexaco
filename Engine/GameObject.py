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

 Game Object Class

########################################################################

Description
-----------
Base class for a game object """


class GameObject(object):
    """A single Gameobject on a hexagonal field
        Has a position and a visible attribute.
    """

    def __init__(self, parent):
        self.parent = parent
        self.name = "Default"
        self.object_id = -1
        self.components = {}

    def update(self):
        """ Is called after each turn to let the object perform an action """
        pass
