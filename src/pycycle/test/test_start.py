
import unittest

from openmdao.main.api import set_as_top

from pycycle import start

class StartTestCase(unittest.TestCase):

    def test_start(self): 
        comp = set_as_top(start.FlowStart())

        comp.W = 3.488
        comp.Pt = .03
        comp.Tt = 630.75
        comp.Mach = 1.0

        comp.run()

        self.assertAlmostEqual(comp.Fl_O.W, 3.488)
        self.assertAlmostEqual(comp.Fl_O.Pt, .03)
        self.assertAlmostEqual(comp.Fl_O.Tt, 630.75)
        #self.assertAlmostEqual(comp.Fl_O.rhos, .000074)
        self.assertAlmostEqual(comp.Fl_O.Mach, 1.00)
        self.assertAlmostEqual(comp.Fl_O.area, 6060.6)

        
if __name__ == "__main__":
    unittest.main()
    