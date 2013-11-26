from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent


class Inlet(CycleComponent): 
    """The inlet takes in air at a given flow rate and mach number, and diffuses it down 
    to a slower mach number and larger area"""

    ram_recovery = Float(1.000, iotype="in", desc="fraction of the total pressure retained")
    
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to compressor", copy=None)
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)
 


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O 

        Fl_O.copy_from( Fl_I )
        Pt_out = Fl_I.Pt*self.ram_recovery
        Fl_O.setTotal_hP(Fl_I.ht, Pt_out)
        Fl_O.W = Fl_I.W

   

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Inlet())
    c.run()

