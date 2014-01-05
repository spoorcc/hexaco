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

 Pheromone Actor Component Class

########################################################################

Description
-----------
Class for a Pheromone Actor component
Gives gameobject the ability to sense pheromone levels around
it and to deposit pheromones """

from Component import Component


class PheromoneActorComponent(Component):
    """An Pheromone sense component
    """

    def __init__(self, parent):
        super(PheromoneActorComponent, self).__init__(parent)
        self.parent = parent

        # Orientation same as in hexagonal position
        self.neighbour_levels = {"food": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                 "home": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
        self.deposit = {"food": 0.0, "home": 0.0}
