
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import splitter_bpr, flowstation
                                             
class SplitterBPRTestCase(unittest.TestCase):

    def setUp(self): 
        self.comp = set_as_top(splitter_bpr.SplitterBPR())

        self.fs = flowstation.FlowStation()
        self.fs.W = 10
        self.fs.setTotalTP(630.74523, 10)

    def test_splitterBPR(self): 
        comp = self.comp

        comp.BPR = 9


        comp.Fl_I = self.fs

        comp.run()
        TOL = .001
        assert_rel_error(self,comp.Fl_O1.W, 1. ,TOL)
        assert_rel_error(self,comp.Fl_O1.Pt, 10. , TOL)
        assert_rel_error(self,comp.Fl_O1.Tt, 630.75, TOL)


        assert_rel_error(self,comp.Fl_O2.W, 9. ,TOL)
        assert_rel_error(self,comp.Fl_O2.Pt, 10., TOL)
        assert_rel_error(self,comp.Fl_O2.Tt, 630.75, TOL)


    
        
if __name__ == "__main__":
    unittest.main()
    