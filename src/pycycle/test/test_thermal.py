import unittest

from openmdao.main.api import set_as_top, Assembly
from openmdao.util.testutil import assert_rel_error

import numpy as np
from pycycle.api import CEA_tp

def rel_error(rhs, lhs, tol=0.01):
    return np.linalg.norm(rhs - lhs) / np.linalg.norm(rhs) < tol


class StartTestCase(unittest.TestCase):
    
    def test_n2ls_4000(self):
        comp = CEA_tp()

        this_nguess = np.array([ 0.02040748,  0.00231478,  0.01020431,  0.03292581])

        this_ch = np.array([[  2.27222641e-02,   2.50370446e-02,   2.27222641e-02],
         [  2.50370446e-02,   7.04838323e-02,   4.54456580e-02],
         [  2.27222641e-02,   4.54456580e-02,   7.59390390e-07]])

        this_rhs = np.array([-0.81078449, -1.59262881, -1.14346367])
        
        this_mu = np.array([-34.02175706, -50.32264785, -32.60178159])

        comp.nguess = this_nguess
        comp.T = 4000
        comp.P = 1.034210
        comp.run()

        rel_error(comp.rhs, this_rhs, 0.001)
        rel_error(comp.ch, this_ch, 0.001)
        rel_error(comp.mu, this_mu, 0.001)

    def test_n2ls_1500(self):
        comp = CEA_tp()

        this_nguess = np.array([6.58936767e-06,   2.27158983e-02,   6.24254002e-06,   2.27252139e-02])

        this_ch = np.array([[  2.27224876e-02,   4.54383859e-02,   2.27224876e-02],
                     [  4.54383859e-02,   9.08951525e-02,   4.54508710e-02],
                     [  2.27224876e-02,   4.54508710e-02,   3.51630007e-06]])

        this_rhs = np.array([-1.40217711, -2.80452075, -1.40240467])
        
        this_mu = np.array([-43.73879404, -61.71398144, -35.95037481])

        comp.nguess = this_nguess
        comp.T = 1500
        comp.P = 1.034210
        comp.run()

        rel_error(comp.rhs, this_rhs, 0.001)
        rel_error(comp.ch, this_ch, 0.001)
        rel_error(comp.mu, this_mu, 0.001)