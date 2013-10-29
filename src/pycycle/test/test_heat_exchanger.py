
import unittest

from openmdao.main.api import set_as_top, Assembly
from openmdao.util.testutil import assert_rel_error
from openmdao.lib.drivers.api import BroydenSolver

from pycycle import heat_exchanger, flowstation


class HeatBalance(Assembly):

    def configure(self):

        hx = self.add('hx', heat_exchanger.HeatExchanger())
        driver = self.add('driver',BroydenSolver())
        driver.add_parameter('hx.T_hot_out',low=0.,high=1000.)
        driver.add_parameter('hx.T_cold_out',low=0.,high=1000.)
        driver.add_constraint('hx.residual_qmax=0')
        driver.add_constraint('hx.residual_e_balance=0')

        #hx.Wh = 0.49
        #hx.Cp_hot = 1.006
        #hx.T_hot_in = 791
        fs = flowstation.FlowStation()
        fs.setTotalTP(1423.8, 0.302712118187) #R, psi
        fs.W = 1.0
        hx.Fl_I = fs
        hx.dpQp = 0.0

        #initial guess
        avg = ( hx.Fl_I.Tt + hx.T_cold_in )/2.
        hx.T_cold_out = avg
        hx.T_hot_out = avg  

        driver.workflow.add(['hx'])


class HXTestCase(unittest.TestCase):

    def test_start(self): 
        hb = set_as_top(HeatBalance())

        hb.hx.design = True
        hb.run()
        
        assert_rel_error(self,hb.hx.Fl_O.Tt, 539.94, .005)
        assert_rel_error(self,hb.hx.Qreleased, 327.22, .005)
        assert_rel_error(self,hb.hx.Qabsorbed, 327.22, .005)
        assert_rel_error(self,hb.hx.Qmax, 335.1, .005)
        assert_rel_error(self,hb.hx.T_cold_in, 518.67, .005)
        assert_rel_error(self,hb.hx.T_cold_out, 749.96, .005)
        
        #check off design 
        #twiddle the values to make it run
        hb.hx.T_cold_out *= .9
        
        hb.run()
        
        assert_rel_error(self,hb.hx.Fl_O.Tt, 539.94, .005)
        assert_rel_error(self,hb.hx.Qreleased, 327.22, .005)
        assert_rel_error(self,hb.hx.Qabsorbed, 327.22, .005)
        assert_rel_error(self,hb.hx.Qmax, 335.1, .005)
        assert_rel_error(self,hb.hx.T_cold_in, 518.67, .005)
        assert_rel_error(self,hb.hx.T_cold_out, 749.96, .005)


        
        
if __name__ == "__main__":
    unittest.main()
    