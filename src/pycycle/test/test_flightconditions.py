
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import flightconditions, flowstation

class FlightConditionsTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(flightconditions.FlightConditions())

        comp.alt = 35000.
        comp.MN = .8
        comp.dTs = 2.
        comp.WAR = .0;
        comp.Wout = 100;

        comp.run()
        
        assert_rel_error(self,comp.Fl_O.W, 100., .005)
        assert_rel_error(self,comp.Fl_O.Mach, .8, .005)        
        assert_rel_error(self,comp.Fl_O.Ps, 3.471, .005)        
        assert_rel_error(self,comp.Fl_O.Pt, 5.2968, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 447.847, .005)
        
        comp.alt = 0.
        comp.MN = .0
        comp.dTs = 0.
        comp.WAR = .0;
        comp.Wout = 100;

        comp.run()
        
        assert_rel_error(self,comp.Fl_O.W, 100., .005)
        assert_rel_error(self,comp.Fl_O.Mach, .0, .005)        
        assert_rel_error(self,comp.Fl_O.Pt, 14.696, .005)        
        assert_rel_error(self,comp.Fl_O.Tt, 518.67, .005)
  
     
if __name__ == "__main__":
    unittest.main()
    