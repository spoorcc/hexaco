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

 Game Object Factory Class

########################################################################

Description
-----------
Class for constructing Game Objects """

from math import sin, cos, radians

from Engine.GameObject import GameObject

from Engine.Components import RenderComponent
from Engine.Components import MoveComponent
from Engine.Components import PositionComponent
from Engine.Components import AiComponent


class GameObjectFactory(object):
    """The ObjectFactory which construcs game objects
    """

    def __init__(self, parent):
        self.parent = parent
        self.hex_radius = 20
        self.next_object_id = 0

    def create_game_object(self):
        """ Creates an emty object with an unique object_id"""

        obj = GameObject(None)
        obj.object_id = self.next_object_id

        self.next_object_id += 1

        return obj

    def create_ant(self):
        """ Returns a newly created ant with an unique object_id"""

        obj = self.create_game_object()
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#880000"
        obj.components['render'].fill = "#001100"

        # Effectivly returns a triangle
        size = 0.4 * self.hex_radius
        obj.components['render'].polygon = [0, -size,
                                            size, size,
                                            -size, size]

        obj.components['position'] = PositionComponent(obj)
        obj.components['position'].orientation = 3

        obj.components['move'] = MoveComponent(obj)
        obj.components['move'].speed = 0.01

        obj.components['ai'] = AiComponent(obj)

        return obj

    def create_tile(self):
        """ Returns a newly created tile """

        obj = self.create_game_object()
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#005500"
        obj.components['render'].fill = "#220000"
        obj.components['render'].polygon = self.create_hexagon(self.hex_radius)

        obj.components['position'] = PositionComponent(obj)

        return obj

    def give_point_on_circle(self, degrees, radius):
        """ Returns the x,y coordinates of a point on a circle with its center
        at 0,0 and with the given radius """
        return [radius * cos(radians(degrees)), radius * sin(radians(degrees))]

    def create_hexagon(self, radius):
        """ Returns the coordinates of a hexagon where the furthest points lay
        on a circle with its center at 0,0 and with the given radius.
        The coordinates are formatted as [ x0, y0, x1, y1, ... xN, yN ]"""

        coordinates = []
        for i in range(0, 6):
            coordinates += self.give_point_on_circle(i * 60, radius)

        return coordinates
