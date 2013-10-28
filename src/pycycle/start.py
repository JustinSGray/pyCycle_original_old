from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation
from pycycle.cycle_component import CycleComponent


class FlowStart(CycleComponent): 
    """Flow initialization""" 

    W = Float(1, iotype="in", desc="mass flow rate", units="lbm/s")
    Pt = Float(14.7, iotype="in", desc="total pressure", units="psi")
    Tt = Float(518, iotype="in", desc="total temperature", units="R")
    Mach = Float(.1, iotype="in", desc="Mach Number")

    area_des = Float(iotype="out", desc="flow area at the design condition")
    Fl_O = FlowStation(iotype="out", desc="outgoing flow at the specified conditions", copy=None)


    def execute(self): 
        Fl_O = self.Fl_O
        Fl_O.setTotalTP(self.Tt, self.Pt)
        Fl_O.W = self.W
        Fl_O.Mach = self.Mach

        if self.run_design: 
            self.area_des = Fl_O.area





