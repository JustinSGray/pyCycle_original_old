
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import compressor, flowstation

class CompressorTestCase(unittest.TestCase):

    def test_compressor(self): 
        comp = set_as_top(compressor.Compressor())

        comp.PRdes = 3.488
        comp.MNexit_des = .4
        comp.eff_des = .80

        fs = flowstation.FlowStation()
        fs.W = 1.08
        fs.setTotalTP(630.75, 0.0272)
        fs.Mach = .6

        ccomp.Fl_I = fs

        comp.run()

        assert_rel_error(self,comp.Fl_O.W, 1.08,.005)
        assert_rel_error(self,comp.Fl_O.Pt, .34, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 1424.01, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .000594, .005)
        assert_rel_error(self,comp.Fl_O.Mach, .4 ,.005)
        assert_rel_error(self,comp.Fl_O.area, 364.7, .005)

        
if __name__ == "__main__":
    unittest.main()
    