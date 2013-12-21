
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import Shaft

class TurbineTestCase(unittest.TestCase):


    def test_shaft(self): 
    	    
    	self.shaft = set_as_top(Shaft())

        shaft = self.shaft
        shaft.trq1 = -10000
        shaft.trq2 = 9000
        
        shaft.run()
        TOL = .001

        assert_rel_error( self,shaft.trqNet, -1000., TOL )

if __name__ == "__main__":
    unittest.main()
    