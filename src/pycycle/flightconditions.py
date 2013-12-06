import math
from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent


class FlightConditions(CycleComponent): 
    """This element determines the flow conditions based on input altitude, Mach number,
       and dTs"""

    alt = Float(0., iotype="in", desc="input altitude", units="ft")
    MN = Float(0., iotype="in", desc="input Mach number")
    dTs = Float(iotype="in", desc="input ambient altitude delta", units="R")
    WAR = Float(iotype="in", desc="Water to air ratio", units="R")
    Wout = Float(iotype="in", desc="Weight flow", units="lbm/s")    
    Fram = Float(iotype="in", desc="Ram drag", units="lbf")
  
 
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from compressor", copy=None)

    def execute(self): 
    	
    	Fl_O = self.Fl_O;
    	
        REARTH = 6369.0
        GMR = 34.163195
        htab = ( 0.0,  11.0, 20.0, 32.0, 47.0, 51.0, 71.0, 84.852 )
        ttab = [ 288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.946 ]
        ptab = [ 1.0, 2.2336110E-1, 5.4032950E-2, 8.5666784E-3, 1.0945601E-3, 6.6063531E-4, 3.9046834E-5, 3.68501E-6 ]
        gtab = [ -6.5, 0.0, 1.0, 2.8, 0, -2.8, -2.0, 0.0 ]

        Ts=0
        Ps=0

        h = self.alt/3280.84*REARTH/(self.alt/3280.84+REARTH)	

        i = 0
        while ( h > htab[i] ):
           i = i + 1
 
        i = i - 1
    
        tbase = ttab[i]*9/5
        tgrad = gtab[i]    
        deltah=h-htab[i]
        Ts=tbase+tgrad*deltah*9/5
        
        if (tgrad == 0. ):
           Ps = ptab[i]*math.exp(-GMR*deltah/tbase*9./5.)*14.696
        else:
           Ps =ptab[i]*((tbase/Ts)**(GMR/tgrad))*14.696

      
        Ts = self.dTs + Ts
        Fl_O.W = self.Wout
        Fl_O.setWAR( self.WAR )

        if ( self.MN > 0 ):
           Fl_O.setStaticTsPsMN( Ts, Ps, self.MN )
        else:
           Fl_O.setTotalTP( Ts, Ps )



        self.Fram = Fl_O.Vflow*Fl_O.W/32.174

if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(FlightConditions())
    c.run()

