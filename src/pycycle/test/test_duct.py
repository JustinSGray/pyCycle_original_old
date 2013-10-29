
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import duct, flowstation

class DuctTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(duct.Duct())

        comp.dPqP = 0
        comp.Q_dot = -237.8
        comp.MNexit_des = .4

        fs = flowstation.FlowStation()
        fs.W = 1.080
        fs.setTotalTP(1424.01, .34)
        fs.Mach = .4

        comp.Fl_I = fs

        comp.design = True
        comp.run()
        
        assert_rel_error(self,comp.Fl_O.W, 1.080, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .34, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 540.00, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .001566, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.4, .005)
        assert_rel_error(self,comp.Fl_O.area, 221.4, .005)

        #check off design 
        comp.run()
        
        assert_rel_error(self,comp.Fl_O.W, 1.080, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .34, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 540.00, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .001566, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.4, .005)
        assert_rel_error(self,comp.Fl_O.area, 221.4, .005)

        #vary something
        comp.dPqP = .1
        comp.run()

        assert_rel_error(self,comp.Fl_O.W, 1.080, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .306, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 540.00, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .0013783, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.4572, .005)
        assert_rel_error(self,comp.Fl_O.area, 221.4, .005)
        
if __name__ == "__main__":
    unittest.main()
    