from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, CanteraFlowStation
from pycycle.cycle_component import CycleComponent


class Duct(CycleComponent): 
    """The inlet takes in air at a given flow rate and mach number, and diffuses it down 
    to a slower mach number and larger area"""

    dPqP = Float(1.000, iotype="in", desc="pressure differential as a fraction of incomming pressure")
    Q_dot = Float(0.00, iotype="in", units="Btu/s", desc="heat flow rate into (positive) or out of (negative) the air")
    MNexit_des = Float(.6, iotype="in", desc="mach number at the exit of the inlet")

    Fl_I = FlowStation(iotype="in", desc="incoming air stream to compressor")
    Fl_O = FlowStation(iotype="out", desc="outgoing air stream from compressor")


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O 

        Pt_out = Fl_I.Pt*(1-self.dPqP)
        q = self.Q_dot/Fl_I.W
        Fl_O.setTotal_hP(Fl_I.ht+q, Pt_out)
        Fl_O.W = Fl_I.W

        if self.run_design: 
            Fl_O.Mach = self.MNexit_des
            self._exit_area_des = Fl_O.area
        else: 
            Fl_O.area = self._exit_area_des

        super(Duct, self).execute()




if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Inlet())
    c.run()

