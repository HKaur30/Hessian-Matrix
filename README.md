# Hessian-Matrix
HessVsFit.py contains code for getting symbolic expression of Gibb's Energy function from a TDB file in pyCalphad software. Later using sympy Univariate Spline curve fitting is done. Compared the data received from hessian with the fitted data. It was almost same. This code is for binary but can be extended to multi-component system by just adding a for loop in the function to differentiate with respect to each components and create an arrayto store hessian components function.

Main_work (4).py contains a eneric Python Code to read an input file containing tdb to extract the components and phases available in the system, further to get user defined Gibbs function for all the phases available in the system and to get the hessian components for all the functions. Later to generate a code for all the
function into a common c file. 

In the get_functions function Mu is calculated, which is the first differential of Gibbs energy with respect to composition and Hessian which is double differential of Gibbs energy with respect to composition. A matrix is created to store the Mu and hessian. 

The function taken as input was as a string so  parse_expr() was used to convert into symbolic expression and this symbolic expression is passed as an argument to the get_functions function.

To get the c code for each function in same c file, we have to combine everything in a matrix and give that as input. So matrix was created named Matrix. 
sympy.utilities.codegen import codegen is used to generate the c code.

alzn_mey.tdb contains thermodynamic database of an binary Al-Zn system.

thermo.c.txt contains generated c code.
