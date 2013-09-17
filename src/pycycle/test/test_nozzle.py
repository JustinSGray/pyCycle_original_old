
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle import nozzle, flowstation

TOL = 0.001

class NozzleTestCaseResonable(unittest.TestCase):

    def setUp(self): 

        self.comp = set_as_top(nozzle.Nozzle())

        fs = flowstation.CanteraFlowStation()
        fs.W = 100.
        fs.setTotalTP( 700., 50.0 )
        fs.Mach = 0.40

        self.comp.Fl_I = fs

        fs_ref = flowstation.CanteraFlowStation()
        fs_ref.W = 1.0
        fs_ref.setTotalTP( 518.67, 15.0 )
        fs_ref.Mach = 0.0

        self.comp.Fl_ref = fs_ref

        self.comp.design = True
        self.comp.run()

    def test_nozzle_off_design(self): 
        

        assert_rel_error(self, self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self, self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self, self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self, self.comp.Fl_O.Mach, 1.432, TOL)
        assert_rel_error(self, self.comp.Fl_O.area, 112.88, TOL)
        assert_rel_error(self, self.comp.Athroat_des, 99.59, TOL)
        assert_rel_error(self, self.comp.Aexit_des, 112.88, TOL)

        #off design calcs
        self.comp.run()
        assert_rel_error(self,self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self,self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self,self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self,self.comp.Fl_O.Mach, 1.432, TOL)
        assert_rel_error(self,self.comp.Fl_O.area, 112.88, TOL)
        assert_rel_error(self, self.comp.Athroat_des, 99.59, TOL)
        assert_rel_error(self, self.comp.Aexit_des, 112.88, TOL)


    def test_nozzle_under(self): 

        self.comp.Fl_ref.setTotalTP( 518.67, 14.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'UNDEREXPANDED')
        assert_rel_error(self,self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self,self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self,self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self, self.comp.Athroat_dmd, 99.59, TOL)
        assert_rel_error(self, self.comp.Fl_O.area, 112.88, TOL)

    def test_nozzle_over(self): 

        self.comp.Fl_ref.setTotalTP( 518.67, 16.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'OVEREXPANDED')
        assert_rel_error(self,self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self,self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self,self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self, self.comp.Fl_O.Ps, 15.0, TOL)

        
        self.comp.Fl_ref.setTotalTP( 518.67, 19.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'OVEREXPANDED')
        assert_rel_error(self, self.comp.Fl_O.Ps, 15.0, TOL)
        assert_rel_error(self, self.comp.Fl_O.Mach, 1.432, TOL)

        
        self.comp.Fl_ref.setTotalTP( 518.67, 24.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'OVEREXPANDED')

        
        self.comp.Fl_ref.setTotalTP( 518.67, 28.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'OVEREXPANDED')

        
        self.comp.Fl_ref.setTotalTP( 518.67, 32.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'OVEREXPANDED')

    def _test_nozzle_normal_shock(self): 
        self.comp.Fl_ref.setTotalTP( 518.67, 35.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'NORMAL_SHOCK')
        assert_rel_error(self,self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self,self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self,self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self, self.comp.Fl_O.Ps, 35.0, TOL)
        assert_rel_error(self, self.comp.Fl_O.Mach, 0.697, TOL)

        
        self.comp.Fl_ref.setTotalTP( 518.67, 37.0 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'NORMAL_SHOCK')
        assert_rel_error(self,self.comp.Fl_O.W, 100., TOL)
        assert_rel_error(self,self.comp.Fl_O.Pt, 50., TOL)
        assert_rel_error(self,self.comp.Fl_O.Tt, 700., TOL)
        assert_rel_error(self, self.comp.Fl_O.Ps, 37.0, TOL)
        assert_rel_error(self, self.comp.Fl_O.Mach, 0.662, TOL)

        # TODO: set W = 96.03, MN throat = 0.793, MN exit = 0.607
        '''
        comp.Fl_ref.setTotalTP( 518.67, 39.0 )
        comp.run()
        self.assertEqual(comp.switchRegime,'UNCHOKED')
        
        # set W = 80.80, MN throat = 0.562, MN exit = 0.470
        comp.Fl_ref.setTotalTP( 518.67, 43.0 )
        comp.run()
        self.assertEqual(comp.switchRegime,'UNCHOKED')
        '''

    def test_nozzle_perfect_expand(self): 
        self.comp.Fl_ref.setTotalTP( 518.67, 14.99 )
        self.comp.run()
        self.assertEqual(self.comp.switchRegime,'PERFECTLY_EXPANDED')


class NozzleTestCaseVeryLowPressure(unittest.TestCase):

    def test_nozzle_very_low_temperatures(self): 
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
    