from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class Shaft(CycleComponent): 
    """The inlet takes in air at a given flow rate and mach number, and diffuses it down 
    to a slower mach number and larger area"""

    Nmech = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")
 
    trq1 = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")
    trq2 = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")  
    trq3 = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")
    trqNet = Float(0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure")

    
    def execute(self): 
        self.trqNet = self.trq1+self.trq2+self.trq3
  


class Nmech(CycleComponent): 
    """The inlet takes in air at a given flow rate and mach number, and diffuses it down 
    to a slower mach number and larger area"""

    Nmech = Float(0.0, iotype="out", desc="pressure differential as a fraction of incomming pressure")

    def execute(self): 
        self.Nmech = self.Nmech
  

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Inlet())
    c.run()

