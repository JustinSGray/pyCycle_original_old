from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Enum

from pycycle.flowstation import FlowStationVar, FlowStation
from pycycle.cycle_component import CycleComponent



class Nozzle(CycleComponent): 
    """Calculates the gross thrust for a convergent-divergent nozzle, assuming an ideally expanded
    exit condition"""

    Fl_ref = FlowStationVar(iotype="in", desc="Flowstation with reference exit conditions", copy=None)

    Fl_I = FlowStationVar(iotype="in", desc="incoming air stream to nozzle", copy=None)
    dPqP = Float(0, iotype="in", desc="ratio of change in total pressure to incomming total pressure")
    
    Fl_O = FlowStationVar(iotype="out", desc="outgoing air stream from nozzle", copy=None)
    Athroat_dmd = Float(iotype="out", desc="demand throat area for the nozzle at the operating condition.")
    Athroat_des = Float(iotype="out", desc="nozzle throat area at the design condition")
    Aexit_des = Float(iotype="out", desc="nozzle exit area at the design condition")
    PsSubsonic = Float(iotype="out", desc="back pressure corresponding to subsonic expansion")
    PsSupersonic = Float(iotype="out", desc="back pressure corresponding to supersonic expansion")
    PsShock = Float(iotype="out", desc="back pressure corresponding to a normal shock at the nozzle exit")
    Fg = Float(iotype="out", desc="gross thrust from nozzle", units="lbf")
    PR = Float(iotype="out", desc="ratio between total and static pressures at the nozzle exit")
    AR = Float(iotype="out", desc="ratio of exit area to throat area")

    #used for mass flow balance iterations
    WqAexit = Float(iotype="out", desc="mass flow per unit area at operating condition", units="lbm/(s*inch**2)")
    WqAexit_dmd = Float(iotype="out", desc="demand mass flow per unit area at operating condition", units="lbm/(s*inch**2)")

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

        fs_throat = FlowStation()
        fs_exitIdeal = FlowStation()

        fs_throat.W = Fl_I.W
        Pt_out = (1-self.dPqP)*Fl_I.Pt
        fs_throat.setTotalTP( Fl_I.Tt, Pt_out )
        fs_throat.Mach = 1.0
        self.Athroat_dmd = fs_throat.area

        fs_exitIdeal.W = Fl_I.W
        fs_exitIdeal.setTotalTP( Fl_I.Tt, Pt_out )
        fs_exitIdeal.Ps = Fl_ref.Ps

        Fl_O.W = Fl_I.W
        Fl_O.setTotalTP( Fl_I.Tt, Pt_out )
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
            Fl_O.area = self.Aexit_des
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
                Fl_O.sub_or_super = "sub"
                Fl_O.Ps = Fl_ref.Ps


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

        self.Fg = Fl_O.W*Fl_O.Vflow/32.174 + Fl_O.area*(Fl_O.Ps-Fl_ref.Ps)
        self.PR = fs_throat.Pt/Fl_O.Ps
        self.AR = Fl_O.area/fs_throat.area
        
        self.WqAexit = Fl_I.W/self.Athroat_des
        self.WqAexit_dmd = Fl_I.W/self.Athroat_dmd

        if self.switchRegime == "UNCHOKED": 
            self.WqAexit = Fl_I.W/Fl_ref.Ps
            self.WqAexit_dmd = Fl_I.W/Fl_O.Ps

                
if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Nozzle())
    c.run()
