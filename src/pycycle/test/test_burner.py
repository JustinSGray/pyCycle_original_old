
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import burner, flowstation

class BurnerTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(burner.Burner())

        comp.ID_fuel = 4
        comp.hFuel = -642
        comp.Wfuel = 2.5
        comp.dPqP = .01
   
        fs = flowstation.FlowStation()
        fs.setDryAir()
        fs.W = 100.
        fs.setTotalTP(1100., 400.)
  
        comp.Fl_I = fs

        comp.run()
        
        assert_rel_error(self,comp.Fl_O.W, 102.5, .005)
        assert_rel_error(self,comp.Fl_O.Pt, 396., .005)
        assert_rel_error(self,comp.Fl_O.Tt, 2669.69, .005)
 
     
if __name__ == "__main__":
    unittest.main()
    