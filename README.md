# Hessian-Matrix
HessVsFit.py contains code for getting symbolic expression of Gibb's Energy function from a TDB file in pyCalphad software. Later using sympy Univariate Spline curve fitting is done. Compared the data received from hessian with the fitted data. It was almost same. This code is for binary but can be extended to multi-component system by just adding a for loop in the function to differentiate with respect to each components and create an arrayto store hessian components function.

contains a eneric Python Code to read an input file containing tdb to extract the components and phases available in the system. Further to get user defined
Gibbs function for all the phases available in the system and then to get the hessian components for all the functions. Lastly to generate a code for all the
function into a common c file. In the get_functions function we are calculating the Mu which is first differential of Gibbs energy with respect to composition and Hessian which is double differential of Gibbs energy with respect to composition. We will create a matrix to store the Mu and hessian.
In the main, firstly reading the the input file and searching for the keywords
COMPONENTS and tdb_phases to get the composition and the phases present in
the system. Secondly, taking the Gibbs Function as input from the user for all
phases present in the system.
The function taken as input was as a string so using parse_expr()it was
converted to sympy symbolic expression and this symbolic expression was
passed as an argument to the get_functions function.
To get the c code for each function in same c file, we have to combine every
thing in a matrix and give that as input. So matrix was created named Matrix.
sympy.utilities.codegen import codegen is used to generate the c code.
