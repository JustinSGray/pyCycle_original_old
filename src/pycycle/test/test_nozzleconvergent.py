
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import NozzleConvergent, FlowStation



class NozzleConvergentCase(unittest.TestCase):

  

    def tearDown(self): 
        comp = None

    def test_nozzleconvergent(self): 
    	   
    	# initial test case based on JT9D 34000 .8 operation    
    	# choked
        self.nozz = set_as_top(NozzleConvergent())
        self.fs = FlowStation()
        self.fs.W = 562.61
        self.fs.setTotalTP( 527.55, 8.978 );
        
        nozz = self.nozz       
        nozz.Fl_I = self.fs 
        nozz.Cfg = .9962
        nozz.PsExh = 3.626
        nozz.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self, nozz.Fg, 21033.3, TOL )
   
   	# initial test case based on JT9D 0. 0. operation    
    	# unchoked
        self.nozz = set_as_top(NozzleConvergent())
        self.fs = FlowStation()
        self.fs.W = 1293.91
        self.fs.setTotalTP( 632.71, 23.195 );
        
        nozz = self.nozz       
        nozz.Fl_I = self.fs 
        nozz.Cfg = .9975
        nozz.PsExh = 14.696
        nozz.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self, nozz.Fg, 38786, TOL )
   
if __name__ == "__main__":
    unittest.main()
    