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

 Collision Component Class

########################################################################

Description
-----------
Class for a Collision component.
Collision component gives game_objects the ability
to collide with other colliding objects """

from Engine.Components.Component import Component


class CollisionComponent(Component):
    """An Collision component
    """

    def __init__(self, parent):
        super(CollisionComponent, self).__init__(parent)
        self.parent = parent

        self.objects_collided_with = []
