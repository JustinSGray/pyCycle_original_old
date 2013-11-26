from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Int

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class Burner(CycleComponent): 
    """The inlet takes in air at a given flow rate and mach number, and diffuses it down 
    to a slower mach number and larger area"""

    ID_fuel = Int( 0, iotype="in", desc="reactant id number of the fuel being burned") 
    dPqP = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")
    hFuel = Float(0.0, iotype="in", desc="enthalpy of incoming fuel")
    Wfuel = Float(0.0, iotype="in", desc="fuel weight flow")


    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to compressor", copy=None)
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O 
        Fl_O.copy_from( Fl_I )
        
        Fl_O.burn( self.ID_fuel, self.Wfuel, self.hFuel ) 

        Fl_O.setTotal_hP( Fl_O.ht, Fl_O.Pt*(1-self.dPqP) )
  

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Burner())
    c.run()

