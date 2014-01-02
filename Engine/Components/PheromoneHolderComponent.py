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

 Pheromone Holder Component Class

########################################################################

Description
-----------
Class for a Pheromone Holder component.
Pheromone component gives game_objects the ability to have a pherome level """

from Component import Component


class PheromoneHolderComponent(Component):
    """An Pheromone component
    """

    def __init__(self, parent):
        super(PheromoneHolderComponent, self).__init__(parent)
        self.parent = parent
        self.level = 0.0
        self.decay = 0.0001

    def update(self):
        """ This will update the level of this holder """

        if self.level > 0.0:
            self.level -= self.decay
        else:
            self.level = 0.0
