import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event

from pycycle.flowstation import FlowStation, FlowStationVar, GAS_CONSTANT
from pycycle.cycle_component import CycleComponent



class Compressor(CycleComponent): 
    """Axial Compressor performance calculations""" 

    
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to compressor", copy=None)

    PR = Float(iotype="out", desc="pressure ratio at operating conditions")
    eff = Float(iotype="out", desc="adiabatic efficiency at the operating condition")
    eff_poly = Float(iotype="out", desc="polytropic efficiency at the operating condition")
    pwr = Float(iotype="out", units="hp", desc="power required to run the compressor at the operating condition")
    tip_radius = Float(iotype="out", units="inch", desc="radius at the tip of the compressor")
    hub_radius = Float(iotype="out", units="inch", desc="radius at the tip of the compressor")
    Wfrac1 = Float(iotype="in", units="lbm/s", desc="Bleed 1 flow fraction")
    hfrac1 = Float(iotype="in", units="Btu/lbm", desc="Bleed 1 enthalpy fraction")
    Pfrac1 = Float(iotype="in", units="lbf/inch**2", desc="Bleed 1 pressure fraction")
    Wfrac2 = Float(iotype="in", units="lbm/s", desc="Bleed 2 flow fraction")
    hfrac2 = Float(iotype="in", units="Btu/lbm", desc="Bleed 2 enthalpy fraction")
    Pfrac2 = Float(iotype="in", units="lbf/inch**2", desc="Bleed 2 pressure fraction")


    Fl_O = FlowStationVar( iotype="out",desc="outgoing air stream from compressor", copy=None )
    Fl_bld1 = FlowStationVar(iotype="out", desc="first bleed port", copy=None )    
    Fl_bld2 = FlowStationVar(iotype="out", desc="second bleed port", copy=None )   
    
   
    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        Fl_O.copy_from( Fl_I )
        Fl_bld1 = self.Fl_bld1
        Fl_bld1.copy_from( Fl_I )
        Fl_bld2 = self.Fl_bld2
        Fl_bld2.copy_from( Fl_I )
        
        FO_ideal = FlowStation()
        FO_ideal.copy_from(  Fl_I )
 
        PtOut = Fl_I.Pt*self.PR
        FO_ideal.setTotalSP( Fl_I.s,PtOut )

        htOut = Fl_I.ht + ( FO_ideal.ht - Fl_I.ht )/self.eff
 
        # set the exit conditions to knowm enthalpy and pressure
        Fl_O.setTotalTP( 518, 15 )
        Fl_O.setTotal_hP( htOut, PtOut )

        # set the condtions for bleed 1  
        Wbleed1 = self.Wfrac1*Fl_I.W
        htBleed1 = Fl_I.ht+ self.hfrac1*( Fl_O.ht - Fl_I.ht )
        PtBleed1 = Fl_I.Pt + self.Pfrac1*( Fl_O.Pt - Fl_I.Pt )
        Fl_bld1.setTotal_hP( htBleed1,PtBleed1 )
        Fl_bld1.W  = Wbleed1
        print 'W in comp',Fl_bld1.W 

        # set the conditions for bleed 2
        Wbleed2 = self.Wfrac2*Fl_I.W;
        htBleed2 = Fl_I.ht+ self.hfrac2*( Fl_O.ht - Fl_I.ht) 
        PtBleed2 = Fl_I.Pt + self.Pfrac2*( Fl_O.Pt - Fl_I.Pt )
        Fl_bld2.setTotal_hP( htBleed2,PtBleed2 )
        Fl_bld2.W  = Wbleed2

        # subtract the bleed flow from the exit flow
        Wout = Fl_I.W - Fl_bld1.W - Fl_bld2.W
        Fl_O.W = Wout

        # determine the power
        pwr = Fl_I.W * (  Fl_I.ht - Fl_O.ht ) * 1.4148;
        pwr = pwr + Fl_bld1.W*(Fl_bld1.ht-Fl_O.ht)*1.4148 + Fl_bld2.W*(Fl_bld2.ht-Fl_O.ht)*1.4148
        
  
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Compressor())
    c.run()


