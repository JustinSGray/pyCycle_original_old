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

    Fl_O = FlowStation(iotype="out", desc="outgoing flow at the specified conditions", copy=None)


    def execute(self): 
        self.Fl_O.setTotalTP(self.Tt, self.Pt)
        self.Fl_O.W = self.W
        self.Fl_O.Mach = self.Mach




