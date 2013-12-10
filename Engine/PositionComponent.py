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

 Position Component Class
 including Unit test class

 * Run file separate to run unit tests

########################################################################

Description
-----------
Class for a position component """

import unittest
from Component import Component
from HexagonalPosition import HexagonalPosition

from math import ceil, floor, fmod

class PositionComponent( Component ):
    """A Move component has a position
    """

    def __init__(self, parent):
        self.parent = parent
        self.pos = HexagonalPosition( self )
        self.orientation = 0

    def xyz(self):
		""" Returns the xyz position as list"""

		return [self.pos.x, self.pos.y, self.pos.z]    

    def center_of_tile( self ):
        return (self.is_float_int(self.pos.x) and self.is_float_int(self.pos.y) and self.is_float_int(self.pos.z) )

    def is_float_int(self, number ):
		return ( abs(float('%.2f'%number)-float('%.f'%number) ) < 0.001 )
        #return ( ceil(number) == number or floor(number) == number )
        #return ( self.round_float( number ) == float( int( number ) ) )
        
    def round_float(self, number):
        return round( number, 3 )
           
###################################################################
#
# Test Code
#
###################################################################

class TestPositionComponent(unittest.TestCase):

    ######################################################

    @classmethod
    def setUpClass(cls):
        "This method is called once, when starting the tests"
        cls.posComp = PositionComponent(None)

    @classmethod
    def tearDownClass(cls):
        "This method is called after finishing all tests"
        pass

    #######################################################

    def setUp(self):
        "This method is called before each test case"
        self.posComp.pos.x = 0.0
        self.posComp.pos.y = 0.0
        self.posComp.pos.z = 0.0

    def tearDown(self):
        "This method is called after each test case"
        pass

    #######################################################

    def test_defaultPosition(self):

        self.assertEqual( self.posComp.pos.x, 0.0 )
        self.assertEqual( self.posComp.pos.y, 0.0 )
        self.assertEqual( self.posComp.pos.z, 0.0 )

    def test_defaultOrientation(self):

        self.assertEqual( self.posComp.orientation, 0 )

    def test_center_of_tile_valid( self ):

        self.assertTrue( self.posComp.center_of_tile() )

        self.posComp.pos.x = -1.0
        self.posComp.pos.z = 1.0

        self.assertTrue( self.posComp.center_of_tile() )

    def test_center_of_tile_invalid( self ):

        self.posComp.pos.x =  0.01
        self.posComp.pos.y = -0.01
        self.assertFalse( self.posComp.center_of_tile() )

    def test_center_of_tile_series( self ):

        counter = 0

        self.posComp.pos.x = -1.0
        self.posComp.pos.y = 1.0
        
        for i in range( 2555 ):
        
            if self.posComp.center_of_tile():
                counter += 1

            self.posComp.pos.x += 0.01
            self.posComp.pos.y -= 0.01

        self.assertEqual( counter, 26 )

    def test_is_float_int( self ):

        self.assertTrue( self.posComp.is_float_int( -4.0 ) )
        self.assertTrue( self.posComp.is_float_int(  0.0 ) )
        self.assertTrue( self.posComp.is_float_int(  1.0 ) )
        self.assertTrue( self.posComp.is_float_int(  -1.0 ) )
        self.assertTrue( self.posComp.is_float_int(  0.0001 ) )
        self.assertTrue( self.posComp.is_float_int(  -0.0009 ) )

        self.assertFalse( self.posComp.is_float_int(  0.5 ) )
        self.assertFalse( self.posComp.is_float_int(  1.1 ) )
        self.assertFalse( self.posComp.is_float_int( -0.3 ) )
        self.assertFalse( self.posComp.is_float_int( -0.5 ) )
    

                
if __name__ == '__main__':
    unittest.main(verbosity=2)
