import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event

from pycycle.flowstation import CanteraFlowStation, FlowStation, GAS_CONSTANT



class Compressor(Component): 

    PR_des = Float(12.47, iotype="in", desc="Pressure ratio at design conditions")
    MNexit_des = Float(.4, iotype="in", desc="mach number at the compressor exit at design conditions")
    W_des = Float(1, iotype="in", units="lbm/s", desc="mass flow rate at design conditions")
    eff_des = Float(.95, iotype="in", desc="adiabatic efficiency at the design condition")
    hub_to_tip = Float(.4, iotype="in", desc="ratio of hub radius to tip radius")
    op_slope = Float(.85, iotype="in", desc="")


    W = Float(iotype="in", units="lbm/s",desc="mass flow rate at operating condition")
    Fl_I = FlowStation(iotype="in", desc="incoming air stream to compressor")

    PR = Float(iotype="out", desc="pressure ratio at operating conditions")
    eff = Float(iotype="out", desc="adiabatic efficiency at the operating condition")
    eff_poly = Float(iotype="out", desc="polytropic efficiency at the operating condition")
    pwr = Float(iotype="out", units="hp", desc="power required to run the compressor at the operating condition")
    Fl_O = FlowStation(iotype="out", desc="outgoing air stream from compressor")

    design = Event(desc="flag to indicate that the calculations are design conditions")

    def __init__(self): 
        super(Compressor, self).__init__()

        self.run_design = False


    def _op_line(self,Wc): 
        """relationship between compressor pressure ratio and mass flow""" 
        b = 1 - self.op_slope #scaled PR and Wc at design are both 1
        #assume a linear op line, with given slope

        norm_PR = self.op_slope*(Wc/self._sWc) + b 
        return norm_PR*self.PR_des

    def _design_fired(self): 
        self.run_design = True

    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        fs_ideal = CanteraFlowStation()
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
            self._sWc = 1./self._Wc_des
        else: 
            #Assumed Op Line Calculation
            self.PR = self._op_line(Fl_I.Wc)
            self.eff = self.eff_des #TODO: add in eff variation with W
            #Operational Conditions
            Pt_out = self.Fl_I.Pt*self.PR
            fs_ideal.setTotalSP(Fl_I.s, Pt_out)
            ht_out = (fs_ideal.ht-Fl_I.ht)/self.eff + Fl_I.ht
            Fl_O.setTotal_hP(ht_out, Pt_out)
            Fl_O.area = self._exit_area_des #causes Mach to be calculated based on fixed area

        C = GAS_CONSTANT*math.log(self.PR)
        delta_s = Fl_O.s - Fl_I.s
        self.eff_poly = C/(C+delta_s)
        self.pwr = Fl_I.W*(Fl_O.ht - Fl_I.ht) * 1.4148532 #btu/s to hp 


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Compressor())
    c.run()


