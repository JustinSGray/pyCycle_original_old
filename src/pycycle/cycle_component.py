import math 

from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree, Event


class CycleComponent(Component): 

    design = Event(desc="flag to indicate that the calculations are design conditions")

    def __init__(self): 
        super(CycleComponent, self).__init__()

        self.run_design = False

    def _design_fired(self): 
        self.run_design = True


    def run(self,*args,**kwargs): 
        super(CycleComponent, self).run(*args,**kwargs)
        self.run_design = False