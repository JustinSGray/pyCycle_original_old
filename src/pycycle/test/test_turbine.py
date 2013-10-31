
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import turbine, flowstation

class TurbineTestCase(unittest.TestCase):

    def setUp(self): 
        self.comp = set_as_top(turbine.Turbine())

        self.fs = flowstation.FlowStation()
        self.fs.W = 16.85
        self.fs.setTotalTP( 1800., 30)

    def tearDown(self): 
        comp = None

    def test_turbine(self): 
        comp = self.comp

        comp.PR = 4.
        comp.eff_des = .85
        comp.Fl_I = self.fs
        comp.design = True

        comp.run()

        TOL = .001
 
        assert_rel_error(self,comp.Fl_O.W, 16.85,TOL)
        assert_rel_error(self,comp.Fl_O.Pt, 7.5, TOL)
        assert_rel_error(self,comp.Fl_O.Tt, 1340.46, TOL)
        assert_rel_error(self,comp.pwr, 2919.92, TOL)

if __name__ == "__main__":
    unittest.main()
    