
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import Burner, FlowStation



class BurnerTestCase(unittest.TestCase):

  

    def tearDown(self): 
        comp = None

    def test_burner(self): 
    	   
    	# initial test case based on JT9D 34000 .8 operation    
    	self.burner = set_as_top(Burner())
        self.fs = FlowStation()
        self.fs.W = 101.57
        self.fs.setDryAir()
        self.fs.setTotalTP( 1209.83, 125.611 )
        
        burner = self.burner
        burner.ID_fuel = 3
        burner.hFuel = -1200
        burner.Wfuel = 1.899
        burner.dPqP = .055
        
        burner.Fl_I = self.fs
        burner.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self, burner.Fl_O.W, 103.47, TOL )
        assert_rel_error( self, burner.Fl_O.Pt, 118.702, TOL )
        assert_rel_error( self, burner.Fl_O.Tt, 2370.00, TOL )
 

if __name__ == "__main__":
    unittest.main()
    