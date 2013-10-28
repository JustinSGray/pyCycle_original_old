
import unittest

from pycycle.flowstation import CanteraFlowStation
from openmdao.util.testutil import assert_rel_error

class FlowStationTestCase(unittest.TestCase):

    def setUp(self): 
        """Initialization function called before every test function""" 
        self.fs = CanteraFlowStation()
        self.fs.W = 100
        self.fs.setDryAir()
        self.fs.setTotalTP(518, 15)

    def tearDown(self): 
        """Clean up function called after every test function"""
        pass #nothing to do for this test

    def test_copyFS(self): 

        #print "TESTING"

        self.new_fs = CanteraFlowStation()

        self.new_fs.copy_from(self.fs)

        self.assertAlmostEqual(self.new_fs.Tt, 518)
        self.assertAlmostEqual(self.new_fs.Pt, 15)

     #all test function have to start with "test_" as the function name
    def test_setTotalTP(self):
        self.assertAlmostEqual(self.fs.Pt, 15.0, places=2)
        self.assertAlmostEqual(self.fs.Tt, 518, places=2)
        self.assertAlmostEqual(self.fs.ht, -6.32816, places=4) #Tom says the ht values will be different
        self.assertAlmostEqual(self.fs.W, 100, places=2)
        self.assertAlmostEqual(self.fs.rhot, .07812, places=4)

    def test_setTotalTP_low_pressure(self): 
        #self.fs.W = 0.745537973147
        #self.fs.area = 133.817708407
        #self.fs.Mach =  0.985900154274
        #self.fs.setTotalTP(1019.04099929, 0.332230438247)
        #print self.fs.Ps, self.fs.rhos, self.fs.area

        self.fs.W = 0.745740162779 
        self.fs.setTotalTP(1032.48576476, 0.33718196038)
        self.fs.Mach = 1
        #self.fs.area = 133.817708407

        print self.fs.area, self.fs.Ps

        self.fail()

 
    def test_setTotal_hP(self):
        ht = self.fs.ht
        self.fs.setTotalTP(1000, 40) #just to move things around a bit
        self.fs.setTotal_hP(ht, 15)
        self.test_setTotalTP() #just call this since it has all the checks we need  

    def test_setTotal_SP(self):
        s = self.fs.s
        self.fs.setTotalTP(1000, 40) #just to move things around a bit
        self.fs.setTotalSP(s, 15)      
        self.test_setTotalTP() #just call this since it has all the checks we need  
     
    def test_delh(self):
        ht = self.fs.ht
        self.fs.setTotalTP(1000, 40)
        diffh = self.fs.ht - ht
        self.assertAlmostEqual(diffh, 117.4544, places=2)        
        
    def test_dels(self):
        s = self.fs.s
        self.fs.setTotalTP(1000, 40)
        diffs = self.fs.s - s
        self.assertAlmostEqual(diffs, .092609, places=4)          
        
    def test_set_WAR(self):
        self.fs.setWAR( 0.02 );
        self.fs.setTotalTP(1000, 15); 
        self.assertAlmostEqual(self.fs.Pt, 15., places=2)
        self.assertAlmostEqual(self.fs.Tt, 1000, places=2)
        self.assertAlmostEqual(self.fs.WAR, 0.02, places=2)
        self.assertAlmostEqual(self.fs.FAR, 0, places=2)
        self.assertAlmostEqual(self.fs.ht, -2.34500, places=2)
        
    def test_setDryAir(self):
        self.fs.setDryAir()
        self.fs.setTotalTP(1000, 15); 
        self.assertAlmostEqual(self.fs.Pt, 15., places=2)
        self.assertAlmostEqual(self.fs.Tt, 1000, places=2)
        self.assertAlmostEqual(self.fs.WAR, 0.0, places=2)
        self.assertAlmostEqual(self.fs.FAR, 0, places=2)
        self.assertAlmostEqual(self.fs.ht, 111.124, places=2)
        self.assertAlmostEqual(self.fs.WAR, 0, places=2)
        self.assertAlmostEqual(self.fs.FAR, 0, places=2)

class TestBurn(unittest.TestCase): 
    def setUp(self):
        self.fs = CanteraFlowStation()
        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)
        self.fs.W = 100.
        self.fs.add_reactant("Jet-A(g)")
        self.fs.burn("Jet-A(g)", 2.5, -642)  

    #all test cases use the same checks here, so just re-use
    def _assert(self): 
        #print (self.fs._flow)  self.assertAlmostEqual(self.fs.W, 102.5, places=2)
        self.assertAlmostEqual(self.fs.FAR, .025, places=2)   
        self.assertAlmostEqual(self.fs.Pt, 400, places=2)
        self.assertAlmostEqual(self.fs.Tt, 2669.69, places=0)
        self.assertAlmostEqual(self.fs.ht, 117.16, places=1) 
        self.assertAlmostEqual(self.fs.rhot, .401845715, places=2)
        self.assertAlmostEqual(self.fs.W, 102.5, places=4)
        self.assertAlmostEqual(self.fs.gamt, 1.293, places=3)

    def test_burn(self):         
        self._assert()
        
    def test_add( self ):
        self.fs1 = CanteraFlowStation()
        self.fs1.setDryAir()
        self.fs1.setTotalTP(1100, 40)
        self.fs1.W = 10. 
        self.fs.add( self.fs1 );
        self.assertAlmostEqual(self.fs.W, 112.5, places=2)
        self.assertAlmostEqual(self.fs.FAR, .02272, places=4)   
        self.assertAlmostEqual(self.fs.Pt, 400, places=2)
        self.assertAlmostEqual(self.fs.Tt, 2507.74, places=0)
        self.assertAlmostEqual(self.fs.ht, 108.05, places=1) 
  
class TestStatics(unittest.TestCase): 
    def setUp(self):
        self.fs = CanteraFlowStation()
        self.fs.W = 100.
        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)      
        #print (self.fs._flow)  

    #all test cases use the same checks here, so just re-use
    def _assert(self): 
 
        TOL = .001
        assert_rel_error(self,self.fs.area, 32.0066, TOL)  
        assert_rel_error(self,self.fs.Mach, .3, TOL)   
        assert_rel_error(self,self.fs.Ps, 376.219, TOL)
        assert_rel_error(self,self.fs.Ts, 1081.732, TOL)   
        assert_rel_error(self,self.fs.Vflow, 479.298, TOL)
        assert_rel_error(self,self.fs.rhos, 0.93825, TOL)       
        assert_rel_error(self,self.fs.Mach, .3, TOL)   
        
    def test_set_Mach(self):
        self.fs.Mach = .3
        self._assert()

    def test_set_area(self):
        self.fs.area = 32.0066
        self.assertLess(self.fs.Mach, 1)
        self._assert()

    def test_set_Ps(self):
        self.fs.Ps = 376.219
        self._assert()
        
    def test_setStaticTsPsMN(self):
        self.fs.setStaticTsPsMN(1081.802, 376.219, .3)
        self._assert()
        
    def test_set_sub(self): 

        self.fs.sub_or_super = "sub"
        self.fs.area = 32
        self.assertLess(self.fs.Mach, 1)

    def test_set_super(self): 

        self.fs.sub_or_super = "super"
        self.fs.area = 32
        self.assertGreater(self.fs.Mach, 1)

        
if __name__ == "__main__":
    unittest.main()
    