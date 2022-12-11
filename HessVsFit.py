import sympy as sym
from sympy import pi, sin, cos, var, simplify
import matplotlib.pyplot as plt
import numpy as np
from sympy import*
from pycalphad import Database, Model
import pycalphad.variables as v

import matplotlib.pyplot as plt
from pycalphad import Database, calculate, Model
import pycalphad.variables as v
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
import pandas as pd

def get_hessian(dbf_sys, component_sys,comp1, comp2, Phases):
  mod = Model(dbf_sys, component_sys, Phases)  
  my_list = [v.Y(Phases,0,comp1), v.Y(Phases,0,comp2), v.T]
  gm = mod.GM
  gm_der = gm.diff(my_list[0]) - gm.diff(my_list[1])
  hess_comp = gm_der.diff(my_list[0]) - gm_der.diff(my_list[1])
  return hess_comp
  




if __name__=="__main__":
 dbf = Database('/home/harpreetk/Downloads/alzn_mey.tdb')
 components = ['AL','ZN']
 c_1 = v.Species('AL')
 c_2 = v.Species('ZN')
 phases = 'LIQUID' 
 
 hessian = get_hessian(dbf,components, c_1, c_2, phases)
 
 
 fig = plt.figure(figsize=(9,6))
 ax = fig.gca()

 result = calculate(dbf, ['AL', 'ZN'], phases, P=101325, T=1000, output='GM')
 ax.scatter(result.X.sel(component='AL'), result.GM, marker='.', s=5)
 
 ax.set_xlabel('X(AL)')
 ax.set_ylabel('GM')
 ax.set_xlim((-0.2, 0.99))
 plt.show()

 hessian_array = [] 
 x = [0.12,0.2,0.25,0.3,0.35,0.4, 0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9, 0.95,0.99] 
 for i in x:
  init_printing(use_unicode=True)
  hessian1 = hessian.subs({v.P:101325, v.T:1000, v.Y(phases,0,c_1): i , v.Y(phases,0,c_2):1-i})
  hessian2 = simplify(hessian1)
  hessian_array.append(hessian2)
  
 df_1 = pd.DataFrame({'X':result.X.sel(component='AL').squeeze(),'GM':result.GM.squeeze()})
 df_1 = df_1.sort_values(by='X')
 GM_array = np.unique(df_1.loc[:,'GM']).squeeze()
 AL_array = np.unique(df_1.loc[:,'X']).squeeze()

 #data fitting
 x = AL_array

 y = GM_array


 #InterpolatedUnivariateSpline
 s = interpolate.UnivariateSpline(x, y)
 xnew = np.linspace(0.1, 0.99, num=1000, endpoint=True)
 xnew1 =  np.linspace(0.1, 0.99, num=1000, endpoint=True)
 ynew = s(xnew)
 plt.figure()
 plt.plot(x, y, 'o', xnew, ynew, '-')
 plt.legend(['data', 'cubic'], loc='best')
 plt.title('InterpolatedUnivariateSpline')
 plt.show()
 ynew1 = s.derivative(2)(xnew1) 

 x_plot = [0.12,0.2,0.25,0.3,0.35,0.4, 0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9, 0.95,0.99]
 y_plot = s.derivative(2)(x_plot) 
 z_plot = hessian_array
 
 plt.plot(x_plot, y_plot, color='r', label='fit')
 plt.plot(x_plot, z_plot, color='g', label='hessian')
 
 plt.xlabel("Composition")
 plt.ylabel("Value")
 plt.title("Hessian and Fit")
  
 # Adding legend, which helps us recognize the curve according to it's color
 plt.legend()
  
 # To load the display window
 plt.show()

 

