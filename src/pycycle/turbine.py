import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event

from pycycle.flowstation import FlowStation, FlowStationVar, GAS_CONSTANT
from pycycle.cycle_component import CycleComponent



class Turbine(CycleComponent): 
    """Axial Compressor performance calculations""" 

    PR = Float( 0., iotype="in", desc="Pressure ratio at design conditions")
    MNexit_des = Float( 0., iotype="in", desc="mach number at the compressor exit at design conditions")
    eff_des = Float( 0., iotype="in", desc="adiabatic efficiency at the design condition")
 
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to compressor", copy=None)

    PR = Float(iotype="out", desc="pressure ratio at operating conditions")
    eff = Float(iotype="out", desc="adiabatic efficiency at the operating condition")
    eff_poly = Float(iotype="out", desc="polytropic efficiency at the operating condition")
    pwr = Float(iotype="out", units="hp", desc="power required to run the compressor at the operating condition")
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)
 

    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        Fl_O.copy_from( Fl_I )
        fs_ideal = FlowStation()
        Fl_O.W = Fl_I.W
        
        
        if self.run_design: 
            #Design Calculations
            Fl_O.copy_from( Fl_I )
            fs_ideal.copy_from( Fl_I )
            Pt_out = self.Fl_I.Pt/self.PR
            fs_ideal.setTotalSP(Fl_I.s, Pt_out)
            ht_out =  Fl_I.ht - ( Fl_I.ht - fs_ideal.ht )*self.eff_des;
            Fl_O.setTotal_hP(ht_out, Pt_out)
            Fl_O.Mach = self.MNexit_des
            self._exit_area_des = Fl_O.area
            self._Wc_des = Fl_I.Wc

   
        C = GAS_CONSTANT*math.log(self.PR)
        delta_s = Fl_O.s - Fl_I.s
        self.eff_poly = C/(C+delta_s)
        self.pwr = Fl_I.W*(Fl_I.ht - Fl_O.ht) * 1.4148532 #btu/s to hp 
 

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Turbine())
    c.run()


