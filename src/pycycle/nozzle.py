from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pyflowstation.pyflowstation import FlowStation



class Nozzle(Component): 
    """Calculates the gross thrust for a convergent-divergent nozzle, assuming an ideally expanded
    exit condition"""

    Fl_ref = FlowStation(iotype="in", desc="Flowstation with reference exit conditions")

    Fl_I = FlowStation(iotype="in", desc="incoming air stream to nozzle")
    Fl_O = FlowStation(iotype="out", desc="outgoing air stream from nozzle")

    design = Event(desc="flag to indicate that the calculations are design conditions")


    def shockPR(self, mach, gamma):
        """Calculates stagnation pressure ratio across a normal shock wave"""
        MN = mach
        g = gamma

        return (((g+1)/2*MN**2/(1+(g-1)/2*MN**2))**(g/(g-1)) * (1/ (2*g/(g+1)*MN**2 - (g-1)/(g+1)))**(1/(g-1)))

        
    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        fs_throat = CanteraFlowStation()
        fs_exitIdeal = CanteraFlowStation()

        fs_throat.W = Fl_I.W
        fs_throat.setTotalTP( Fl_I.Tt, Fl_I.Pt )
        fs_throat.Mach = 1.0
        Athroat_dmd = fs_throat.area

        fs_exitIdeal.W = Fl_I.W
        fs_exitIdeal.setTotalTP( Fl_I.Tt, Fl_I.Pt )
        fs_exitIdeal.Ps = Fl_ref.Ps

        Fl_O.W = Fl_I.W
        Fl_O.setTotalTP( Fl_I.Tt, Fl_I.Pt )
        Fl_O.Mach = fs_exitIdeal.Mach

        
        if self.run_design: 
            # Design Calculations at throat
            Athroat_des = fs_throat.area
            
            # Design calculations at exit
            Aexit_des = fs_exitIdeal.area

        else:
            # Find subsonic solution
            Fl_O.area = Aexit_des
            MachSubsonic = Fl_O.Mach
            if MachSubsonic > 1:
                print "invalid nozzle subsonic solution"
            PsSubsonic = Fl_O.Ps
            
            # Find supersonic solution
            
            
            # normal shock at nozzle exit
            


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Nozzle())
    c.run()
