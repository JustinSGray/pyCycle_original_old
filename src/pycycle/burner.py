from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Int

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class Burner(CycleComponent): 
    """The burner takes mixes one cantera flow with another at cantera reactant
       and user supplied enthalpy.  If this cantera reactant is fuel, burning will
       occur"""

    #IO Variables
    ID_fuel = Int( 0, iotype="in", desc="reactant id number of the flow being mixed (fuel being burned)", units = "lbm/s" ) 
    dPqP = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure", units = "lbf/inch**2" )
    hFuel = Float( 0.0, iotype="in", desc="enthalpy of incoming fuel", units = "Btu/lbm" )
    Wfuel = Float( 0.0, iotype="in", desc="fuel weight flow", units = "lbm/s" )

    #flow connections
    Fl_I = FlowStationVar( iotype="in", desc="incoming flow stream to the burner", copy=None )
    Fl_O = FlowStationVar( iotype="out", desc="flow stream leaving the burner", copy=None )


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O 
        
        #set the exit station to the inlet as a starting point
        Fl_O.copy_from( Fl_I )
        
        #mix the new reactant with the flow
        Fl_O.burn( self.ID_fuel, self.Wfuel, self.hFuel ) 

        #apply the pressure drop
        Fl_O.setTotal_hP( Fl_O.ht, Fl_O.Pt*(1-self.dPqP) )
  

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Burner())
    c.run()

