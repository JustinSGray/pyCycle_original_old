import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event

from pycycle.flowstation import FlowStation, FlowStationVar, GAS_CONSTANT
from pycycle.cycle_component import CycleComponent



class Compressor(CycleComponent): 
    """Axial Compressor performance calculations""" 

    PR_des = Float(12.47, iotype="in", desc="Pressure ratio at design conditions")
    MNexit_des = Float(.4, iotype="in", desc="mach number at the compressor exit at design conditions")
    eff_des = Float(.95, iotype="in", desc="adiabatic efficiency at the design condition")
    hub_to_tip = Float(.4, iotype="in", desc="ratio of hub radius to tip radius")
    op_slope = Float(.85, iotype="in", desc="")

    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to compressor", copy=None)

    PR = Float(iotype="out", desc="pressure ratio at operating conditions")
    eff = Float(iotype="out", desc="adiabatic efficiency at the operating condition")
    eff_poly = Float(iotype="out", desc="polytropic efficiency at the operating condition")
    pwr = Float(iotype="out", units="hp", desc="power required to run the compressor at the operating condition")
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)
    tip_radius = Float(iotype="out", units="inch", desc="radius at the tip of the compressor")
    hub_radius = Float(iotype="out", units="inch", desc="radius at the tip of the compressor")


    def _op_line(self,Wc): 
        """relationship between compressor pressure ratio and mass flow""" 
        b = 1 - self.op_slope #scaled PR and Wc at design are both 1
        #assume a linear op line, with given slope

        norm_PR = self.op_slope*(Wc/self._Wc_des) + b 

        return norm_PR*self.PR_des


    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        fs_ideal = FlowStation()
        Fl_O.W = Fl_I.W
        
        
        if self.run_design: 
            #Design Calculations
            Pt_out = self.Fl_I.Pt*self.PR_des
            self.PR = self.PR_des
            fs_ideal.setTotalSP(Fl_I.s, Pt_out)
            ht_out = (fs_ideal.ht-Fl_I.ht)/self.eff_des + Fl_I.ht
            Fl_O.setTotal_hP(ht_out, Pt_out)
            Fl_O.Mach = self.MNexit_des
            self._exit_area_des = Fl_O.area
            self._Wc_des = Fl_I.Wc

        else: 
            #Assumed Op Line Calculation
            self.PR = self._op_line(Fl_I.Wc)
            self.eff = self.eff_des #TODO: add in eff variation with W
            #Operational Conditions
            Pt_out = Fl_I.Pt*self.PR
            fs_ideal.setTotalSP(Fl_I.s, Pt_out)
            ht_out = (fs_ideal.ht-Fl_I.ht)/self.eff + Fl_I.ht
            Fl_O.setTotal_hP(ht_out, Pt_out)
            Fl_O.area = self._exit_area_des #causes Mach to be calculated based on fixed area

        C = GAS_CONSTANT*math.log(self.PR)
        delta_s = Fl_O.s - Fl_I.s
        self.eff_poly = C/(C+delta_s)
        self.pwr = Fl_I.W*(Fl_O.ht - Fl_I.ht) * 1.4148532 #btu/s to hp 
        self.tip_radius = (Fl_O.area/math.pi/(1-self.hub_to_tip**2))**.5
        self.hub_radius = self.hub_to_tip*self.tip_radius


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Compressor())
    c.run()


