__all__ = ['FlowStation']

from os.path import dirname, join

from openmdao.main.api import VariableTree
from openmdao.lib.datatypes.api import Float, VarTree, Enum

from Cantera import *

import pycycle #used to find file paths

GAS_CONSTANT = 0.0685592 #BTU/lbm-R

#secant solver with a limit on overall step size
def secant(func, x0, TOL=1e-7, x_min=1e15, x_max=1e15 ):
    if x0 >= 0:
        x1 = x0*(1 + 1e-4) + 1e-4
    else:
        x1 = x0*(1 + 1e-4) - 1e-4
    f1, f = func(x1), func(x0)
    if (abs(f) > abs(f1)):
        x1, x0 = x0, x1 
        f1, f = f, f1
    dx = f * (x0 - x1) / float(f - f1)  
    count = 0  
    while 1:
        if abs(dx) < TOL * (1 + abs(x0)): 
        #if abs((f1-f)/(f+1e-10)) < TOL: 
            return x0 -dx
        dx = f * (x0 - x1) / float(f - f1)  
        df = abs((f1-f)/(f+1e-10))      

        if x0-dx < x_min: 
            #x1, x0 = x0, x0*(1+.01*abs(dx)/dx)
            x1, x0 = x0, (x_min+x0)/2
        elif x0-dx > x_max: 
            x1, x0 = x0, (x_max+x0)/2
        else:    
            x1, x0 = x0, x0 - dx
        f1, f = f, func(x0) 
        count = count + 1


class FlowStation(VariableTree):

    reactants = []
    
    reactantNames = [[0 for x in xrange(6)] for x in xrange(6)]
    reactantSplits =[[0 for x in xrange(6)] for x in xrange(6)]
    numreacts = 0

    ht=Float(0.0, desc='total enthalpy', units='Btu/lbm')
    Tt=Float(0.0, desc='total temperature', units='degR')
    Pt=Float(0.0, desc='total pressure', units='lbf/inch**2')
    rhot=Float(0.0, desc='total density', units='lbm/ft**3') 
    gamt=Float(0.0, desc='total gamma') 
    Cp = Float(0.0, desc='Specific heat at constant pressure', units='Btu/(lbm*degR)')
    Cv = Float(0.0, desc='Specific heat at constant volume', units='Btu/(lbm*degR)')
    s =Float(0.0, desc='entropy', units='Btu/(lbm*R)')
    W =Float(0.0, desc='weight flow', units='lbm/s') 
    FAR =Float(0.0, desc='fuel to air ratio') 
    WAR =Float(0.0, desc='water to air ratio') 
    hs=Float(0.0, desc='static enthalpy', units='Btu/lbm')
    Ts=Float(0.0, desc='static temperature', units='degR')
    Ps=Float(0.0, desc='static pressure', units='lbf/inch**2')
    rhos=Float(0.0, desc='static density', units='lbm/ft**3')
    gams=Float(0.0, desc='static gamma')    
    Vflow =Float(0.0, desc='Velocity', units='ft/s')   
    Vsonic=Float(0.0, desc='Speed of sound', units='ft/s')
    Mach=Float(0.0, desc='Mach number')
    area =Float(0.0, desc='flow area', units='inch**2') 
    #mu = Float(0.0, desc='dynamic viscosity', units='lbm/(s*ft)')

    sub_or_super = Enum(('sub','super'), desc="selects preference for subsonic or supersonice solution when setting area")

    Wc = Float(0.0, desc='corrected weight flow', units='lbm/s') 


    #intialize station        
    def __init__(self,*args,**kwargs): 
        super(FlowStation, self).__init__(*args,**kwargs)

        #properties file path
        _dir = dirname(pycycle.__file__)
        _prop_file = join(_dir,'gri1000.cti')


        self.reactantNames=[[0 for x in xrange(6)] for x in xrange(6)]
        self.reactantSplits=[[0 for x in xrange(6)] for x in xrange(6)]
        self.numreacts = 0
        self._trigger = 0
        self._species=[1.0, 0, 0, 0, 0, 0, 0, 0]
        self._mach_or_area=0    
        self._flow=importPhase(_prop_file)
        self._flowS=importPhase(_prop_file)

    #add a reactant that can be mixed in
    @staticmethod
    def add_reactant(reactants, splits ):
    
            FlowStation.reactantNames[FlowStation.numreacts][0] = reactants[0]
            FlowStation.reactantNames[FlowStation.numreacts][1] = reactants[1]           
            FlowStation.reactantNames[FlowStation.numreacts][2] = reactants[2]
            FlowStation.reactantNames[FlowStation.numreacts][3] = reactants[3]
            FlowStation.reactantNames[FlowStation.numreacts][4] = reactants[4]
            FlowStation.reactantNames[FlowStation.numreacts][5] = reactants[5]
 
            FlowStation.reactantSplits[FlowStation.numreacts][0] = splits[0]
            FlowStation.reactantSplits[FlowStation.numreacts][1] = splits[1]    
            FlowStation.reactantSplits[FlowStation.numreacts][2] = splits[2]
            FlowStation.reactantSplits[FlowStation.numreacts][3] = splits[3]   
            FlowStation.reactantSplits[FlowStation.numreacts][4] = splits[4]
            FlowStation.reactantSplits[FlowStation.numreacts][5] = splits[5]   
            FlowStation.numreacts = FlowStation.numreacts + 1

    def _W_changed(self): 
        if self._trigger == 0:
            self._trigger=1
            self.setStatic()
            self._trigger=0

    #trigger action on Mach
    def _Mach_changed(self):
        if self._trigger == 0:
            self._trigger=1
            self._mach_or_area=1
            self.setStatic()
            self._trigger=0
                    
    #trigger action on area        
    def _area_changed(self):
        if self._trigger == 0:
            self._trigger=1
            self._mach_or_area=2
            self.setStatic()
            self._trigger=0
           
    #trigger action on static pressure       
    def _Ps_changed(self):
        if self._trigger == 0:
            self._trigger=1
            self._mach_or_area=3
            self.setStatic()
            self._trigger=0 

    def _setComp(self):
 
 
        global reactantNames 
        global reactantSplits 
        global numreacts
     
        tempcomp = ''
        compname    = ['', '', '', '', '', '', '', '', '', '', '', '']
        fract = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        numcurrent = 0;
        for cName in range ( 0, FlowStation.numreacts ):
            for cSpecies in range( 0, 6 ):
                if FlowStation.reactantSplits[cName][cSpecies]*self._species[cName] > 0.00001:
                   fract[numcurrent]=FlowStation.reactantSplits[cName][cSpecies]*self._species[cName];        
                   compname[numcurrent] = FlowStation.reactantNames[cName][cSpecies];
                   numcurrent = numcurrent+1;
    
  
        count1 = numcurrent-1
        while count1 > -1:
            count2 =  numcurrent-1
            while count2 > -1:
                if compname[count2] == compname[count1] and count1 != count2:
                   fract[count1]=fract[count1]+fract[count2]
                   fract[count2] = 0

                count2 = count2 - 1
            count1 = count1 - 1
  
        count1 = numcurrent-1
        while count1 > -1:      
             if fract[count1] > .000001:
                 tempcomp = tempcomp + str(compname[count1])+':' +str(fract[count1])+ ' '
             count1 = count1 - 1
            
        self._flow.setMassFractions( tempcomp )


    #set the composition to dry air
    def setDryAir(self):
        self._species[0]=1 
        self.WAR=0
        self.FAR=0
        self._setComp()
        self._trigger=0
        
    #set the composition to pure mixture of one of the reactants    
    def setReactant(self, i):
    	self._species= [0,0,0,0,0,0]
        self._species[i-1] = 1
        
    #set the compositon to air with water
    def setWAR(self, WAR):
        self._trigger=1
        self.WAR=WAR
        self.FAR=0
        self._species[0]=(1)/(1+WAR)
        self._species[1]=(WAR)/(1+WAR)
        self._setComp()
        self.setStatic()
        self._trigger=0
        
    def _total_calcs(self): 
        self.ht=self._flow.enthalpy_mass()*0.0004302099943161011
        self.s=self._flow.entropy_mass()*0.000238845896627
        self.rhot=self._flow.density()*.0624
        self.Tt=self._flow.temperature()*9./5.
        self.Cp = self._flow.cp_mass()*2.388459e-4
        self.Cv = self._flow.cv_mass()*2.388459e-4
        self.gamt=self.Cp/self.Cv
        self._flowS=self._flow 
        self.setStatic()
        self.Wc = self.W*(self.Tt/518.67)**.5/(self.Pt/14.696)    
        self.Vsonic=math.sqrt(self.gams*GasConstant*self._flowS.temperature()/self._flowS.meanMolecularWeight())*3.28084

        #self.mu = self._flow.viscosity()*0.671968975    
        self._trigger=0

    #set total conditions based on T an P
    def setTotalTP(self, Tin, Pin):
        self._setComp()    
        self._trigger=1
        self.Tt=Tin
        self.Pt=Pin                
        self._flow.set(T=Tin*5./9., P=Pin*6894.75729)
        self._flow.equilibrate('TP')
        self._total_calcs()

    #set total conditions based on h and P
    def setTotal_hP(self, hin, Pin):
        self._setComp()
        self._trigger=1 
        self.ht=hin
        self.Pt=Pin
        self._flow.set(H=hin/.0004302099943161011, P=Pin*6894.75729)
        self._flow.equilibrate('HP')
        self._total_calcs()


    #set total condition based on S and P
    def setTotalSP(self, sin, Pin):
        self._setComp()
        self._trigger=1
        self.s=sin
        self.Pt=Pin             
        self._flow.set(S=sin/0.000238845896627, P=Pin*6894.75729)
        self._flow.equilibrate('SP', loglevel=1)
        self._total_calcs()
        self._trigger=0

    #add another station to this one
    #mix enthalpies and keep pressure and this stations value
    def add(self, FS2):
        temp =""
        for i in range(0, len(self._species)):
                self._species[i]=(self.W*self._species[i]+FS2.W*FS2._species[i])/(self.W + FS2.W)
        self._setComp()
        air1 = self.W * ( 1. / ( 1. + self.FAR + self.WAR ))
        air2 = FS2.W *( 1. / ( 1 + FS2.WAR + FS2.FAR ))
        self.FAR = ( air1 * self.FAR + air2*FS2.FAR )/( air1 + air2 )
        self.WAR = ( air1 * self.WAR + air2*FS2.WAR )/( air1 + air2 )
        self.ht=(self.W*self.ht+FS2.W*FS2.ht)/(self.W+FS2.W)
        self.W=self.W +(FS2.W)
        self._flow.set(T=self.Tt*5./9., P=self.Pt*6894.75729) 
        self._flow.equilibrate('TP')
        self._flow.set(H=self.ht/0.0004302099943161011, P=self.Pt*6894.75729)
        self._flow.equilibrate('HP')
        self.Tt=self._flow.temperature()*9./5.
        self.s=self._flow.entropy_mass()* 0.000238845896627
        self.rhot=self._flow.density()*.0624
        self.gamt=self._flow.cp_mass()/self._flow.cv_mass()          
                    
    def copy_from(self, FS2):
        """duplicates total properties from another flow station""" 
        self.ht=FS2.ht
        self.Tt=FS2.Tt
        self.Pt=FS2.Pt
        self.rhot=FS2.rhot
        self.gamt=FS2.gamt
        self.s =FS2.s
        self.W =FS2.W
        self.FAR =FS2.FAR
        self.WAR =FS2.WAR
        temp =""
        for i in range(0, len(self.reactants)):
                self._species[i]=FS2._species[i]
                temp=temp+self.reactants[i]+":"+str(self._species[i])+" "
        self._flow.setMassFractions(temp)
        self._flow.set(T=self.Tt*5./9., P=self.Pt*6894.75729)
        self._flow.equilibrate('TP')
                    
    #burn a fuel with this station        
    def burn(self, fuel, Wfuel, hfuel):
        flow_1=self.W
        self.W=self.W + Wfuel 
        for i in range(0, len(self._species)):            
            if ( fuel - 1 ) == i:
                self._species[i]=(flow_1*self._species[i]+Wfuel)/ self.W
            else:
                self._species[i]=(flow_1*self._species[i])/ self.W
        self.ht= (flow_1 * self.ht + Wfuel * hfuel)/ self.W
        air1=flow_1 * (1. / (1. + self.FAR + self.WAR))
        self.FAR=(air1 * self.FAR + Wfuel)/(air1)
        self._setComp() 
        self._flow.set(T=2660*5/9, P=self.Pt*6894.75729)
        self._flow.equilibrate('TP')
        self._flow.set(H=self.ht/0.0004302099943161011, P=self.Pt*6894.75729)
        self._flow.equilibrate('HP')
        self.Tt=self._flow.temperature()*9./5.
        self.s=self._flow.entropy_mass()*0.000238845896627  
        self.rhot=self._flow.density()*.0624
        self.gamt=self._flow.cp_mass()/self._flow.cv_mass()

    #set the statics based on Mach
    def setStaticMach(self):
        mach_target = self.Mach
        def f(Ps):
            self.Ps=Ps
            self.setStaticPs()
            return self.Mach - mach_target

        Ps_guess = self.Pt*(1 + (self.gamt-1)/2*mach_target**2)**(self.gamt/(1-self.gamt))*.9
        secant(f, Ps_guess, x_min=0, x_max=self.Pt)


    #set the statics based on pressure
    def setStaticPs(self):
        self._flowS=self._flow 
        self._flowS.set(S=self.s/0.000238845896627, P=self.Ps*6894.75729) 
        self._flowS.equilibrate('SP')
        self.Ts=self._flowS.temperature()*9./5.
        self.rhos=self._flowS.density()*.0624
        self.gams=self._flowS.cp_mass()/self._flowS.cv_mass() 
        self.hs=self._flowS.enthalpy_mass()*0.0004302099943161011 
        self.Vflow=(778.169*32.1740*2*(self.ht-self.hs))**.5
        self.Vsonic=math.sqrt(self.gams*GasConstant*self._flowS.temperature()/self._flowS.meanMolecularWeight())*3.28084
        self.Mach=self.Vflow / self.Vsonic
        self.area= self.W / (self.rhos*self.Vflow)*144. 

    def setStaticArea(self): 
        target_area = self.area
        Ps_guess=self.Pt*(1 + (self.gamt-1)/2)**(self.gamt/(1-self.gamt)) #at mach 1
        def f(Ps):
            self.Ps = Ps
            self.setStaticPs()
            return 1-self.Mach
        
        Ps_M1 = secant(f,Ps_guess,x_min=0,x_max=self.Pt)

        #find the subsonic solution first
        guess = (self.Pt+Ps_M1)/2
        def f(Ps):
            self.Ps = Ps
            self.setStaticPs()
            return self.W/(self.rhos*self.Vflow)*144.-target_area
        secant(f,  guess, x_min=Ps_M1, x_max=self.Pt)

        #if you want the supersonic one, just keep going with a little lower initial guess    
        if self.sub_or_super == "super":
            #jsg: wild guess of 1/M_subsonic
            mach_guess = 1/self.Mach
            Ps_guess=self.Pt*(1 + (self.gamt-1)/2*mach_guess**2)**(self.gamt/(1-self.gamt))
            secant(f, Ps_guess, x_min=0, x_max=Ps_M1)

    #determine which static calc to use
    def setStatic(self):
        if (self.Tt and self.Pt): # if non zero
            self.Wc = self.W*(self.Tt/518.67)**.5/(self.Pt/14.696)

        if self._mach_or_area == 0:
            self.Ps = self.Pt 
            self.Ts = self.Tt
            self.rhos = self.rhot
            self.gams = self.gamt
            self.hs = self.ht 
            self.Vflow = 0
            self.Mach = 0

        elif self._mach_or_area == 1:
            self.setStaticMach()

        elif self._mach_or_area ==2:
            self.setStaticArea()
            
        elif self._mach_or_area == 3:
            self.setStaticPs()

    #set the statics based on Ts, Ps, and MN
    #UPDGRAEDE TO USE LOOPS
    def setStaticTsPsMN(self, Ts, Ps, MN): 
        self._trigger=1 

        self.Tt=Ts*(1+(self.gamt - 1) /2.* MN**2)
        self.Pt=Ps*(1+(self.gamt - 1) /2.* MN**2)**(self.gamt /(self.gamt -1))
        self.setTotalTP(self.Tt, self.Pt)

        #do this once more beacause gamt changed... very crude iteration
        self.Tt=Ts*(1+(self.gamt - 1) /2.* MN**2)
        self.Pt=Ps*(1+(self.gamt - 1) /2.* MN**2)**(self.gamt /(self.gamt -1))
        self.setTotalTP(self.Tt, self.Pt)

        self._trigger=1
        self.Mach=MN 
        self.setStaticMach()
        self.area= self.W / (self.rhos * self.Vflow)*144. 
        self._trigger=0


#For right now, all FlowStations are Air/Fuel FlowStations
FlowStation.add_reactant( ['N2', 'O2', 'AR', 'CO2', '', ''],[.755184, .231416, .012916, 0.000485, 0., 0. ] )
FlowStation.add_reactant( ['H2O', '', '', '', '', ''], [1., 0., 0., 0., 0., 0. ] )    
FlowStation.add_reactant( ['CH2', 'CH', '', '', '', ''], [.922189, 0.07781, 0., 0., 0., 0. ] )           
FlowStation.add_reactant( ['C', 'H', '', '', '', ''], [.86144,.13856, 0., 0., 0., 0. ] )   
FlowStation.add_reactant( ['Jet-A(g)', '', '', '', '', ''], [1., 0., 0., 0., 0., 0. ] )   
FlowStation.add_reactant( ['H2', '', '', '', '', ''], [1., 0., 0., 0., 0., 0. ] )  

#variable class used in components
class FlowStationVar(VarTree): 
   def __init__(self,*args,**metadata): 
        super(FlowStationVar,self).__init__(FlowStation(), *args, **metadata)
