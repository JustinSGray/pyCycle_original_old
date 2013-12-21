
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import Duct, FlowStation



class DuctTestCase(unittest.TestCase):

  

    def tearDown(self): 
        comp = None

    def test_duct(self): 
    	   
    	# initial test case based on JT9D 34000 .8 operation    
    	self.duct = set_as_top(Duct())
        self.fs = FlowStation()
        self.fs.W = 100.
        self.fs.setTotalTP( 1000, 100 );
        
        duct = self.duct         
        duct.Fl_I = self.fs 
        duct.dPqP = .1
        duct.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self, duct.Fl_O.W, 100., TOL )
        assert_rel_error( self, duct.Fl_O.Pt, 90., TOL )
        assert_rel_error( self, duct.Fl_O.Tt, 1000., TOL )

if __name__ == "__main__":
    unittest.main()
    