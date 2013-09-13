
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import compressor, flowstation

class CompressorTestCase(unittest.TestCase):

    def test_compressor(self): 
        comp = set_as_top(compressor.Compressor())

        comp.PR_des = 12.47
        comp.MNexit_des = .4
        comp.eff_des = .80

        fs = flowstation.CanteraFlowStation()
        fs.W = 1.08
        fs.setTotalTP(630.74523, 0.0271945)
        fs.Mach = .6

        comp.Fl_I = fs
        comp.design = True

        comp.run()

        TOL = .001
        assert_rel_error(self,comp.Fl_O.W, 1.08,TOL)
        assert_rel_error(self,comp.Fl_O.Pt, .33899, TOL)
        assert_rel_error(self,comp.Fl_O.Tt, 1424.01, TOL)
        assert_rel_error(self,comp.Fl_O.rhos, .000594, TOL)
        assert_rel_error(self,comp.Fl_O.Mach, .4 ,TOL)
        assert_rel_error(self,comp.Fl_O.area, 364.7, TOL)
        assert_rel_error(self,comp.pwr, 303.2, TOL)
        assert_rel_error(self,comp.eff_poly, .8545, TOL)

        
if __name__ == "__main__":
    unittest.main()
    