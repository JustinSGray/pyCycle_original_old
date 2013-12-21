
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import Inlet, FlowStation



class InletTestCase(unittest.TestCase):

  

    def tearDown(self): 
        comp = None

    def test_duct(self): 
    	   
    	# initial test case based on JT9D 34000 .8 operation    
    	self.inlet = set_as_top(Inlet())
        self.fs = FlowStation()
        self.fs.W = 100.
        self.fs.setTotalTP( 1000, 100 );
        
        inlet = self.inlet       
        inlet.Fl_I = self.fs 
        inlet.ram_recovery = .9
        inlet.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self, inlet.Fl_O.W, 100., TOL )
        assert_rel_error( self, inlet.Fl_O.Pt, 90., TOL )
        assert_rel_error( self, inlet.Fl_O.Tt, 1000., TOL )

if __name__ == "__main__":
    unittest.main()
    