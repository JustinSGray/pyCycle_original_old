
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import inlet, flowstation

class StartTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(inlet.Inlet())

        comp.ram_recovery = 1.0
        comp.MNexit_des = .6

        fs = flowstation.FlowStation()
        fs.W = 1.080
        fs.setTotalTP(630.75, 0.0272)
        fs.Mach = 1.0

        comp.Fl_I = fs

        comp.design = True
        comp.run()

        assert_rel_error(self,comp.Fl_O.W, 1.080, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .0272, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 630.75, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .000098, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.6, .005)
        assert_rel_error(self,comp.Fl_O.area, 2230.8, .005)

        #check off design 
        comp.run()

        assert_rel_error(self,comp.Fl_O.W, 1.080, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .0272, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 630.75, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .000098, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.6, .005)
        assert_rel_error(self,comp.Fl_O.area, 2230.8, .005)

        #vary something
        comp.Fl_I.W = .9
        comp.run()

        assert_rel_error(self,comp.Fl_O.W, .9, .005)
        assert_rel_error(self,comp.Fl_O.Pt, .0272, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 630.75, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 0.45955, .005)
        assert_rel_error(self,comp.Fl_O.area, 2230.8, .005)
        
if __name__ == "__main__":
    unittest.main()
    