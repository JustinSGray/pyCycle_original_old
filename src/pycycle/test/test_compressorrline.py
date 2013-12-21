
import unittest

from openmdao.main.api import set_as_top
from openmdao.util.testutil import assert_rel_error

from pycycle.api import CompressorRline, FlowStation



class CompressorRlineTestCase(unittest.TestCase):

  

    def tearDown(self): 
        comp = None

    def test_compressor(self): 
    	   
    	# initial test case based on JT9D 34000 .8 operation    
    	self.comp = set_as_top(CompressorRline())
        self.fs = FlowStation()
        self.fs.W = 111.61
        self.fs.setDryAir()
        self.fs.setTotalTP( 707.81, 22.395 )
        comp = self.comp
        comp.PR = 5.609
        comp.eff = .8651
        comp.Wfrac1=.055
        comp.hfrac1=1
        comp.Pfrac1=1
        comp.Wfrac2=.035
        comp.hfrac2=1
        comp.Pfrac2=1
        comp.Nmech=8000

        comp.Fl_I = self.fs
        comp.run()

        TOL = .001
        
        # check the flow and mechanical values
        assert_rel_error( self,comp.Fl_O.W, 101.57, TOL )
        assert_rel_error( self,comp.Fl_O.Pt, 125.611, TOL )
        assert_rel_error( self,comp.Fl_O.Tt, 1209.83, TOL )
 
        assert_rel_error( self,comp.Fl_bld1.W, 6.1386, TOL )
        assert_rel_error( self,comp.Fl_bld1.Pt, 125.611, TOL )
        assert_rel_error( self,comp.Fl_bld1.Tt, 1209.83, TOL )
        
        assert_rel_error( self,comp.Fl_bld2.W, 3.9064, TOL )
        assert_rel_error( self,comp.Fl_bld2.Pt, 125.611, TOL )
        assert_rel_error( self,comp.Fl_bld2.Tt, 1209.83, TOL )
        
        
        assert_rel_error( self,comp.pwr, -19639.2, TOL )
        assert_rel_error( self,comp.trq, -1350.435, TOL )
        
        assert_rel_error( self,comp.eff, .8651, TOL )

        # adjust the bleed fraction to ensure the temperature is about half
        # way between input and output
        comp.hfrac1 = .5
        comp.run()
 
        assert_rel_error( self,comp.Fl_bld1.Tt, 961.654, TOL )
        
if __name__ == "__main__":
    unittest.main()
    