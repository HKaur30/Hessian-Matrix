from sympy import *
import pandas as pd
import numpy as np
import sympy as sym
sym.init_printing()
import sys
import re
import sympy

def get_functions(GM,components,t): 
    d_GM = {}
    ln = len(components)
    for i, j in enumerate(components[0:ln-1]):
     d_GM[j] = GM.diff(j) - GM.diff(components[ln-1])
    Mu = [d_GM[j] for j in components[0:ln-1]] 
    Mu_matrix = sym.Matrix(Mu)
    d2_GM={}
    for i, k in enumerate(components[0:ln-1]):
       d2_GM[k]={}
    for i, k in enumerate(components[0:ln-1]):
       for l, m in enumerate(components[0:ln-1]):
           d2_GM[k][m] = Mu[i].diff(m) - Mu[i].diff(components[ln-1])
    Hessian = [[d2_GM[k][m] for m in components[0:ln-1]] for k in components[0:ln-1]]
    Hessian_matrix = sym.Matrix(Hessian)
    return GM,Mu_matrix,Hessian_matrix,ln
    
if __name__=="__main__":  
 with open("Path of text file containing Gibb's Function",'r') as file:
    lines=file.readlines()
    flag = 0
    index = 0
    for line in lines:
        index = index+1
        word = re.match(r'COMPONENTS', line)
        if word:
            flag = 1
            break
    if flag == 0:
        print("Components not found") 
    else:
        Components = []
        Line = lines[index-1]
        component = Line.split("=")[1].replace(';', '').strip()
        components = re.sub(r"[{} ]","",component).split(",")
        for i in range (0,len(components)-1):
         Components.append(components[i])
         print ("Components",i+1," :")
         print (components[i])
    flag = 0
    index = 0
    for line in lines:
        index = index+1
        word = re.match(r'tdb_phases', line)
        if word:
            flag = 1
            break
    if flag == 0:
        print("Phase not found")
    else:
        GM = []
        Lines = lines[index-1]
        phase = Lines.split("=")[1].replace(';', '').strip()
        phases = re.sub(r"[{} ]","",phase).split(",")
        for i in range (0,len(phases)):
         print ("Enter Gibbs Function For Following Phase and composition of components should be in", Components, "representation only :")
         print (phases[i])
         print ()
         GM.append(input())
         print ()
 from sympy.parsing.sympy_parser import parse_expr               
 X = sympy.symbols(Components)
 T = sympy.symbols('T')
 GM_Exp = []
 for j in GM:
  GM_Exp.append(parse_expr(j)) 
 GFE = [sym.symbols('Gibb_%d' %k) for k in range(len(phases))]
 Mu = [sym.symbols('Mu_%d' %k) for k in range(len(phases))]
 hessian = [sym.symbols('hessian_%d' %k) for k in range(len(phases))]
 GM_1 = [sym.symbols('GM_1_%d' %k) for k in range(len(phases))]
 mu_1 = [sym.symbols('mu_1_%d' %k) for k in range(len(phases))]
 hessian_1 = [sym.symbols('hessian_1_%d' %k) for k in range(len(phases))]

 for k in range(len(phases)):
   GM, mu, hessian_M, comps = get_functions(GM_Exp[k],Components,T)
   Gibbs = sym.symbols('Gibb')
   MU = sym.MatrixSymbol('Mu',comps-1,1)
   Hessian = sym.MatrixSymbol('hessian',comps-1,comps-1)
   GM_1[k] = sym.Eq(Gibbs,GM)
   mu_1[k] = sym.Eq(MU,mu)
   hessian_1[k] = sym.Eq(Hessian,hessian_M)
   hessian1 = hessian_M.subs([(X[0],0.6), (X[1], 0.4), (T, 1000)]) 
   print (hessian1)
 Matrix = [(GFE[k].name, GM_1[k]) for k in range(len(phases))] + [(Mu[k].name, mu_1[k]) for k in range(len(phases))] + [(hessian[k].name, hessian_1[k]) for k in range(len(phases))]
 
 from sympy.utilities.codegen import codegen
 codegen(Matrix, language='c', to_files=True, header=True, prefix='Gibbs')
 





      
  



