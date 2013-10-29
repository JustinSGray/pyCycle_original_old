from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class SplitterBPR(CycleComponent): 
    """Takes a single incoming air stream and splits it into two separate ones
    based on a given bypass ratio"""

    BPR = Float(2.0, iotype="in", desc="ratio of mass flow in Fl_O2 to Fl_O1")
    MNexit1_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O1")
    MNexit2_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O2")


    BPR_des = Float(iotype="out", desc="bypass ratio of the splitter at the design condition")
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to splitter", copy=None)
    Fl_O1 = FlowStationVar(iotype="out", desc="outgoing air stream 1", copy=None)
    Fl_O2 = FlowStationVar(iotype="out", desc="outgoing air stream 2", copy=None)


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O1 = self.Fl_O1
        Fl_O2 = self.Fl_O2

        Fl_O1.W = Fl_I.W/(self.BPR+1)
        Fl_O2.W = Fl_O1.W*self.BPR

        Fl_O1.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        Fl_O2.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        

        if self.run_design: 
            Fl_O1.Mach = self.MNexit1_des
            Fl_O2.Mach = self.MNexit2_des

            self._exit_area_1_des = Fl_O1.area
            self._exit_area_2_des = Fl_O2.area

            self.BPR_des = self.BPR
        else: 
            Fl_O1.area = self._exit_area_1_des
            Fl_O2.area = self._exit_area_2_des

class SplitterW(CycleComponent): 

    W1_des = Float(.44, iotype="in", desc="design mass flow in Fl_O1", units="lbm/s")
    MNexit1_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O1")
    MNexit2_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O2")

    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to splitter", copy=None)
    Fl_O1 = FlowStationVar(iotype="out", desc="outgoing air stream 1", copy=None)
    Fl_O2 = FlowStationVar(iotype="out", desc="outgoing air stream 2", copy=None)

    def execute(self): 
        """Takes a single incoming air stream and splits it into two separate ones
        based on a given mass flow for the Fl_O1"""

        Fl_I = self.Fl_I
        Fl_O1 = self.Fl_O1
        Fl_O2 = self.Fl_O2
        Fl_O1.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        Fl_O2.setTotalTP(Fl_I.Tt, Fl_I.Pt)

        if self.run_design: 
            Fl_O1.W = self.W1_des
            Fl_O2.W = Fl_I.W - self.W1_des

            self._BPR_des = Fl_O2.W/Fl_O1.W

            Fl_O1.Mach = self.MNexit1_des
            Fl_O2.Mach = self.MNexit2_des

            self._exit_area_1_des = Fl_O1.area
            self._exit_area_2_des = Fl_O2.area
        else: 
            Fl_O1.W = Fl_I.W/(self._BPR_des+1)
            Fl_O2.W = Fl_O1.W*self._BPR_des

            Fl_O1.area = self._exit_area_1_des
            Fl_O2.area = self._exit_area_2_des


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Splitter())
    c.run()

