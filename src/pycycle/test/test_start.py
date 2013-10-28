
import unittest

from openmdao.main.api import set_as_top, Assembly
from openmdao.util.testutil import assert_rel_error


from pycycle.api import FlowStart, FlowStation


class TestA(Assembly): 

    def configure(self):
        comp = self.add('comp', FlowStart())

        comp.W = 3.488
        comp.Pt = 0.0272
        comp.Tt = 630.75
        comp.Mach = 1.0

        self.driver.workflow.add('comp')



class StartTestCase(unittest.TestCase):
    def test_start_in_assembly(self): 

        a = set_as_top(TestA())
        a.run()

        assert_rel_error(self,a.comp.Fl_O.W, 3.488,.005)
        assert_rel_error(self,a.comp.Fl_O.Pt, .0272, .005)
        assert_rel_error(self,a.comp.Fl_O.Tt, 630.75, .005)
        assert_rel_error(self,a.comp.Fl_O.rhos, .000074, .005)
        assert_rel_error(self,a.comp.Fl_O.Mach, 1.00,.005)
        assert_rel_error(self,a.comp.Fl_O.area, 6060.6, .005)


    def test_start(self): 
        comp = set_as_top(FlowStart())

        comp.W = 3.488
        comp.Pt = 0.0272
        comp.Tt = 630.75
        comp.Mach = 1.0

        comp.run()

        assert_rel_error(self,comp.Fl_O.W, 3.488,.005)
        assert_rel_error(self,comp.Fl_O.Pt, .0272, .005)
        assert_rel_error(self,comp.Fl_O.Tt, 630.75, .005)
        assert_rel_error(self,comp.Fl_O.rhos, .000074, .005)
        assert_rel_error(self,comp.Fl_O.Mach, 1.00,.005)
        assert_rel_error(self,comp.Fl_O.area, 6060.6, .005)

        
if __name__ == "__main__":
    unittest.main()
    