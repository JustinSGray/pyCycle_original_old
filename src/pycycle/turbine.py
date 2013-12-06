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
    Fl_bld1 = FlowStationVar(iotype="in", desc="bleed entering the front of the turbine", copy=None)
    Fl_bld2 = FlowStationVar(iotype="in", desc="bleed entering the exit of the turbine", copy=None)

    PR = Float(iotype="out", desc="pressure ratio at operating conditions")
    eff = Float(iotype="out", desc="adiabatic efficiency at the operating condition")
    eff_poly = Float(iotype="out", desc="polytropic efficiency at the operating condition")
    pwr = Float(iotype="out", units="hp", desc="power required to run the compressor at the operating condition")
   
    Nmech = Float( 10000., iotype="in", desc="Mechanical speed")
    trq = Float( 0., iotype="out", desc="trq") 
    
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)
 

    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        Fl_bld1 = self.Fl_bld1
        Fl_bld2 = self.Fl_bld2

        F41 = FlowStation()
        F48 = FlowStation()
        fs_ideal = FlowStation()

        
        F41.copy_from( Fl_I )
        F41.add( Fl_bld1 )
        fs_ideal.copy_from( F41 )
        F48.copy_from( F41 )

        #Design Calculations
        #fs_ideal.copy_from( Fl_O )
        Pt_out = self.Fl_I.Pt/self.PR
        fs_ideal.setTotalSP(F41.s, Pt_out)

        ht_out =  F41.ht - ( F41.ht - fs_ideal.ht )*self.eff;
        F48.setTotal_hP(ht_out, Pt_out)
        
        C = GAS_CONSTANT*math.log(self.PR)
        delta_s = Fl_O.s - Fl_I.s
        self.eff_poly = C/(C+delta_s)
        self.pwr = (F41.W)*(F41.ht - Fl_O.ht) * 1.4148532 #btu/s to hp 
        self.trq =  550. * self.pwr / self.Nmech;
 
        Fl_O.copy_from( F48 )
        Fl_O.add( Fl_bld2 )
        
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Turbine())
    c.run()

 
