"""
    preHeatEx.py -  (Run this before heatExchanger2.py)
        Performs inital energy balance for a basic heat exchanger design

     Originally built by Scott Jones in NPSS, ported and augmented by Jeff Chin   

NTU (effectiveness) Method
    Determine the heat transfer rate and outlet temperatures when the type and size of the heat exchanger is specified.

    NTU Limitations
    1) Effectiveness of the chosen heat exchanger must be known (empirical)

    Compatible with OpenMDAO v0.8.1
"""

from math import log, pi, sqrt, e

from openmdao.main.api import Assembly, Component
from openmdao.lib.datatypes.api import Float, Bool
from openmdao.lib.drivers.api import BroydenSolver 
from openmdao.main.api import convert_units as cu

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent



class HeatExchanger(CycleComponent): 
    """Calculates output temperatures for water and air, and heat transfer, for a given 
    water flow rate for a water-to-air heat exchanger"""

    #inputs
    W_cold = Float(.992, iotype="in", units = 'lbm/s', desc='Mass flow rate of cold fluid (water)') 
    Cp_cold = Float(0.9993, iotype="in", units = 'Btu/(lbm*R)', desc='Specific Heat of the cold fluid (water)') 
    T_cold_in = Float(518.58, iotype="in", units = 'R', desc='Temp of water into heat exchanger') 
    effectiveness = Float(.9765, iotype="in", desc='Heat Exchange Effectiveness') 
    MNexit_des = Float(.6, iotype="in", desc="mach number at the exit of heat exchanger")
    dPqP = Float(.1, iotype="in", desc="pressure differential as a fraction of incomming pressure")
    #State Vars
    T_hot_out = Float(1400, iotype="in", units = 'R', desc='Temp of air out of the heat exchanger')    
    T_cold_out = Float(518, iotype="in", units = 'R', desc='Temp of water out of the heat exchanger') 
    

    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to heat exchanger", copy=None)

    #outputs
    Qreleased = Float(iotype="out", units = 'hp', desc='Energy Released') 
    Qabsorbed= Float(iotype="out", units = 'hp', desc='Energy Absorbed') 
    LMTD = Float(iotype="out", desc='Logarathmic Mean Temperature Difference')
    Qmax= Float(iotype="out", units = 'hp', desc='Theoretical maximum possible heat transfer') 
 
    residual_qmax = Float(iotype="out", desc='Residual of max*effectiveness') 
    residual_e_balance = Float(iotype="out", desc='Residual of the energy balance')

    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from heat exchanger", copy=None)

    def execute(self):
        """Calculate Various Paramters"""
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O

        T_cold_in = self.T_cold_in
        T_cold_out = self.T_cold_out
        T_hot_in = self.Fl_I.Tt
        T_hot_out = self.T_hot_out
        W_cold = self.W_cold
        Wh = Fl_I.W
        Cp_hot = Fl_I.Cp
        Cp_cold = self.Cp_cold
        
        W_coldCpMin = W_cold*Cp_cold;
        if ( Wh*Cp_hot < W_cold*Cp_cold ):
            W_coldCpMin = Wh*Cp_hot
        self.Qmax = W_coldCpMin*(T_hot_in - T_cold_in)*1.4148532; #BTU/s to hp


        self.Qreleased = Wh*Cp_hot*(T_hot_in - T_hot_out)*1.4148532;
        self.Qabsorbed = W_cold*Cp_cold*(T_cold_out - T_cold_in)*1.4148532;


        try: 
            self.LMTD = ((T_hot_out-T_hot_in)+(T_cold_out-T_cold_in))/log((T_hot_out-T_cold_in)/(T_hot_in-T_cold_out))
        except ZeroDivisionError: 
            self.LMTD = 0

        self.residual_qmax = self.Qreleased-self.effectiveness*self.Qmax

        self.residual_e_balance = self.Qreleased-self.Qabsorbed

        Fl_O.setTotalTP(T_hot_out, Fl_I.Pt*(1-self.dPqP))
        Fl_O.W = Fl_I.W
        if self.run_design: 
            Fl_O.Mach = self.MNexit_des  
            self._exit_area_des = Fl_O.area
        else: 
            Fl_O.area = self._exit_area_des
 
if __name__ == "__main__":

    from openmdao.main.api import set_as_top
     

    class HeatBalance(Assembly):

        def configure(self):

            hx = self.add('hx', HeatExchanger())
            driver = self.add('driver',BroydenSolver())
            driver.add_parameter('hx.T_hot_out',low=0.,high=1000.)
            driver.add_parameter('hx.T_cold_out',low=0.,high=1000.)
            driver.add_constraint('hx.residual_qmax=0')
            driver.add_constraint('hx.residual_e_balance=0')

            #hx.Wh = 0.49
            #hx.Cp_hot = 1.006
            #hx.T_hot_in = 791
            fs = FlowStation()
            fs.setTotalTP(1423.8, 0.302712118187) #R, psi
            fs.W = 1.0
            hx.Fl_I = fs
            hx.W_cold = .45
            hx.T_hot_out = hx.Fl_I.Tt
            hx.T_cold_out = hx.T_cold_in

            driver.workflow.add(['hx'])

    test = HeatBalance()  
    set_as_top(test)
    test.hx.design = True

    test.run()

    print test.hx.W_cold, test.hx.T_hot_out, test.hx.Fl_I.Tt
    