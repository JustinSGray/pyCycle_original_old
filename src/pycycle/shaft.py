from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class Shaft(CycleComponent): 
    """This componet serves as the torque balancing part of the shaft element"""

    Nmech = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units='rpm' )
 
    trq1 = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units='ft*lbf' )
    trq2 = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units='ft*lbf' )  
    trq3 = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units='ft*lbf' )
    trqNet = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units='ft*lbf'  )

    
    def execute(self): 
        self.trqNet = self.trq1+self.trq2+self.trq3
  


class Nmech(CycleComponent): 
    """This component serves as the model hub for the speed (usually set from the sovler)"""

    Nmech = Float( 0.0, iotype="out", desc="pressure differential as a fraction of incomming pressure", units='rpm' )

    def execute(self): 
        self.Nmech = self.Nmech
  
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Shaft())
    c.run()
