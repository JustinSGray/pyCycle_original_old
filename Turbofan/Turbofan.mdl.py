from openmdao.main.api import Assembly, Component
from openmdao.lib.drivers.api import DOEdriver
from openmdao.lib.doegenerators.api import FullFactorial
from openmdao.lib.casehandlers.api import DumpCaseRecorder
from openmdao.lib.datatypes.api import Float
from openmdao.lib.drivers.api import BroydenSolver

from pycycle.api import (FlightConditions, Inlet, SplitterBPR, Compressor, Duct,
    Nozzle, Burner, Turbine, Nozzle, Shaft, Nmech, FlowStationVar)

class Turbofan(Assembly): 
	
   def configure(self):

        #component definition
        fc = self.add('fc', FlightConditions())
        fc.alt = 34000
        fc.MN = .8
        fc.Wout = 674.2
        
        inlet = self.add('inlet', Inlet() )
        inlet.ram_recovery = .995
        
        fan = self.add('fan', Compressor())
        fan.eff = .867
        fan.PR = 1.645
        
        split = self.add( 'split', SplitterBPR())
        split.BPR = 5.041
        
        bypduct = self.add( 'bypduct', Duct())
        bypduct.dPqP = .01
        
        bypnoz = self.add( 'bypnoz', Nozzle())
        bypnoz.cfg = .9962
        self.connect('fc.Fl_O.Ps', 'bypnoz.PsExh')       
   
        duct1 = self.add( 'duct1', Duct())
        duct1.dPqP = .0025
                    
        lpc = self.add( 'lpc', Compressor())
        lpc.eff = .868
        lpc.PR = 2.488       
        
        duct2 = self.add( 'duct2', Duct())
        duct2.dPqP = .0025
        
        hpc = self.add( 'hpc', Compressor())
        hpc.eff = .865
        hpc.PR = 5.609 
        hpc.Wfrac1=.055
        hpc.hfrac1=1
        hpc.Pfrac1=1
        hpc.Wfrac2=.035
        hpc.hfrac2=1
        hpc.Pfrac2=1
               
        
        burner = self.add( 'burner', Burner())
        burner.ID_fuel = 3
        burner.hFuel = -1200
        burner.Wfuel = 1.899
        burner.dPqP = .055
        
        
        hpt = self.add( 'hpt', Turbine())
        hpt.eff = .9133
        hpt.PR = 2.670
        
        duct3 = self.add( 'duct3', Duct())
        duct3.dPqP = .005
        
        lpt = self.add( 'lpt', Turbine())
        lpt.eff = .9323
        lpt.PR = 4.886
        
        duct4 = self.add( 'duct4', Duct())
        duct4.dPqP = .01
        
        prinoz = self.add( 'prinoz', Nozzle())
        prinoz.cfg = .9978
        self.connect('fc.Fl_O.Ps', 'prinoz.PsExh')    
        
        hpshaft = self.add( 'hpshaft', Shaft())
        hpspeed = self.add( 'hpspeed', Nmech())
        hpspeed.Nmech = 8000
        
        lpshaft = self.add( 'lpshaft', Shaft() )
        lpspeed = self.add( 'lpspeed', Nmech())
        hpspeed.Nmech = 2000

        #inter component connections
        self.connect( 'fc.Fl_O', 'inlet.Fl_I' )
        self.connect( 'inlet.Fl_O', 'fan.Fl_I' )
        self.connect( 'fan.Fl_O', 'split.Fl_I' )
        self.connect( 'split.Fl_O2', 'bypduct.Fl_I' )
        self.connect( 'bypduct.Fl_O', 'bypnoz.Fl_I' )
        self.connect( 'split.Fl_O1', 'duct1.Fl_I' )
        self.connect( 'duct1.Fl_O', 'lpc.Fl_I' )
        self.connect( 'lpc.Fl_O', 'duct2.Fl_I' )
        self.connect( 'duct2.Fl_O', 'hpc.Fl_I' )
        self.connect( 'hpc.Fl_O', 'burner.Fl_I' )
        self.connect( 'burner.Fl_O',  'hpt.Fl_I')
        self.connect( 'hpt.Fl_O', 'duct3.Fl_I' )
        self.connect( 'duct3.Fl_O', 'lpt.Fl_I' )
        self.connect( 'lpt.Fl_O', 'duct4.Fl_I' )
        self.connect( 'duct4.Fl_O', 'prinoz.Fl_I' )
        self.connect( 'hpc.Fl_bld1', 'hpt.Fl_bld1' )
        self.connect( 'hpc.Fl_bld2', 'hpt.Fl_bld2' )

        self.connect( 'hpspeed.Nmech', ['hpshaft.Nmech','hpc.Nmech', 'hpt.Nmech'] )
        self.connect( 'lpspeed.Nmech', ['lpshaft.Nmech','fan.Nmech','lpc.Nmech', 'lpt.Nmech'] )
        self.connect( 'hpc.pwr', 'hpshaft.trq1' )
        self.connect( 'hpt.pwr', 'hpshaft.trq2' )       
        self.connect( 'fan.pwr', 'lpshaft.trq1' )
        self.connect( 'lpc.pwr', 'lpshaft.trq2' )
        self.connect( 'lpt.pwr', 'lpshaft.trq3' )       
        
        hpspeed.Nmech = 8000
        lpspeed.Nmech = 2000
        
        driver = self.driver
        comp_list = [
        	'inlet',
                'fan',
                'split',
                'bypduct',
                'bypnoz',
                'lpc',
                'hpc', 
                'burner',
                'hpt', 
                'lpt', 
                'prinoz',
                'hpshaft',
                'lpshaft',
                'fc'
          ]

        solver = self.add('solver',BroydenSolver())

        solver.workflow.add( comp_list )
        driver.workflow.add('solver')

from collections import OrderedDict
TF1 = Turbofan()

TF1.run()

#TF1.run()

print 'torques'
print TF1.hpshaft.trqNet
print TF1.hpshaft.trq1
print TF1.hpshaft.trq2

print 'torques'
print TF1.lpshaft.trqNet
print TF1.lpshaft.trq1
print TF1.lpshaft.trq2
print TF1.lpshaft.trq3

print TF1.hpc.trq
print TF1.hpt.trq


print 'fc'
print TF1.fc.Fl_O.Pt
print TF1.fc.Fl_O.Ps
print TF1.fc.Fl_O.Tt
print TF1.fc.Fl_O.W

print 'inlet'
print TF1.inlet.Fl_O.Pt
print TF1.inlet.Fl_O.Tt
print TF1.inlet.Fl_O.W

print 'split'
print TF1.split.Fl_O1.Pt
print TF1.split.Fl_O1.Tt
print TF1.split.Fl_O1.W

print 'split'
print TF1.split.Fl_O2.Pt
print TF1.split.Fl_O2.Tt
print TF1.split.Fl_O2.W

print 'bypduct'
print TF1.bypduct.Fl_O.Pt
print TF1.bypduct.Fl_O.Tt
print TF1.bypduct.Fl_O.W

print 'lpc'
print TF1.lpc.Fl_O.Pt
print TF1.lpc.Fl_O.Tt
print TF1.lpc.Fl_O.W

print 'hpc'
print TF1.hpc.Fl_O.Pt
print TF1.hpc.Fl_O.Tt
print TF1.hpc.Fl_O.W

print 'burner'
print TF1.burner.Fl_O.Pt
print TF1.burner.Fl_O.Tt
print TF1.burner.Fl_O.W  

print 'hpt'
print TF1.hpt.Fl_O.Pt
print TF1.hpt.Fl_O.Tt
print TF1.hpt.Fl_O.W  

print 'lpt'
print TF1.lpt.Fl_O.Pt
print TF1.lpt.Fl_O.Tt
print TF1.lpt.Fl_O.W  

print TF1.hpshaft.trqNet
print TF1.burner.Wfuel/(TF1.prinoz.Fg+TF1.bypnoz.Fg-TF1.fc.Fram)*3600.


