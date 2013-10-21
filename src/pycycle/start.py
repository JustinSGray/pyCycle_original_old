from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, secant
from pycycle.cycle_component import CycleComponent


class FlowStart(CycleComponent): 
    """Flow initialization""" 

    W = Float(1, iotype="in", desc="mass flow rate", units="lbm/s")
    Pt = Float(14.7, iotype="in", desc="total pressure", units="psi")
    Tt = Float(518, iotype="in", desc="total temperature", units="degR")
    Mach = Float(.1, iotype="in", desc="Mach Number")

    Fl_O = FlowStation(iotype="out", desc="outgoing flow at the specified conditions", copy=None)


    def execute(self): 
        self.Fl_O.setTotalTP(self.Tt, self.Pt)
        self.Fl_O.W = self.W
        self.Fl_O.Mach = self.Mach

class FlowStartStatic(CycleComponent): 

    W = Float(1, iotype="in", desc="mass flow rate", units="lbm/s")
    Ps = Float(14.7, iotype="in", desc="total pressure", units="psi")
    Ts = Float(518, iotype="in", desc="total temperature", units="degR")
    Mach = Float(.1, iotype="in", desc="Mach Number")

    Fl_O = FlowStation(iotype="out", desc="outgoing flow at the specified conditions", copy=None)


    def execute(self): 
        self.Fl_O.setStaticTsPsMN(self.Ts, self.Ps, self.Mach)
        self.Fl_O.W = self.W
        self.Fl_O.Mach = self.Mach


class FlowStartStaticV(CycleComponent): 

    W = Float(1, iotype="in", desc="mass flow rate", units="lbm/s")
    Ps = Float(14.7, iotype="in", desc="total pressure", units="psi")
    Ts = Float(518, iotype="in", desc="total temperature", units="degR")
    velocity = Float(0, iotype="in", desc="Speed", units="ft/s")

    Fl_O = FlowStation(iotype="out", desc="outgoing flow at the specified conditions", copy=None)

    def _f(self, Mach):
        self.Fl_O.setStaticTsPsMN(self.Ts, self.Ps, Mach)
        return self.Fl_O.Vflow - self.velocity


    def execute(self): 
        
        if self.velocity == 0: 
            self.Fl_O.setStaticTsPsMN(self.Ts, self.Ps, 0)
        else: 
            M_guess = .9
            Mach = secant(self._f, M_guess, x_min=0)

        self.Fl_O.W = self.W
        self.Fl_O.Mach = Mach





