
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import nozzle, flowstation

class StartTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(nozzle.Nozzle())

        fs = flowstation.CanteraFlowStation()
        fs.W = .639
        fs.setTotalTP(630.75 , 0.0272)
        fs.Mach = 1.0

        comp.Fl_I = fs

        fs_ref = flowstation.FlowStation()
        fs_ref.W = 3.488
        fs_ref.setTotalTP(630.75 , 0.0272)
        fs_ref.Mach = 1.0

        comp.Fl_ref = fs_ref
        comp.run()

        assert_rel_error(self,comp.Fl_O.W, .639, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .34, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 540.0, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .000177, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 2.7092, .005)
        assert_rel_error(self,comp.Fl_O.area, 264.43, .005)

        
if __name__ == "__main__":
    unittest.main()
    