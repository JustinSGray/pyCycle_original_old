import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event

from pycycle.flowstation import CanteraFlowStation, FlowStation, GAS_CONSTANT

class CycleComponent(Component): 

    design = Event(desc="flag to indicate that the calculations are design conditions")

    def __init__(self): 
        super(CycleComponent, self).__init__()

        self.run_design = False

    def _design_fired(self): 
        self.run_design = True


    def execute(self): 
        self.run_design = False