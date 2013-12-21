
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import turbine_prmap, flowstation

class TurbineTestCase(unittest.TestCase):


  

    def test_turbine(self): 
    	    
    	self.turbine = set_as_top(turbine_prmap.TurbinePRmap())

        self.fs = flowstation.FlowStation()
        self.fs._species=[.9816,0,.018355,0,0,0,0]
        self.fs.W = 103.47
        self.fs.setTotalTP( 2371.94, 119.086 )
     
        self.b1 = flowstation.FlowStation()
        self.b1.W = 6.1386
        self.b1.setTotalTP( 1211.05, 126.017 )

        self.b2 = flowstation.FlowStation()
        self.b2.W = 3.9064
        self.b2.setTotalTP( 1211.05, 126.017 )
        
        turbine = self.turbine
        turbine.eff = .9133
        turbine.PR = 2.670
        turbine.Nmech = 8000.
        
        turbine.Fl_I = self.fs
        turbine.Fl_bld1 = self.b1
        turbine.Fl_bld2 = self.b2        
        turbine.run()
        TOL = .001

        assert_rel_error( self,turbine.Fl_O.W, 113.51, TOL )
        assert_rel_error( self,turbine.Fl_O.Pt, 44.60, TOL )
        assert_rel_error( self,turbine.Fl_O.Tt, 1850.6, TOL )
        
        
        assert_rel_error( self,turbine.pwr, 19684, TOL )
        assert_rel_error( self,turbine.trq, 1353.2, TOL )

if __name__ == "__main__":
    unittest.main()
    