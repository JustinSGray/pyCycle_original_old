
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import splitter, flowstation

class SplitterTestCase(unittest.TestCase):

    def setUp(self): 
        self.comp = set_as_top(splitter.SplitterBPR())

        self.fs = flowstation.FlowStation()
        self.fs.W = 3.48771299
        self.fs.setTotalTP(630.74523, 0.0271945)
        self.fs.Mach = 1

    def tearDown(self): 
        comp = None

    def test_splitter(self): 
        comp = self.comp

        comp.BPR = 2.2285
        comp.MNexit1_des = 1.00
        comp.MNexit2_des = 1.00
        comp.design = True

        comp.Fl_I = self.fs

        comp.run()

    def check(self, comp): 


        TOL = .001
        assert_rel_error(self,comp.Fl_O1.W, 1.08 ,TOL)
        assert_rel_error(self,comp.Fl_O1.Pt, 0.0271945 , TOL)
        assert_rel_error(self,comp.Fl_O1.Tt, 630.75, TOL)
        assert_rel_error(self,comp.Fl_O1.rhos, 0.0000737216 , TOL)
        assert_rel_error(self,comp.Fl_O1.Mach, 1.0 ,TOL)
        assert_rel_error(self,comp.Fl_O1.area, 1877.2, TOL)

        assert_rel_error(self,comp.Fl_O2.W, 2.407 ,TOL)
        assert_rel_error(self,comp.Fl_O2.Pt, 0.0271945 , TOL)
        assert_rel_error(self,comp.Fl_O2.Tt, 630.75, TOL)
        assert_rel_error(self,comp.Fl_O2.rhos, 0.0000737216 , TOL)
        assert_rel_error(self,comp.Fl_O2.Mach, 1.0 ,TOL)
        assert_rel_error(self,comp.Fl_O2.area, 4183.4, TOL)

    def test_splitterBPR(self): 
        comp = self.comp

        comp.BPR = 2.2285
        comp.MNexit1_des = 1.00
        comp.MNexit2_des = 1.00
        comp.design = True

        comp.Fl_I = self.fs

        comp.run()

        self.check(comp)

        #run off design
        comp.run()

        self.check(comp)

        #try changing something

        TOL = 0.001
        comp.Fl_I.W *= .95
        comp.run()
        assert_rel_error(self,comp.Fl_O1.Mach, .76922 ,TOL)
        assert_rel_error(self,comp.Fl_O2.Mach, .76922 ,TOL)

    def test_splitterW(self): 
        comp = self.comp = set_as_top(splitter.SplitterW())

        comp.W1_des = 1.08
        comp.MNexit1_des = 1.00
        comp.MNexit2_des = 1.00
        comp.design = True

        comp.Fl_I = self.fs

        comp.run()

        self.check(comp)

        #run off design
        comp.run()

        self.check(comp)

        #try changing something

        TOL = 0.001
        comp.Fl_I.W *= .95
        comp.run()
        assert_rel_error(self,comp.Fl_O1.Mach, .76922 ,TOL)
        assert_rel_error(self,comp.Fl_O2.Mach, .76922 ,TOL)


        
if __name__ == "__main__":
    unittest.main()
    