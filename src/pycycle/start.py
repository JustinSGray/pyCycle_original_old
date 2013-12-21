from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class FlowStart(CycleComponent): 
    """Start a flow""" 

    W = Float( 0., iotype="in", desc="mass flow rate", units="lbm/s" )
    Pt = Float( 14.7, iotype="in", desc="total pressure", units="psi" )
    Tt = Float( 518, iotype="in", desc="total temperature", units="degR" )
    species1 = Float( 1., iotype="in", desc="relative amount of species 1 in the flow" )   
    species2 = Float( 0., iotype="in", desc="relative amount of species 2 in the flow" )   
    species3 = Float( 0., iotype="in", desc="relative amount of species 3 in the flow" )   
    species4 = Float( 0., iotype="in", desc="relative amount of species 4 in the flow" )   
    species5 = Float( 0., iotype="in", desc="relative amount of species 5 in the flow" )   
    species6 = Float( 0., iotype="in", desc="relative amount of species 6 in the flow" )   
                    
    Fl_O = FlowStationVar( iotype="out", desc="outgoing flow at the specified conditions", copy=None )


    def execute(self): 
        Fl_O = self.Fl_O
        Fl_O._species = [ self.species1, self.species2, self.species3, self.species4, self.species5, self.species6 ]
        Fl_O.setTotalTP( self.Tt, self.Pt )
        Fl_O.W = self.W

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(FlowStart())
    c.run()


