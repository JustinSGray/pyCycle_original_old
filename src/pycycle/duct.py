from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation, FlowStationVar
from pycycle.cycle_component import CycleComponent


class Duct(CycleComponent): 
    """The duct allows the user to apply a pressure drop to the stream"""

    dPqP = Float( 0.0, iotype="in", desc="pressure differential as a fraction of incomming pressure" )

    Fl_I = FlowStationVar( iotype="in", desc="incoming air stream to compressor", copy=None )
    Fl_O = FlowStationVar( iotype="out", desc="outgoing air stream from compressor", copy=None )


    def execute( self ): 
        Fl_I = self.Fl_I
        Fl_O = self.Fl_O 
 
        # pass the flow information along
        Fl_O.copy_from( Fl_I )
        
        #determine the exit pressure
        Pt_out = Fl_I.Pt*( 1 - self.dPqP )

        # set the exit conditions based on the new enthalpy and pressure
        Fl_O.setTotal_hP( Fl_I.ht, Pt_out )


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Duct())
    c.run()

