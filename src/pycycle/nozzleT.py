from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Enum

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent



class Nozzle(CycleComponent): 
 
    PsExh = Float(0., iotype="in", units = "lbf/inch**2",desc="Exhaust static pressure")
    Ath = Float(0., iotype="in", units = "inch**2",desc="Nozzle throat area")
    Cfg = Float(1., iotype="in",desc="Coefficient gross thrust")
    Fg = Float(0., iotype="in", units = "lbf",desc="Gross Thrust")
     
    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to nozzle", copy=None)
    Fl_Th = FlowStationVar(iotype="in", desc="Nozzle throat conditions", copy=None) 
 
    def execute(self): 
  
         # set the throat conditions based on MN
         Fl_I= self.Fl_I
         Fl_Th = self.Fl_Th
         Fl_Th.copy_from( Fl_I )
         Fl_Th.Ps = self.PsExh;

         if Fl_Th.Mach > 1.0:
            # static pressur results in MN > 1  Nozzle is choked
            # set MN to 1
            Fl_Th.MN = 1 
            Ath = Fl_Th.W / ( Fl_Th.rhos * Fl_Th.Vflow)*144.;
         else:
            print self.PsExh
            Ath = Fl_Th.W / ( Fl_Th.rhos * Fl_Th.Vflow )*144.;
            # store area for use in off-design    
            
         self.Fg   = ( Fl_Th.W / 32.174 ) * Fl_Th.Vflow + ( Fl_Th.Ps - self.PsExh ) * Fl_Th.area*self.Cfg

     
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Nozzle())
    c.run()
