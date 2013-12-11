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

 Pheromone Engine Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Class for a Pheromone Engine """

import unittest

from GameObject import GameObject
from Components import PheromoneSenseComponent
from Components import PheromoneComponent

class PheromoneEngine(object):
    """The engine managing all pheromones on the map
    """

    _instance = None
    def __new__(cls, *args, **kwargs):
        """ Called when creating new instance, return existing instance
        otherwise create new one, singleton pattern """
        if not cls._instance:
            cls._instance = super(PheromoneEngine, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        
        self.pheromone_objects = []
        self.pheromone_sense_objects = []
    
    def add_component(self, game_object ):
        """ If a object has a pheromone and a position component it is added
        to the list of objects to update """

        if 'pheromone' in game_object.components:
            self.pheromone_objects.append( game_object.objectID )

        if 'pheromone_sense' in game_object.components:
            self.pheromone_sense_objects.append( game_object.objectID )

    def get_game_object(self, objectID ):
        """ This method should be overloaded """
        print "Whooops " 

    def get_levels_xyz( self, xyz ):
        """ Returns all levels of the adjacent tiles of position x, y ,z """

        for object_id in self.pheromone_sense_objects:
            print object_id
        
    def update_map(self):
        """ Update the objects that need pheromone data """

        for object_id in self.pheromone_objects:

            try:
                obj = self.get_game_object( object_id )
                
            except:
                print "Could not find object"
                
            ph_comp  = obj.components['pheromone_sense']
            pos_comp = obj.components['position']

            ph_comp.neighbour_levels = self.get_levels_xyz( pos_comp.xyz )
          

###################################################################
#
# Test Code
#
###################################################################

class TestPheromoneEngine(unittest.TestCase):
    """Test object for PheromoneEngine"""

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.pher_eng = PheromoneEngine(None)
                        
    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called befire each test case"
        self.pher_eng = PheromoneEngine(None)
        
        self.dummy_pher_container = GameObject( None )
        self.dummy_pher_container.components['pheromone'] = PheromoneComponent(None)

        self.dummy_pher_sensor = GameObject( None )
        self.dummy_pher_sensor.components['pheromone_sense'] = PheromoneSenseComponent( None )


    def tearDown(self):
        "This method is called after each test case"
        self.pher_eng.pheromone_objects = []
        self.pher_eng.pheromone_sense_objects = []
        

    #######################################################
    
    def test_add_game_object_valid(self):
        """ Test if adding a valid object succeeds """
                
        self.pher_eng.add_component( self.dummy_pher_container )        
        self.assertEqual( len(self.pher_eng.pheromone_objects ), 1 )

        self.pher_eng.add_component( self.dummy_pher_sensor )        
        self.assertEqual( len(self.pher_eng.pheromone_sense_objects ), 1 )

    def test_add_game_object_invalid(self):
        """ Test if adding an invalid object fails """
        
        self.pher_eng.add_component( "not an object" )
        self.assertEqual( len(self.pher_eng.pheromone_objects ), 0 )
        

if __name__ == '__main__':
    unittest.main(verbosity=1)
