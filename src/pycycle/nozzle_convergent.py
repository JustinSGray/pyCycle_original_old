from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Enum

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent



class NozzleConvergent(CycleComponent): 
 
    PsExh = Float( 0., iotype="in", desc="Exhaust static pressure", units="lbf/inch**2" )
    Ath = Float( 0., iotype="in", desc="Nozzle throat area", units="inch**2" )
    Cfg = Float( 1., iotype="in", desc="Coefficient on gross thrust" )
    Fg = Float( 0., iotype="in", desc="Gross Thrust", units="lbf" )
     
    Fl_I = FlowStationVar( iotype="in", desc="incoming air stream to nozzle", copy=None )
    Fl_Th = FlowStationVar( iotype="in", desc="Nozzle throat conditions", copy=None ) 
 
    def execute(self): 
  
         # set the throat conditions based on MN
         Fl_I= self.Fl_I
         Fl_Th = self.Fl_Th
         Fl_Th.copy_from( Fl_I )
         Fl_Th.Ps = self.PsExh;

         # determine is the exhaust pressure chokes the nozzle
         if Fl_Th.Mach > 1.0:
            # static pressur results in MN > 1  Nozzle is choked
            # set MN to 1
            Fl_Th.MN = 1 
            Ath = Fl_Th.W / ( Fl_Th.rhos * Fl_Th.Vflow)*144.;
         else:
            #nozzle not choked, run to static pressure 	 
            print self.PsExh
            Ath = Fl_Th.W / ( Fl_Th.rhos * Fl_Th.Vflow )*144.;
            
         #calculate gross thrust   
         self.Fg   = ( Fl_Th.W / 32.174 ) * Fl_Th.Vflow + ( Fl_Th.Ps - self.PsExh ) * Fl_Th.area*self.Cfg

     
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(NozzleConvergent())
    c.run()
