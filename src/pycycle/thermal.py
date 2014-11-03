import numpy as np 

from openmdao.main.api  import Assembly,Component
from openmdao.lib.datatypes.api import Float, Array


R =1.987 #universal gas constant

a=np.array([
[ #CO
4.619197250e+05,-1.944704863e+03,5.916714180e+00,-5.664282830e-04,
1.398814540e-07,-1.787680361e-11,9.620935570e-16,-2.466261084e+03,
-1.387413108e+01],
[#CO2
1.176962419e+05,-1.788791477e+03,8.291523190e+00,-9.223156780e-05,
4.863676880e-09,-1.891053312e-12,6.330036590e-16,-3.908350590e+04,
-2.652669281e+01],
[ #O2
-1.037939022e+06,2.344830282e+03,1.819732036e+00,1.267847582e-03,
-2.188067988e-07,2.053719572e-11,-8.193467050e-16,-1.689010929e+04,
1.738716506e+01
]])
wt_mole = np.array([ 28.01, 44.01, 32. ])    
element_wt = [ 12.01, 16.0 ]
aij = np.array([ [1,1,0], [1,2,2] ])


_num_element = 2
_num_react = 3

#pre-computed constants used in calculations
_aij_prod = np.empty((_num_element,_num_element, _num_react))
for i in range( 0, _num_element ):
    for j in range( 0, _num_element ):
        _aij_prod[i][j] = aij[i]*aij[j]

_aij_prod_deriv = np.zeros((_num_element**2,_num_react))
for k in xrange(_num_element**2):
    for l in xrange(_num_react):
        i = k/_num_element
        j = np.mod(k,_num_element)
        _aij_prod_deriv[k][l] = _aij_prod[i][j][l]


class CEA_tp(Component):

    nguess = Array(iotype="in", desc="molar concentration of the mixtures, \
                   last element is the total molar concentration")
    T = Float(iotype="in", desc="Temperature")
    P = Float(iotype="in", desc="Pressure")

    rhs = Array(np.zeros(_num_element + 1), iotype="out", desc="Right-hand side of resulting system")
    mu = Array(iotype="out", desc="A chemical thing")
    ch = Array(np.zeros((_num_element+1, _num_element+1)), iotype="out", 
               desc="Left-hand side of resulting system")
    
    def H0(self):
        ai = a.T
        T = self.T
        return (-ai[0]/T**2 + ai[1]/T*np.log(T) + ai[2] + ai[3]*T/2. + ai[4]*T**2/3. + ai[5]*T**3/4. + ai[6]*T**4/5.+ai[7]/T)
    
    def S0(self):
        ai = a.T
        T = self.T
        return (-ai[0]/(2*T**2) - ai[1]/T + ai[2]*np.log(T) + ai[3]*T + ai[4]*T**2/2. + ai[5]*T**3/3. + ai[6]*T**4/5.+ai[8] )
    
    def execute(self):
        """
        Maps molar concentrations to pi coefficients matrix 
        and a right-hand-side
        """ 

        nj = self.nguess[:-1]
        nmoles = self.nguess[-1]
        b = np.zeros(_num_element)
        b0 = np.zeros(_num_element)
    
        #calculate mu for each reactant
        self.mu = self.H0() - self.S0() + np.log(nj) + np.log(self.P/nmoles) #pressure in Bars

        #calculate b_i for each element
        for i in range( 0, _num_element ):
            b[ i ] =  np.sum(aij[i]*nj) 

        ##determine pi coef for 2.24, 2.56, and 2.64 for each element
        for i in range( 0, _num_element ):
            for j in range( 0, _num_element ):
                tot = np.sum(_aij_prod[i][j]*nj)
                self.ch[i][j] = tot
                
                
        #determine the delta n coeff for 2.24, dln/dlnT coeff for 2.56, and dln/dlP coeff 2.64
        #and pi coef for 2.26,  dpi/dlnT for 2.58, and dpi/dlnP for 2.66
        #and self.rhs of 2.64
        
        #determine the delta coeff for 2.24 and pi coef for 2.26\  
        self.ch[_num_element,:-1]= b
        self.ch[:-1,_num_element]= b

        #determine delta n coef for eq 2.26
        sum_nj = np.sum(nj)
        self.ch[-1,-1] = sum_nj - nmoles

        #determine right side of matrix for eq 2.24
        for i in range(_num_element ):
            sum_aij_nj_muj = np.sum(aij[i]*nj*self.mu)
            self.rhs[i] = sum_aij_nj_muj + b0[i] - b[i]

        #determine the right side of the matrix for eq 2.36
        sum_nj_muj = np.sum(nj*self.mu)
        self.rhs[-1] = nmoles - sum_nj + sum_nj_muj
    
