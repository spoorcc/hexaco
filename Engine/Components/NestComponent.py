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

 Food Component Class

########################################################################

Description
-----------
Class for a Food component.
Nest component gives game_objects the ability to be a nest """

from Engine.Components.Component import Component


class NestComponent(Component):
    """An Nest component
    """

    def __init__(self, parent):
        super(NestComponent, self).__init__(parent)
        self.parent = parent

        self.amount_of_ants = 0
