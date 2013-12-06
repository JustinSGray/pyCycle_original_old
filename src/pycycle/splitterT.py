from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class SplitterBPR(CycleComponent): 
    """Takes a single incoming air stream and splits it into two separate ones
    based on a given bypass ratio"""

    BPR = Float(2.0, iotype="in", desc="ratio of mass flow in Fl_O2 to Fl_O1")


    BPR_des = Float(iotype="out", desc="bypass ratio of the splitter at the design condition")
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to splitter", copy=None)
    Fl_O1 = FlowStationVar(iotype="out", desc="outgoing air stream 1", copy=None)
    Fl_O2 = FlowStationVar(iotype="out", desc="outgoing air stream 2", copy=None)


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O1 = self.Fl_O1
        Fl_O2 = self.Fl_O2
        #Fl_O1.copy_from( Fl_I )
        #Fl_O2.copy_from( Fl_I )

        Fl_O1.W = Fl_I.W/(self.BPR+1)
        Fl_O2.W = Fl_O1.W*self.BPR

        Fl_O1.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        Fl_O2.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        
        
