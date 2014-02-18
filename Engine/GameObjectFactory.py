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


from Engine.LibPolygons import create_triangle, create_hexagon, create_octagon

from Engine.GameObject import GameObject

from Engine.Components import RenderComponent
from Engine.Components import MoveComponent
from Engine.Components import PositionComponent
from Engine.Components import AiComponent
from Engine.Components import PheromoneActorComponent
from Engine.Components import PheromoneHolderComponent

from Engine.GameSettings import HEX_RADIUS, ANT_DEFAULTS


class GameObjectFactory(object):
    """The ObjectFactory which construcs game objects
    """

    def __init__(self, parent):
        self.parent = parent
        self.hex_radius = HEX_RADIUS
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

        size = 0.4 * self.hex_radius
        obj.components['render'].polygon = create_triangle(size)

        obj.components['position'] = PositionComponent(obj)
        obj.components['position'].orientation = 3

        obj.add_component('move', MoveComponent(parent=obj,
                                                speed=ANT_DEFAULTS['SPEED']))
        obj.add_component('ai', AiComponent(obj))

        obj.components['pheromone_actor'] = PheromoneActorComponent(obj)
        obj.components['pheromone_actor'].deposit["food"] \
                                        = ANT_DEFAULTS['DEPOSIT_FOOD']
        obj.components['pheromone_actor'].deposit["home"] \
                                        = ANT_DEFAULTS['DEPOSIT_HOME']

        return obj

    def create_tile(self):
        """ Returns a newly created tile """

        obj = self.create_game_object()
        obj.components['render'] = RenderComponent(obj)
        obj.components['render'].color = "#005500"
        obj.components['render'].fill = "#220000"
        obj.components['render'].polygon = create_hexagon(self.hex_radius)

        obj.components['position'] = PositionComponent(obj)

        obj.components['pheromone_holder'] = PheromoneHolderComponent(obj)
        obj.components['pheromone_holder'].decay = 0.8

        return obj
