
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import nozzle, flowstation

class StartTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(nozzle.Nozzle())

        fs = flowstation.CanteraFlowStation()
        fs.W = .639
        fs.setTotalTP(540. , 0.34)
        fs.Mach = 0.4

        comp.Fl_I = fs

        fs_ref = flowstation.CanteraFlowStation()
        fs_ref.W = 3.488
        fs_ref.setTotalTP(630.75 , 0.0272)
        fs_ref.Mach = 1.0

        comp.Fl_ref = fs_ref
        comp.design = True
        comp.run()

        TOL = .01 #this test needs larger tollerance due to exteremely low temperatures
        assert_rel_error(self,comp.Fl_O.W, .639, TOL)
        assert_rel_error(self,comp.Fl_O.Pt, .34, TOL)
        assert_rel_error(self,comp.Fl_O.Tt, 540.0, TOL)
        assert_rel_error(self,comp.Fl_O.Mach, 2.7092, TOL)
        assert_rel_error(self,comp.Fl_O.area, 264.204, TOL)
        assert_rel_error(self,comp.Fl_O.rhos, .000177443, TOL)

        #off design calcs
        comp.run()
        assert_rel_error(self,comp.Fl_O.W, .639, TOL)
        assert_rel_error(self,comp.Fl_O.Pt, .34, TOL)
        assert_rel_error(self,comp.Fl_O.Tt, 540.0, TOL)
        assert_rel_error(self,comp.Fl_O.Mach, 2.7092, TOL)
        assert_rel_error(self,comp.Fl_O.area, 264.204, TOL)
        assert_rel_error(self,comp.Fl_O.rhos, .000177443, TOL)


        comp.Fl_ref.setTotalTP(630.75 , 0.03)
        comp.run()
        self.assertEqual(comp.switchRegime,'OVEREXPANDED')

        comp.Fl_ref.setTotalTP(630.75 , 0.026)
        comp.run()
        self.assertEqual(comp.switchRegime,'UNDEREXPANDED')

        comp.Fl_ref.setTotalTP(630.75 , 0.0272)
        comp.run()
        self.assertEqual(comp.switchRegime,'PERFECTLY_EXPANDED')

        
if __name__ == "__main__":
    unittest.main()
    