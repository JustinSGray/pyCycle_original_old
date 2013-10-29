
import unittest

from openmdao.util.testutil import assert_rel_error

from pycycle.flowstation import FlowStation


class FlowStationTestCase(unittest.TestCase):

    def setUp(self): 
        """Initialization function called before every test function""" 
        self.fs = FlowStation()

        self.fs.W = 100
        self.fs.setDryAir()
        self.fs.setTotalTP(518, 15)

    def tearDown(self): 
        """Clean up function called after every test function"""
        pass #nothing to do for this test

    def test_copyFS(self): 

        #print "TESTING"

        self.new_fs = FlowStation()

        self.new_fs.copy_from(self.fs)

        assert_rel_error(self,self.new_fs.Tt, 518, .0001)
        assert_rel_error(self,self.new_fs.Pt, 15, .0001)

     #all test function have to start with "test_" as the function name
    def test_setTotalTP(self):

        self.assertAlmostEqual(self.fs.Pt, 15.0, places=2)
        self.assertAlmostEqual(self.fs.Tt, 518, places=2)
        self.assertAlmostEqual(self.fs.ht, -6.32357, places=4) #Tom says the ht values will be different
        self.assertAlmostEqual(self.fs.W, 100, places=2)
        self.assertAlmostEqual(self.fs.rhot, .07812, places=4)



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
        assert_rel_error(self,diffh, 117.4544, .0001)        
        
    def test_dels(self):
        s = self.fs.s
        self.fs.setTotalTP(1000, 40)
        diffs = self.fs.s - s
        assert_rel_error(self,diffs, .092609, .0001)        
        
    def test_set_WAR(self):
        self.fs.setWAR( 0.02 )
        self.fs.setTotalTP(1000, 15); 
        assert_rel_error(self,self.fs.Pt, 15., .0001)
        assert_rel_error(self,self.fs.Tt, 1000, .0001)
        assert_rel_error(self,self.fs.WAR, 0.02, .0001)
        assert_rel_error(self,self.fs.FAR, 0, .0001)
        assert_rel_error(self,self.fs.ht, -.11513, .0001)

    def test_setDryAir(self):
        self.fs.setDryAir()
        self.fs.setTotalTP(1000, 15); 
        assert_rel_error(self,self.fs.Pt, 15.,.0001)
        assert_rel_error(self,self.fs.Tt, 1000, .0001)
        assert_rel_error(self,self.fs.WAR, 0.0, .0001)
        assert_rel_error(self,self.fs.FAR, 0, .0001)
        assert_rel_error(self,self.fs.ht, 111.129, .0001)
        assert_rel_error(self,self.fs.WAR, 0, .0001)
        assert_rel_error(self,self.fs.FAR, 0, .0001)



class TestBurn(unittest.TestCase): 
    def setUp(self):
        self.fs = FlowStation()
        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)
        self.fs.W = 100
        self.fs.burn(4,2.5, -642)  
        
    #all test cases use the same checks here, so just re-use
    def _assert(self): 
        #print (self.fs._flow)  assert_rel_error(self,self.fs.W, 102.5, places=2)
        assert_rel_error(self,self.fs.FAR, .025, .0001)   
        assert_rel_error(self,self.fs.Pt, 400, .0001)
        assert_rel_error(self,self.fs.Tt, 2669.69, .0001)
        assert_rel_error(self,self.fs.ht, 117.171, .0001) 
        assert_rel_error(self,self.fs.rhot, .404265, .0001)
        assert_rel_error(self,self.fs.W, 102.5, .0001)
        assert_rel_error(self,self.fs.gamt, 1.293336, .0001)

    def test_burn(self):         
        self._assert()
        
    def test_add( self ):
        self.fs1 = FlowStation()

        self.fs1.setDryAir()
        self.fs1.setTotalTP(1100, 15)
        self.fs1.W = 100.
        self.fs1.setWAR( .02 )
        self.fs1.setTotalTP(1100, 400)
        self.fs.add( self.fs1 )
        assert_rel_error(self,self.fs.Tt, 1932.471, .0001)
        assert_rel_error(self,self.fs.W, 202.5, .0001)
        assert_rel_error(self,self.fs.FAR, .012623, .001)   
        assert_rel_error(self,self.fs.Pt, 400, .001)
        assert_rel_error(self,self.fs.ht, 71.83056, .0001)
        assert_rel_error(self,self.fs.gamt, 1.3200, .0001)
        assert_rel_error(self,self.fs.WAR, .00990099, .0001)  
                
class TestStatics(unittest.TestCase): 
    def setUp(self):
        self.fs = FlowStation()
        self.fs.W = 100.
        self.fs.setDryAir()
        self.fs.setTotalTP(1100, 400)      
        #print (self.fs._flow)  

    #all test cases use the same checks here, so just re-use
    def _assert(self): 
 
        assert_rel_error(self,self.fs.area, 32.006, .0001)  
        assert_rel_error(self,self.fs.Mach, .3, .0001)   
        assert_rel_error(self,self.fs.Ps, 376.194, .0001)
        assert_rel_error(self,self.fs.Ts, 1081.781, .0001)   
        assert_rel_error(self,self.fs.Vflow, 479.519, .0001)
        assert_rel_error(self,self.fs.rhos, .93826, .0001)         
        assert_rel_error(self,self.fs.gams, 1.37596, .0001) 

    def test_set_Mach(self):
        self.fs.Mach = .3
        self._assert()

    def test_set_area(self):
        self.fs.area = 32.006
        self.assertLess(self.fs.Mach, 1)
        self._assert()

    def test_set_Ps(self):
        self.fs.Ps = 376.194
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
        
class HotH2(unittest.TestCase): 
    def testMN( self ):
        self.fs = FlowStation()
        self.fs.setReactant(6)
        self.fs.W = 100
        self.fs.setTotalTP( 5000, 540 );
        self.fs.Mach = 3.   
        assert_rel_error(self,self.fs.Mach, 3., .0001)   
        assert_rel_error(self,self.fs.Ts, 2052.78, .0001)   
        assert_rel_error(self,self.fs.Ps, 13.032, .0001)
        assert_rel_error(self,self.fs.Vflow, 24991.2, .0001)
        assert_rel_error(self,self.fs.rhos, .001192, .0001)        
        assert_rel_error(self,self.fs.gams, 1.370663, .0001)         

        
if __name__ == "__main__":
    unittest.main()
    