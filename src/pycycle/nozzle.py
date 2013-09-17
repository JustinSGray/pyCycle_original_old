from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Enum

from pycycle.flowstation import FlowStation, CanteraFlowStation, secant
from pycycle.cycle_component import CycleComponent



class Nozzle(CycleComponent): 
    """Calculates the gross thrust for a convergent-divergent nozzle, assuming an ideally expanded
    exit condition"""

    Fl_ref = FlowStation(iotype="in", desc="Flowstation with reference exit conditions")

    Fl_I = FlowStation(iotype="in", desc="incoming air stream to nozzle")
    
    Fl_O = FlowStation(iotype="out", desc="outgoing air stream from nozzle")
    Athroat_dmd = Float(iotype="out", desc="demand throat area for the nozzle at the operating condition")
    Athroat_des = Float(iotype="out", desc="nozzle throat area at the design condition")
    Aexit_des = Float(iotype="out", desc="nozzle exit area at the design condition")
    PsSubsonic = Float(iotype="out", desc="back pressure corresponding to subsonic expansion")
    PsSupersonic = Float(iotype="out", desc="back pressure corresponding to supersonic expansion")
    PsShock = Float(iotype="out", desc="back pressure corresponding to a normal shock at the nozzle exit")

    switchRegime = Enum(('UNCHOKED', 'NORMAL_SHOCK', 'UNDEREXPANDED', 'PERFECTLY_EXPANDED' ,'OVEREXPANDED'), 
        iotype="out", desc="nozzle operating regime")



    def shockPR(self, mach, gamma):
        """Calculates stagnation pressure ratio across a normal shock wave"""
        MN = mach
        g = gamma

        return (((g+1)/2*MN**2/(1+(g-1)/2*MN**2))**(g/(g-1)) * (1/ (2*g/(g+1)*MN**2 - (g-1)/(g+1)))**(1/(g-1)))

        
    def execute(self): 

        Fl_I = self.Fl_I
        Fl_O = self.Fl_O
        Fl_ref = self.Fl_ref

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
            self.Athroat_des = fs_throat.area

            # Design calculations at exit
            self.Aexit_des = fs_exitIdeal.area
            self.switchRegime = "PERFECTLY_EXPANDED"
        else:
            # Find subsonic solution, curve 4
            Fl_O.sub_or_super = "sub"
            Fl_O.area = self.Aexit_des

            MachSubsonic = Fl_O.Mach

            if MachSubsonic > 1:
                print "invalid nozzle subsonic solution"
            PsSubsonic = Fl_O.Ps

            # Find supersonic solution, curve 5
            Fl_O.sub_or_super = "super"
            PsOut = Fl_ref.Ps
            def F( Ps ):
                Fl_O.Ps = Ps
                return Fl_O.area - self.Aexit_des
            Fl_O.Ps = secant( F, PsOut )
            MachSupersonic = Fl_O.Mach
            PsSupersonic = Fl_O.Ps

            # normal shock at nozzle exit, curve c
            Fl_O.sub_or_super = "sub"
            Msuper = MachSupersonic
            PtExit = self.shockPR( Msuper, fs_throat.gams ) * fs_throat.Pt
            Fl_O.setTotalTP( fs_throat.Tt, PtExit )
            Fl_O.area = self.Aexit_des      
            PsShock = Fl_O.Ps
            
            # find correct operating regime
            # curves 1 to 4
            if Fl_ref.Ps >= PsSubsonic:
                self.switchRegime = "UNCHOKED"
                
                fs_throat.sub_or_super = "sub"
                Fl_O.sub_or_super = "sub"
                fs_throat.area = self.Athroat_des
                Fl_O.setTotalTP( fs_throat.Tt, fs_throat.Pt )
                Fl_O.area = self.Aexit_des

            # between curves 4 and c
            elif Fl_ref.Ps < PsSubsonic and Fl_ref.Ps >= PsShock:
                self.switchRegime = "NORMAL_SHOCK"

                Msuper = 1.5
                def F( MN ):
                    PtExit = self.shockPR( MN, fs_throat.gams) * fs_throat.Pt
                    Fl_O.setTotalTP( fs_throat.Tt, PtExit )
                    Fl_O.sub_or_super = "sub"
                    Fl_O.area = self.Aexit_des
                    return (Fl_O.Ps - Fl_ref.Ps)/Fl_ref.Ps
                Fl_O.Mach = secant( F, Msuper )

            # between curves c and 5
            elif Fl_ref.Ps < PsShock and Fl_ref.Ps > PsSupersonic:
                self.switchRegime = "OVEREXPANDED"
                Fl_O.sub_or_super = "super"
                Fl_O.setTotalTP( fs_throat.Tt, fs_throat.Pt )
                Fl_O.area = self.Aexit_des

            # between curves 5 and e
            elif Fl_ref.Ps <= PsSupersonic:
                self.switchRegime = "UNDEREXPANDED"
                Fl_O.sub_or_super = "super"
                Fl_O.setTotalTP( fs_throat.Tt, fs_throat.Pt )
                Fl_O.area = self.Aexit_des
            if abs(Fl_ref.Ps - PsSupersonic)/Fl_ref.Ps < .001: 
                self.switchRegime = "PERFECTLY_EXPANDED"

                
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Nozzle())
    c.run()
