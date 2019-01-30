
import sys
import os

currentdirectory = os.path.dirname(os.path.realpath(__file__))


sys.path.append(currentdirectory+"/packages/ply/")
sys.path.append(currentdirectory+"/packages/plyj/")
sys.path.append(currentdirectory+"/packages/pyparsing/")
sys.path.append(currentdirectory+"/packages/pycparser1/")
sys.path.append(currentdirectory+"/packages/pycparserext/")
sys.path.append(currentdirectory+"/packages/regex/")
sys.path.append(currentdirectory+"/packages/mpmath/")
sys.path.append(currentdirectory+"/packages/sympy/")
sys.path.append(currentdirectory+"/packages/z3/python/")

import subprocess
import FOL_translation
import utiles_translation
import time
import datetime
import regex
from sympy import *
from pyparsing import *
from sympy.core.relational import Relational
from pycparser1 import parse_file,c_parser, c_ast, c_generator
from pycparserext.ext_c_parser import GnuCParser
from pycparserext.ext_c_generator import GnuCGenerator




_infix_op = ['=','==','!=','<','<=','>','>=','*','**','+','-','/', '%', 'implies','<<','>>','&','|']



current_milli_time = lambda: int(round(time.time() * 1000))

"""
#Get timestap
"""

def getTimeStamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return "\n***********************\n"+str(st)+"\n***********************\n"


def programPrint(statement):
    generator = GnuCGenerator()
    return str(generator.visit(statement))




def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True




def is_number(s):
    if s=='j':
    	return False
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True

def is_hex(input_string):
        flag=True
        if input_string is None:
            return None
        try:
            flag=int(input_string, 16)
        except ValueError:
            return None
	if flag:
		if '0x' in input_string:
    			return str(int(input_string, 16))
    		else:
    			return None
	else:
    		return None




"""
Reading the contain of the file 
"""
def readingFile( filename ):
	content=None
	with open(currentdirectory+"/"+filename) as f:
    		content = f.readlines()
    	return content
 
"""
Wrtitting the contain on file 
"""
def writtingFile( filename , content ):
	file = open(currentdirectory+"/"+filename, "w")
	file.write(str(content))
	file.close()

"""
Appending the contain on file 
"""
def appendingFile( filename , content ):
	file = open(currentdirectory+"/"+filename, "a")
	file.write(str(content))
	file.close()

"""

write logs

"""

def writeLogFile(filename , content):
	if os.path.isfile(currentdirectory+"/"+filename):
    		appendingFile( filename , content )
	else:
    		writtingFile( filename , content )


# variables introduced in the translation

def isvariable(x):
    if x.startswith('_x') or  x.startswith('_y') or  x.startswith('_n') or  x.startswith('_s'):
        return True
    else:
        return False



# program variables and temporary program variables and big N

def is_program_var(x,v):
    if x.startswith('_N'):
        return True
    for y in v:
        if x==y or x.startswith(y+OUT) or (x.startswith(y+TEMP) and 
                                           x[len(y+TEMP):].isdigit()) or x.startswith(y+LABEL):
            return True
    return False



#Find Intersection of Two lists


def intersect3(c1,c2,c3):
	return list(set(list(set(c1) & set(c2)))-set(c3))

def intersect2(c1,c2):
	return list(set(c1) & set(c2))
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True




def is_number(s):
    if s=='j':
    	return False
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True

def is_hex(input_string):
        flag=True
        if input_string is None:
            return None
        try:
            flag=int(input_string, 16)
        except ValueError:
            return None
	if flag:
		if '0x' in input_string:
    			return str(int(input_string, 16))
    		else:
    			return None
	else:
    		return None


#Find Intersection of Two lists


def intersect3(c1,c2,c3):
	return list(set(list(set(c1) & set(c2)))-set(c3))

def intersect2(c1,c2):
	return list(set(c1) & set(c2))
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True




def is_number(s):
    if s=='j':
    	return False
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True

def is_hex(input_string):
        flag=True
        if input_string is None:
            return None
        try:
            flag=int(input_string, 16)
        except ValueError:
            return None
	if flag:
		if '0x' in input_string:
    			return str(int(input_string, 16))
    		else:
    			return None
	else:
    		return None


#Find Intersection of Two lists


def intersect3(c1,c2,c3):
	return list(set(list(set(c1) & set(c2)))-set(c3))

def intersect2(c1,c2):
	return list(set(c1) & set(c2))


"""

axiomes to Z3 statements

"""


"""
#Test Case 1
#variable="n1"

#Test Case 2
#variable="_n1"

"""


def isConstant( variable ):
	status=False
	find=regex.compile(r'[_]N\d')
	group = find.search(variable)
	if group is not None:
		status=True
	return status


#fun_name="ackermann_2"

#fun_list=['ackermann']

def isRecurrenceFun( fun_name, fun_list ):
	status=False
        for fun in fun_list:
            if fun_name.startswith(fun+'_')==True:
                digit=fun_name.replace(fun+'_', '')
                if is_number(digit)==True:
                    return fun
	return None






def constructAndOrlist(e_array,operator):
	if len(e_array)>2:
                cond=[]
                cond.append(operator)
                cond.append(e_array[0])
                cond.append(constructAndOrlist(e_array[1:],operator))
		return cond
	if len(e_array)==2:
                cond=[]
                cond.append(operator)
                cond.append(e_array[0])
                cond.append(constructAndOrlist(e_array[1:],operator))
		return cond
	else:
		return e_array[0]





def constructAndOr(e_array,operator):
	if len(e_array)>2:
		return operator+'('+e_array[0]+','+constructAndOr(e_array[1:],operator)+')'
	if len(e_array)==2:
		return operator+'('+e_array[0]+','+e_array[1]+')'
	else:
		return e_array[0]
                
                
def constructAndOrArray(e_array,operator):
	if len(e_array)>2:
		return eval("['"+operator+"',"+str(e_array[0])+','+str(constructAndOrArray(e_array[1:],operator))+']')
	if len(e_array)==2:
		return eval("['"+operator+"',"+str(e_array[0])+','+str(e_array[1])+']')
	else:
		return e_array[0]






"""
#Test Case 1
#variable="n1"

#Test Case 2
#variable="_n1"

"""


def isLoopvariable( variable ):
	status=False
	find=regex.compile(r'[_]n\d')
	group = find.search(variable)
	if group is not None:
		status=True
	return status


"""
#Test Case 1
#variable="C1"

#Test Case 2
#variable="C0"

"""


def isConstInResult( variable ):
	status=False
	find=regex.compile(r'C\d')
	group = find.search(variable)
	if group is not None:
		status=True
	return status


#Test Case 1
#variable="d1array4"

#Test Case 2
#variable="d1ar4"	
	
def isArrayFunction( variable ):
	status=False
	find=regex.compile(r'([d]\d[a][r][r][a][y]\d|[d]\d[a][r][r][a][y])')
	group = find.search(variable)
	if group is not None:
		status=True
	return status


#Is Boolean Variable

#Test Case 1
#variable="bool_go_error1"

#Test Case 2
#variable="bool_go_error2"	
	
def isBoolVariable( variable ):
	status=False
	find=regex.compile(r'([b][o][o][l][_][g][o][_])')
	group = find.search(variable)
	if group is not None:
		status=True
	return status




#expression='n+1'

def replaceAddOperator(expression):
	p = regex.compile(r'[A-Za-z|\d|\)|\]][+][A-Za-z|\d|\(|\]]')
	result=(p.sub(lambda m: m.group().replace("+", " + "), expression))
	result=replaceAddOperator1(result)
	return result

def replaceAddOperator1(expression):
	p = regex.compile(r'[A-Za-z|\d|\s][+][A-Za-z|\d]')
	result=(p.sub(lambda m: m.group().replace("+", "+ "), expression))
	return result
	



#Is Varible is Substitution Variable
# variable = 'f1_1_i'
def isSubsVar( variable ):
	status=False
	find=regex.compile(r'f\d[_]\d')
	group = find.search(variable)
	if group is not None:
		status=True
	return status



#get variable
def expr2varlist(e,variable_list):
    args=FOL_translation.expr_args(e)    
    op=FOL_translation.expr_op(e)
    if len(args)==0:
    	if '_n' not in op and is_number(op)==False:
    		variable_list.append(op)
    else:
        if op=='and' or op=='or':
            if len(args)==1:
               expr2varlist(args[0],variable_list)
            else:
                for x in args:
                    expr2varlist(x,variable_list)
        elif op=='not' and len(args)==1:
            expr2varlist(args[0],variable_list)
        elif op=='implies' and len(args)==2:
        	expr2varlist(args[0],variable_list)
        	expr2varlist(args[1],variable_list)
        elif op in _infix_op and len(args)==2:
        	expr2varlist(args[0],variable_list)
        	expr2varlist(args[1],variable_list)
        else:
            for x in args:
        	expr2varlist(x,variable_list)


#return the list of program variables in an expression 

def expr_func(e,v): #e - expr
    ret = []
    f = FOL_translation.expr_op(e)
    if is_program_var(f,v) or '__VERIFIER_nondet' in f:
        ret.append(f)
    for e1 in FOL_translation.expr_args(e):
        ret = ret + expr_func(e1,v)
    return ret
    

#substitution of functors: in e, replace functor n1 by n2
def expr_sub(e,n1,n2): # e - expr; n1,n2 - strings
    e1=list(expr_sub(x,n1,n2) for x in e[1:])
    if e[0]==n1:
        return [n2]+e1
    else:
        return e[:1]+e1
        

#substitution of functors in a set: in e, for all x in v1 but not in v2, replace x+n1 by x+n2
def expr_sub_set(e,n1,n2,v1,v2): #e - expr; n1,n2 - strings, v1, v2 - sets of strings
    e1 = list(expr_sub_set(e2,n1,n2,v1,v2) for e2 in e[1:])
    if e[0].endswith(n1):
        x = e[0][:len(e[0])-len(n1)]
        if (x in v1) and (not x in v2):
            return [x+n2]+e1
        else:
            return e[:1]+e1
    else:
        return e[:1]+e1
        
        

# expr_replace(e,e1,e2): replace all subterm e1 in e by e2

def expr_replace(e,e1,e2): #e,e1,e2: expr
    if e==e1:
        return e2
    else:
        return e[:1]+list(expr_replace(x,e1,e2) for x in FOL_translation.expr_args(e))
        



# expr_replace(e,e1,e2): replace all subterm e1 in e by e2

#e=['a', ['implies', ['<', ['_n1'], ['_N1']], ['<', ['x2', ['_n1']], ['y2', ['_n1']]]]]

#e=['a', ['<', ['x2', ['_N1']], ['y2', ['_N1']]]]

def expr_complement(e): #e,e1,e2: expres
    if e[:1]==['!']:
        return e[1:][0]
    elif e[:1]==['<']:
    	e[:1]=['>=']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['>']:
    	e[:1]=['<=']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['>=']:
        e[:1]=['<']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['<=']:
        e[:1]=['>']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['==']:
        e[:1]=['!=']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['!=']:
        e[:1]=['==']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['&&']:
        e[:1]=['||']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['||']:
        e[:1]=['&&']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['and']:
        e[:1]=['or']
        return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    elif e[:1]==['or']:
        e[:1]=['and']
    	return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))
    else:
        return e[:1]+list(expr_complement(x) for x in FOL_translation.expr_args(e))





        

# expr_sub_dict(e,d): d is a dictonary of substitutions: functor 'f' to e1=d['f'] so that in e, each f term f(t1,...,tk) is replaced by e1(_x1/t1,...,_xk/tk)

def expr_sub_dict(e,d):
    args = FOL_translation.expr_args(e)
    args1 = list(expr_sub_dict(x,d) for x in args)
    if FOL_translation.expr_op(e) in d:
        return expr_sub_var_list(d[FOL_translation.expr_op(e)],list(expres('_x'+str(i+1)) for i in range(len(args))),args1)
    else:
        return expres(FOL_translation.expr_op(e),args1)
        

# expr_sub_var_list(e,l1,l2): in e, replace all terms in l1 by the corresponding terms in l2

def expr_sub_var_list(e,l1,l2): #e: expr, l1,l2: lists of the same length of exprs
    for i,x in enumerate(l1):
        if e==x:
            return l2[i]
    return e[:1]+list(expr_sub_var_list(y,l1,l2) for y in expr_args(e))


# compute E[n] extend(e,n,excl,v). n is an expr like ['_n1'], excl is a container of strings that are not to be extended
def extend(e,n,excl,v):
    op = FOL_translation.expr_op(e)
    x = [n] if (is_program_var(op,v) and not (op in excl)) or '__VERIFIER_nondet' in op else []
    return expres(op, list(extend(e1,n,excl,v) for e1 in FOL_translation.expr_args(e)) + x)


#A dictionary of dependencies para is such that, if x is an input variable, then para[x] is a list whose first element is 1 and the second element is the variable's parameter name; otherwise, para[x] is the list of input variables that x is depended on. 
#example: para = { 'X':[1,['_y1']], 'X11':[0,['_y1','_y2'], ['X','Y']],...} meaning 'X' is an input variable parameterized as '_y1' and 'X11' is a function depending on X and Y whose corresponding parameters are '_y1' and '_y2', respectively.
#So after parameterization, X11(a,X) will become X11(a,_y1,_y1,_y2)

def parameterize_expres(e,para): 
    if e[0] in para:
        if para[e[0]][0] == 1:
            return para[e[0]][1]+list(parameterize_expres(x,para) for x in e[1:])
        else:
            return e[:1]+list(parameterize_expres(x,para) for x in e[1:])+para[e[0]][1]
    else:
        return e[:1]+list(parameterize_expres(x,para) for x in e[1:])


#parameterize non-input functions then restore the input variables to its name
#given above para, X11(a,X) will become X11(a,X,X,Y), assuming that _y2 corresponds to Y

def parameterize_expr_sub(e,para): 
    if e[0] in para:
        if para[e[0]][0] == 1:
            return [e[0]]+list(parameterize_expr_sub(x,para) for x in e[1:])
        else:
            return e[:1]+list(parameterize_expr_sub(x,para) for x in e[1:])+para[e[0]][2]
    else:
        return e[:1]+list(parameterize_expr_sub(x,para) for x in e[1:])



def substituteValue(expression,key,value):
	if '/' in str(expression):
		#no,deno=fraction(together(expression))
		no,deno=fraction(expression)
		no=sympify(no).expand(basic=True)
		no=no.subs(simplify(key),simplify(value))
		deno=deno.subs(simplify(key),simplify(value))
		if deno==1:
			return powsimp(no)
		else:
                 	return Mul(powsimp(no), Pow(powsimp(deno), -1), evaluate=False)
	
	else:
		return simplify(expression).subs(simplify(key),simplify(value))
                
                
                
                
                
def simplify_sympy(expression):
        #if '/' in str(expression) and '>' not in str(expression) and '<' not in str(expression) and '=' not in str(expression):  
        if '<<' in str(expression) or '>>' in str(expression):
		return expression 
        if sympify(expression)==True or sympify(expression)==False:
		return expression        
        if '/' in str(expression):
        	expression,flag=expressionChecking(expression)
        	if flag==True:
        		expression_mod=expression 
        	else:
        		expression_mod=powsimp(expression)
        else:
            if 'array' not in str(expression):
                expression_mod=powsimp(expression)
            else:
                expression_mod=expression 
    
	if '/' not in str(expression_mod) and 'E' not in str(expression_mod) and 'e' not in str(expression_mod):
		expression=expression_mod
	if '/' in str(expression):
		no,deno=fraction(together(expression))
		no=sympify(no).expand(basic=True)
		deno=sympify(deno).expand(basic=True)
		if deno==1:
			expression,flag=expressionChecking(expression)
			if flag==True:
				return expression
				#return pow_to_mul(powsimp(expression))
			else:
				return pow_to_mul(powsimp(expression))
			#return pow_to_mul(powsimp(no))
		else:
                 	return Mul(pow_to_mul(powsimp(no)), Pow(pow_to_mul(powsimp(deno)), -1), evaluate=False)
	
	else:
		#return str(sympify(expression).expand(basic=True))
		if type(expression) is str:
                    return expression
                else:
                    expressiontemp=sympify(expression).expand(basic=True)
                    if '/' in str(expressiontemp):
                            return pow_to_mul(powsimp(sympify(expression)))
                    else:
                            return pow_to_mul(powsimp(sympify(expression).expand(basic=True)))






"""
#Function to Simplify and Expand an expression using sympy
"""
def simplify_expand_sympy(expression):
    if 'If' in str(expression) or '%' in str(expression):
    	return expression
    if 'Implies' not in expression and 'ite' not in expression and '==' not in  expression and '!=' not in  expression and 'And' not in  expression and 'Or' not in  expression and 'Not' not in  expression and 'ForAll' and 'Exists' not in  expression and 'Implies' not in expression:
    	return str(simplify_sympy(expression))
    elif 'Implies' in expression :
        axioms=extract_args(expression)
        if len(axioms)==2:
            #return 'Implies('+simplify_expand_sympy(axioms[0])+','+simplify_expand_sympy(axioms[1])+')'
            return 'Implies('+axioms[0]+','+simplify_expand_sympy(axioms[1])+')'
        else:
            return expression
    elif 'ite' in expression and 'And' not in  expression and 'Or' not in  expression and 'Not' not in  expression and 'ForAll' and 'Exists' not in  expression and 'Implies' not in expression:
        axioms=extract_args(expression)
        if len(axioms)==3:
            return 'If('+simplify_expand_sympy(axioms[0])+','+simplify_expand_sympy(axioms[1])+','+simplify_expand_sympy(axioms[2])+')'
        else:
            return expression
    elif '==' in  expression and '!=' not in  expression and 'and' not in  expression and 'or' not in  expression and 'And' not in  expression and 'Or' not in  expression and 'Not' not in  expression and 'ForAll' and 'Exists' not in  expression and 'Implies' not in expression:
        left =None
        right =None
        left,right,expression=parenthesesOrganizer( expression ,left ,right)
        axioms=expression.split('==')
        if len(axioms)!=2:
            return expression
        if left is not None and right is not None:
        	if '%' in axioms[0]:
        		leftin =None
			rightin =None
        		leftin,rightin,axioms[0]=parenthesesOrganizer( axioms[0] ,left ,right)
        		axm=axioms[0].split('%')
        		if left is not None and right is not None:
        			expression="("+left+leftin+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+rightin+')==('+str(simplify_sympy(axioms[1]))+right+")"
        		else:
        			expression="("+left+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+')==('+str(simplify_sympy(axioms[1]))+right+")"
        	
        	else:
        		expression="("+left+str(simplify_sympy(axioms[0]))+')==('+str(simplify_sympy(axioms[1]))+right+")"
        		#expression=left+str(pow_to_mul(powsimp(sympify(axioms[0])).expand(basic=True)))+'=='+str(powsimp(pow_to_mul(sympify(axioms[1])).expand(basic=True)))+right
        else:
        	if '%' in axioms[0]:
			leftin =None
			rightin =None
			leftin,rightin,axioms[0]=parenthesesOrganizer( axioms[0] ,left ,right)
			axm=axioms[0].split('%')
			if left is not None and right is not None:
				expression=left+leftin+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+rightin+'=='+str(simplify_sympy(axioms[1]))+right
			else:
				expression=left+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+'=='+str(simplify_sympy(axioms[1]))+right
		        	
        	else:
        		expression=str(simplify_sympy(axioms[0]))+'=='+str(simplify_sympy(axioms[1]))
        		#expression=str(pow_to_mul(powsimp(sympify(axioms[0])).expand(basic=True)))+'=='+str(pow_to_mul(powsimp(sympify(axioms[1])).expand(basic=True)))
        return expression
    elif '!=' in  expression and 'and' not in  expression and 'or' not in  expression and 'And' not in  expression and 'Or' not in  expression and 'Not' not in  expression and 'ForAll' and 'Exists' not in  expression and 'Implies' not in expression:
        left =None
        right =None
        left,right,expression=parenthesesOrganizer( expression ,left ,right)
        axioms=expression.split('!=')
        if len(axioms)!=2:
            return expression
        if left is not None and right is not None:
              	if '%' in axioms[0]:
	        	leftin =None
			rightin =None
	        	leftin,rightin,axioms[0]=parenthesesOrganizer( axioms[0] ,left ,right)
	        	axm=axioms[0].split('%')
	        	if leftin is not None and rightin is not None:
	        		expression=left+leftin+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+rightin+'=='+str(simplify_sympy(axioms[1]))+right
	        	else:
        			expression=left+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+'=='+str(simplify_sympy(axioms[1]))+right
        	else:
        		expression=left+str(simplify_sympy(axioms[0]))+'!='+str(simplify_sympy(axioms[1]))+right
        		#expression=left+str(powsimp(pow_to_mul(sympify(axioms[0])).expand(basic=True)))+'!='+str(pow_to_mul(powsimp(sympify(axioms[1])).expand(basic=True)))+right
        else:
        	 if '%' in axioms[0]:
		 	leftin =None
			rightin =None
			leftin,rightin,axioms[0]=parenthesesOrganizer( axioms[0] ,left ,right)
			axm=axioms[0].split('%')
			if leftin is not None and rightin is not None:
				expression=left+leftin+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+rightin+'=='+str(simplify_sympy(axioms[1]))+right
			else:
		        	expression=left+str(simplify_sympy(axm[0]))+'%'+str(simplify_sympy(axm[1]))+'=='+str(simplify_sympy(axioms[1]))+right

        	 else:
        		expression=str(simplify_sympy(axioms[0]))+'!='+str(simplify_sympy(axioms[1]))
        		#expression=str(pow_to_mul(powsimp(sympify(axioms[0])).expand(basic=True)))+'!='+str(pow_to_mul(powsimp(sympify(axioms[1])).expand(basic=True)))
        return expression
    else:
        return  expression







"""
Function to Take care of the parentheses During 

#substitutor='(X2(_N1(B,A),A,B)'
#left=None
#right=None

"""
def parenthesesOrganizer( substitutor ,left ,right):
	if left is None:
		left=""
	if right is None:
		right=""
	if substitutor[0]=="(":
		left=left+"("
		substitutor=substitutor[1:len(substitutor)]
		if substitutor[len(substitutor)-1]==")":
			right=right+")"
			substitutor=substitutor[0:len(substitutor)-1]
			leftin=None
			rightin=None
			leftin,rightin,substitutor_update=parenthesesOrganizer(substitutor,leftin ,rightin)
			if leftin is not None and rightin is not None:
				substitutor=leftin+substitutor_update+rightin
		else:
			substitutor="("+substitutor
			left=left[0:len(left)-1]
	return left,right,substitutor





"""
#Extract arguments from smallest function

#Example 1: expr="smallest(n,_N1,su(n)>X(n))"
#extract_args(expr):

"""
def extract_args(expr):
    paren = 0
    start = 0
    ret = []
    for i, c in enumerate(expr):
        if c=='(':
            paren+=1
            if paren==1:
                start=i+1
        elif c==')':
            if paren==1 and start:
                ret.append(expr[start: i]) 
            paren-=1
        elif c==',' and paren==1:
            ret.append(expr[start:i])
            start=i+1
    return ret








"""
Expanding algebraic powers
"""

def pow_to_mul(expression):
    """
    Convert integer powers in an expression to Muls, like a**2 => a*a(Only for Squre).
    """
    #expression=simplify(expression).expand(basic=True)
    #expression=simplify(expression)
    pows=list(expression.atoms(Pow))
    if any(not e.is_Integer for b, e in (i.as_base_exp() for i in pows)):
    	#A power contains a non-integer exponent
    	return expression
    repl=None
    for b,e in (i.as_base_exp() for i in pows):
    	if e==2:
    		repl = zip(pows,((Mul(*[b]*e,evaluate=False)) for b,e in (i.as_base_exp() for i in pows)))
    if repl is not None:
    	return expression.subs(repl)
    else:
    	return expression
    
    
    
#substituting close form solution in rest of the axiomes
def solnsubstitution(axioms,key,substituter):
	update_axioms=[]
    	for axiom in axioms:
    		if axiom[0]!='i0' and axiom[0]!='i1':
               		update_axioms.append(expr_replace(axiom,key,substituter))
    		else:
                        if axiom[0]=='i1':
                            axiom[4]=expr_replace(axiom[4],key,substituter)
                            update_axioms.append(axiom)
                        elif axiom[0]=='i0':
                            axiom[3]=expr_replace(axiom[3],key,substituter)
                            update_axioms.append(axiom)
                        else:
                            update_axioms.append(axiom)
    	return update_axioms



    
def solnsubstitution_Array(axioms,key,substituter):
	update_axioms=[]
    	for axiom in axioms:
    		if axiom[0]!='i0' and axiom[0]!='i1':
               		update_axioms.append(expr_array_replace(axiom,key,substituter))
    		else:
                        if axiom[0]=='i1':
                            axiom[4]=expr_array_replace(axiom[4],key,substituter)
                            update_axioms.append(axiom)
                        elif axiom[0]=='i0':
                            axiom[3]=expr_array_replace(axiom[3],key,substituter)
                            update_axioms.append(axiom)
                        else:
                            update_axioms.append(axiom)
    	return update_axioms

def translatepowerToFunCheck(expression):
    if "**" in expression:
    	expression=transferToFunctionSyntax(str(expression))
    	xform = expr.transformString(expression)[1:-1]
    	xform=xform.replace('[','(')
    	expression=xform.replace(']',')')
   	#print expression
    return expression

#expression="(A+B+((Z**(K)-1)/(Z-1))*(Z-1))"
#expression="((Z**(K)-1)/(Z-1))*(Z-1)"
#expression="(Z/2)*6<=Z"
#expression="r6(_n2)>=(((2**-(_n2))*((2**_N1)*B))/2)"
#expressionChecking(expression)
def expressionChecking(expression):
	if '(((((((' not in str(expression):
		if "**" in str(expression):
			expression=translatepowerToFunCheck(str(expression))
		#p = getParser()
                parser = c_parser.CParser()
		#tree = p.parse_expression(expression)
                ast = parser.parse("void test(){"+str(expression)+";}")
		statement_temp=ast.ext[0].body.block_items[0]
		#expr_wff=eval(expressionCreator(tree)) 
                expr_wff = eval(utiles_translation.expressionCreator_C(statement_temp))
		flag=False
		return expr2simplified(expr_wff,flag)
	else:
		return str(expression),False




#Parsing Method Starts

# define some basic operand expressions
number = Regex(r'\d+(\.\d*)?([Ee][+-]?\d+)?')
ident = Word(alphas+'_', alphanums+'_')
#fn_call = ident + '(' + Optional(delimited_list(expr)) + ')'

# forward declare our overall expression, since a slice could 
# contain an arithmetic expression
expr = Forward()
#slice_ref = '[' + expr + ']'

slice_ref = '[' + expr + ZeroOrMore("," + expr) + ']'

# define our arithmetic operand
operand = number | Combine(ident + Optional(slice_ref))
#operand = number | fn_call | Combine(ident + Optional(slice_ref))
inequalities = oneOf("< > >= <= = == !=")

# parse actions to convert parsed items
def convert_to_pow(tokens):
    tmp = tokens[0][:]
    ret = tmp.pop(-1)
    tmp.pop(-1)
    while tmp:
        base = tmp.pop(-1)
        # hack to handle '**' precedence ahead of '-'
        if base.startswith('-'):
            ret = '-power(%s,%s)' % (base[1:], ret)
        else:
            ret = 'power(%s,%s)' % (base, ret)
        if tmp:
            tmp.pop(-1)
    return ret

def unary_as_is(tokens):
    return '(%s)' % ''.join(tokens[0])

def as_is(tokens):
    return '%s' % ''.join(tokens[0])


# simplest infixNotation - may need to add a few more operators, but start with this for now
arith_expr = infixNotation( operand,
    [
    ('-', 1, opAssoc.RIGHT, as_is),
    ('**', 2, opAssoc.LEFT, convert_to_pow),
    ('-', 1, opAssoc.RIGHT, unary_as_is),
    ((inequalities,inequalities), 3, opAssoc.LEFT, as_is),
    (inequalities, 2, opAssoc.LEFT, as_is),
    (oneOf("* /"), 2, opAssoc.LEFT, as_is),
    (oneOf("+ -"), 2, opAssoc.LEFT, as_is),
    (oneOf('and or'), 2, opAssoc.LEFT, as_is),
    ])
#('-', 1, opAssoc.RIGHT, as_is),
# now assign into forward-declared expr
expr <<= arith_expr.setParseAction(lambda t: '(%s)' % ''.join(t))

"""
#expression="2**3"
#expression="2**-3"
#expression="2**3**x5"
#expression="2**-3**x6[-1]"
#expression="2**-3**x5+1"
#expression="(a+1)**2"
#expression="((a+b)*c)**2"
#expression="B**2"
#expression="-B**2"
#expression"(-B)**2"
#expression="B**-2"
#expression="B**(-2)"
#expression="((Z**(_N1+1)-1)/(Z-1))*(Z-1))"
#expression="((_N1+1)**2)<=X"
#expression="_n2*_n3*_N1(_n2, _n3)**2/2"
#translatepowerToFun(expression)
#expression="_n2*_n3*_N1(_n2, X(_n3))**2/2"

#expression="(((2.00000000000000)+_n2*_n3*_N1(_n2, X(_n3))**2/2))"

"""

def translatepowerToFun(expression):
    if "**" in expression:
        try:
            backup_expression=expression
            if ("<" in  expression or ">" in  expression) and '/' not in expression :
                expression=simplify(expression)
            expression=transferToFunctionSyntax(str(expression))
            xform = expr.transformString(expression)[1:-1]
            #xform = expr.transformString(expression)
            xform=xform.replace('[','(')
            expression=xform.replace(']',')')
        except Exception as e:
            expression=backup_expression
   	#print expression
    return expression
 
 
 

"""
Example 1:
>>> expression="x(n)+(y(n)+1)*n"
>>> transferToMathematicaSyntax(expression)
'x[n]+(y[n]+1)*n'

Example 2:

>>> expression="x(n(a,b),a,b)+2^(y(_N1(a,b),a,b)+1)"
>>> transferToMathematicaSyntax(expression)
'x[n[a,b],a,b]+2^(y[_N1[a,b],a,b]+1)'

Example 3:

>>> expression="x(n)+(y(n)/(_N1(n)))"
>>> transferToMathematicaSyntax(expression)
'x[n]+(y[n]/(_N1(n)))'

"""

#Changing function of the formate f(n) to f[n]. It assist the pasring 

def transferToFunctionSyntax(expression):
	if "(" in expression and ")" in expression:
		p = regex.compile(r'\b[a-zA-Z_]\w*(\((?>[^()]|(?1))*\))')
		result=(p.sub(lambda m: m.group().replace("(", "[").replace(")", "]"), expression))
	else:
		result=expression
	return result


#wff to Simplified Expression
def expr2simplified(e,flag):
    args=FOL_translation.expr_args(e)
    op=FOL_translation.expr_op(e)
    if len(args)==0:
        return op,flag
    else:
	if op in _infix_op and len(args)==2:
	    expr1,flag=expr2simplified(args[0],flag)
	    if flag==True:
	    	expr2,flag=expr2simplified(args[1],flag)
	    	flag=True
	    else:
	    	expr2,flag=expr2simplified(args[1],flag)
	    if op=='*' and FOL_translation.expr_op(args[0])=='/':
	    	n,d=fraction(expr1)
	    	if gcd(d,expr2)!=1:
	    		flag=True
	    elif op=='/' and FOL_translation.expr_op(args[0])=='*':
	    	n,d=fraction(expr2)
	    	if gcd(expr1,d)!=1:
	    		flag=True
            if flag==True:
            	expression= '(' + expr1+ op + expr2 +')' 
            else:
            	expression= '((' + str(pow_to_mul(powsimp(expr1)))+ ')'+ op + '('+ str(pow_to_mul(powsimp(expr2)))+'))' 
            return expression,flag
        else:
            return op +'('+ ','.join(list(FOL_translation.trim_p(FOL_translation.expr2string1(x)) for x in args))+ ')',flag
        
        
        
"""
#Is Function Present 

"""
def isVariablePresent(e):
    args=FOL_translation.expr_args(e)
    op=FOL_translation.expr_op(e)
    if len(args)==0:
        if op.startswith('_n')==True or op.startswith('_x')==True:
            return true
    else:
        if op=='and' or op=='or':
            if len(args)==1:
                if isVariablePresent(args[0])==True:
                    return True
            else:
                status=False
                for x in args:
                    if isVariablePresent(x)==True:
                        return True
        elif op=='not' and len(args)==1:
            return isFunctionPresent(args[0])
        elif op=='implies' and len(args)==2:
             if isVariablePresent(args[0])==True or isVariablePresent(args[1])==True:
                 return True
        elif op in _infix_op and len(args)==2:
            if isVariablePresent(args[0])==True or isVariablePresent(args[1])==True:
                return True
        else:
            for x in args:
                if isVariablePresent(x)==True:
                    return True
    return None

    
    
"""
#Is Function Present 

"""
def isFunctionPresent(e):
    args=FOL_translation.expr_args(e)
    op=FOL_translation.expr_op(e)
    if len(args)==0:
        if op.startswith('_n')==True or op.startswith('_x')==True:
            return None
    else:
        if op=='and' or op=='or':
            
            if len(args)==1:
                if isFunctionPresent(args[0])==True:
                    return True
            else:
                status=False
                for x in args:
                    if isFunctionPresent(x)==True:
                        return True
        elif op=='not' and len(args)==1:
            return isFunctionPresent(args[0])
        elif op=='implies' and len(args)==2:
             if isFunctionPresent(args[0])==True or isFunctionPresent(args[1])==True:
                 return True
        elif op in _infix_op and len(args)==2:
            if isFunctionPresent(args[0])==True or isFunctionPresent(args[1])==True:
                return True
        else:
            if op !='ite' :
                return True

    return None


"""
#Is Function Present 

"""
def getAllVarFun(e,map_fun,map_var):
    args=FOL_translation.expr_args(e)
    op=FOL_translation.expr_op(e)
    if len(args)==0:
        if op.startswith('_n')==True or op.startswith('_x')==True:
            map_var[op]=op
    else:
        if op=='and' or op=='or':
            
            if len(args)==1:
                getAllVarFun(args[0],map_fun,map_var)
            else:
                for x in args:
                    getAllVarFun(x,map_fun,map_var)
        elif op=='not' and len(args)==1:
            getAllVarFun(args[0],map_fun,map_var)
        elif op=='implies' and len(args)==2:
            getAllVarFun(args[0],map_fun,map_var)
            getAllVarFun(args[1],map_fun,map_var)
        elif op in _infix_op and len(args)==2:
            getAllVarFun(args[0],map_fun,map_var)
            getAllVarFun(args[1],map_fun,map_var)
        else:
            if op !='ite' and '__VERIFIER_' not in op:
                map_fun[op]=op
            for x in args:
                getAllVarFun(x,map_fun,map_var)


"""
#convert all power operator to power function
"""
def convert_pow_op_fun(expression):
    return expression



def conditionSimplifyPower(expression):
	if '/' not in expression and 'Or' not in expression and '==' not in expression and 'And' not in expression and 'If' not in expression and 'char(' not in expression and 'Implies' not in expression:
		return convert_pow_op_fun(simplify_expand_sympy(expression))
	elif 'Or' not in expression and 'And' not in expression and 'If' not in expression and 'char(' not in expression and 'Implies' not in expression:
		return convert_pow_op_fun(expression)
	else:
		return expression
            
            
            
"""

1.Directly translate axoimes to z3 constraint 2.Change  exponential operator ** to power function

"""
def query2z3_update(constraint_list,conclusion,vfact,witnessXml):
	pythonProgram="import sys\n"
        pythonProgram+="import os\n"
        pythonProgram+="currentdirectory = os.path.dirname(os.path.realpath(__file__))\n"
        pythonProgram+="sys.path.append(currentdirectory+\"/packages/setuptools/\")\n"
        pythonProgram+="currentdirectory = os.path.dirname(os.path.realpath(__file__))\n"
        pythonProgram+="sys.path.append(currentdirectory+\"/packages/z3/python/\")\n"
	pythonProgram+="from z3 import *\n"
        pythonProgram+="init(currentdirectory+\"/packages/z3\")\n"
	pythonProgram+="set_param(proof=True)\n"
        pythonProgram+="\ntry:\n"
	pythonProgram+="\t_p1=Int('_p1')\n"
	pythonProgram+="\t_p2=Int('_p2')\n"
	pythonProgram+="\t_n=Int('_n')\n"
        pythonProgram+="\t_bool=Int('_bool')\n"
	pythonProgram+="\tarraySort = DeclareSort('arraySort')\n"
	pythonProgram+="\t_f=Function('_f',IntSort(),IntSort())\n"
        pythonProgram+="\t_ToReal=Function('_ToReal',RealSort(),IntSort())\n"
        pythonProgram+="\t_ToInt=Function('_ToInt',IntSort(),RealSort())\n"
    
        duplicate_map={}

	status=""
	for [x,k,l] in vfact:
		if k==0:
			if ('_PROVE' not in x or '_ASSUME' not in x) and x not in duplicate_map.keys():
				if l[0]=="int":
					if '_N' in x:
						pythonProgram+='\t'+x+"=Const(\'"+x+"\',IntSort())\n"
					else:				
						pythonProgram+='\t'+x+"=Int(\'"+x+"\')\n"
				elif l[0]=="double":
					pythonProgram+='\t'+x+"=Real(\'"+x+"\')\n"
				elif l[0]=="float":
					pythonProgram+='\t'+x+"=Real(\'"+x+"\')\n"
                        	elif l[0]=="Bool":
					pythonProgram+='\t'+x+"=Int(\'"+x+"\')\n"
				elif l[0]=="constant":
					pythonProgram+='\t'+x+"=Const(\'"+x+"\',IntSort())\n"
				elif l[0]=="array":
					if 'array(' not in x:
                                            pythonProgram+='\t'+x+"=Const(\'"+x+"\',arraySort)\n"
				else:
					pythonProgram+='\t'+x+"=Int(\'"+x+"\')\n"
                                duplicate_map[x]=x
		else:
			if ('_PROVE' not in x or '_ASSUME' not in x) and x not in duplicate_map.keys():
				pythonProgram+='\t'+x+"=Function(\'"+x+"\'"
                                duplicate_map[x]=x
				for e in l:
					if e=="int":
						pythonProgram+=",IntSort()"
					elif e=="unsigned":
						pythonProgram+=",IntSort()"
					elif e=="long":
						pythonProgram+=",IntSort()"
					elif e=="Bool":
						pythonProgram+=",IntSort()"
					elif e=="array":
						pythonProgram+=",arraySort"
					else:
						pythonProgram+=",RealSort()"
                                pythonProgram+=")\n"
	power_flag=False
	for equation in constraint_list:
		if '**' in equation or 'power' in equation:
			power_flag=True
	if conclusion is not None:
            if '**' in conclusion or 'power' in conclusion:
		power_flag=True
	if power_flag==True:		
		#pythonProgram+="\tpower=Function(\'power\',IntSort(),IntSort(),IntSort())\n"
                pythonProgram+="\tpower=Function(\'power\',RealSort(),RealSort(),RealSort())\n"
		pythonProgram+="\t_s=Solver()\n"
		#pythonProgram+="_s.add(ForAll(x,Implies(x>0,power(x, 0)==1)))\n"
		#pythonProgram+="_s.add(ForAll([x,y],Implies(And(x>0,y>0),power(x, y)==power(x, y-1)*x)))\n"
		#pythonProgram+="_s.set(mbqi=True)\n"
        	pythonProgram+="\t_s.add(ForAll([_p1],Implies(_p1>=0, power(0,_p1)==0)))\n"
        	pythonProgram+="\t_s.add(ForAll([_p1,_p2],Implies(power(_p2,_p1)==0,_p2==0)))\n"
        	pythonProgram+="\t_s.add(ForAll([_p1],Implies(_p1>0, power(_p1,0)==1)))\n"
        	pythonProgram+="\t_s.add(ForAll([_p1,_p2],Implies(power(_p1,_p2)==1,Or(_p1==1,_p2==0))))\n"
        	pythonProgram+="\t_s.add(ForAll([_p1,_p2],Implies(And(_p1>0,_p2>=0), power(_p1,_p2+1)==power(_p1,_p2)*_p1)))\n"  
        else:
        	pythonProgram+="\t_s=Solver()\n"

	pythonProgram+="\t_s.add(ForAll([_n],Implies(_n>=0, _f(_n)==_n)))\n"
	pythonProgram+="\t_s.set(\"timeout\","+str(500)+")\n"
	for equation in constraint_list:
		pythonProgram+="\t_s.add("+str(equation)+")\n"
	finalProgram=pythonProgram
	#finalProgram+="_s.add(Not("+str(transferToFunctionRec(conclusion))+"))\n"
        if conclusion is not None:
            finalProgram+="\t_s.add(Not("+str(conclusion)+"))\n"
        finalProgram+="\nexcept Exception as e:\n"+"\tprint \"Error(Z3Query)\""+"\n\tfile = open('j2llogs.logs', 'a')\n"+"\n\tfile.write(str(e))\n"+"\n\tfile.close()\n"+"\n\tsys.exit(1)\n"
        finalProgram+="\ntry:\n"
        finalProgram+="\tresult=_s.check()\n\tif sat==result:\n"+"\t\tprint \"Counter Example\"\n"+"\t\tprint _s.model()\n"+"\telif unsat==result:\n"+"\t\tresult\n"+"\t\ttry:\n"+"\t\t\tif os.path.isfile(\'j2llogs.logs\'):\n"+"\t\t\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\t\tfile.close()\n"+"\t\t\telse:\n"+"\t\t\t\tfile = open(\'j2llogs.logs\', \'w\')\n"+"\t\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\t\tfile.close()\n"+"\t\texcept Exception as e:\n"+"\t\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+\"Error\"+\"\\n\")\n"+"\t\t\tfile.close()\n"+"\t\tprint \"Successfully Proved\"\n"+"\telse:\n"+"\t\tprint \"Failed To Prove\""
        #finalProgram+="\tif sat==_s.check():\n"+"\t\tprint \"Counter Example\"\n"+"\t\tprint _s.model()\n"+"\t\twitnessXmlStr="+str(witnessXml)+"\n"+"\t\tmiddle=''\n"+"\t\tfor element in _s.model():\n"+"\t\t\tif str(element)==witnessXmlStr[2]:\n"+"\t\t\t\tmiddle+='<data key=\"assumption\">'+'\\\\'+'result=='+str(_s.model()[element])+'</data>'\n"+"\t\tfile = open(witnessXmlStr[3]+'_witness.graphml', 'w')\n"+"\t\tfile.write(witnessXmlStr[0]+middle+witnessXmlStr[1])\n"+"\t\tfile.close()\n"+"\telif unsat==_s.check():\n"+"\t\t_s.check()\n"+"\t\ttry:\n"+"\t\t\tif os.path.isfile(\'j2llogs.logs\'):\n"+"\t\t\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\t\tfile.close()\n"+"\t\t\telse:\n"+"\t\t\t\tfile = open(\'j2llogs.logs\', \'w\')\n"+"\t\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\t\tfile.close()\n"+"\t\texcept Exception as e:\n"+"\t\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+\"Error\"+\"\\n\")\n"+"\t\t\tfile.close()\n"+"\t\tprint \"Successfully Proved\"\n"+"\telse:\n"+"\t\tprint \"Failed To Prove\""
	finalProgram+="\nexcept Exception as e:\n"+"\tprint \"Error(Z3Query)\""+"\n\tfile = open('j2llogs.logs', 'a')\n"+"\n\tfile.write(str(e))\n"+"\n\tfile.close()\n"
	#finalProgram+="if sat==_s.check():\n"+"\tprint \"Counter Example\"\n"+"\tprint _s.model()\n"+"\twitnessXmlStr="+str(witnessXml)+"\n"+"\tmiddle=''\n"+"\tfor element in _s.model():\n"+"\t\tif str(element)==witnessXmlStr[2]:\n"+"\t\t\tmiddle+='<data key=\"assumption\">'+'\\\\'+'result=='+str(_s.model()[element])+'</data>'\n"+"\tfile = open(witnessXmlStr[3]+'_witness.graphml', 'w')\n"+"\tfile.write(witnessXmlStr[0]+middle+witnessXmlStr[1])\n"+"\tfile.close()\n"+"elif unsat==_s.check():\n"+"\t_s.check()\n"+"\ttry:\n"+"\t\tif os.path.isfile(\'j2llogs.logs\'):\n"+"\t\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\tfile.close()\n"+"\t\telse:\n"+"\t\t\tfile = open(\'j2llogs.logs\', \'w\')\n"+"\t\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\t\tfile.close()\n"+"\texcept Exception as e:\n"+"\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+\"Error\"+\"\\n\")\n"+"\t\tfile.close()\n"+"\tprint \"Successfully Proved\"\n"+"else:\n"+"\tprint \"Failed To Prove\""
	#finalProgram+="if sat==_s.check():\n"+"\tprint \"Counter Example\"\n"+"\tprint _s.model()\n"+"\twitnessXmlStr="+str(witnessXml)+"\n"+"\tmiddle=''\n"+"\tfor element in _s.model():\n"+"\t\tif str(element)!=witnessXmlStr[2]:\n"+"\t\t\tmiddle+='<data key=\"assumption\">'+str(element)[:-1]+'=='+str(_s.model()[element])+'</data>'\n"+"\t\telse:\n"+"\t\t\tmiddle+='<data key=\"assumption\">'+'\\\\'+'result=='+str(_s.model()[element])+'</data>'\n"+"\tfile = open(witnessXmlStr[3]+'_witness.graphml', 'w')\n"+"\tfile.write(witnessXmlStr[0]+middle+witnessXmlStr[1])\n"+"\tfile.close()\n"+"elif unsat==_s.check():\n"+"\t_s.check()\n"+"\tif os.path.isfile(\'j2llogs.logs\'):\n"+"\t\tfile = open(\'j2llogs.logs\', \'a\')\n"+"\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\tfile.close()\n"+"\telse:\n"+"\t\tfile = open(\'j2llogs.logs\', \'w\')\n"+"\t\tfile.write(\"\\n**************\\nProof Details\\n**************\\n\"+str(_s.proof().children())+\"\\n\")\n"+"\t\tfile.close()\n"+"\tprint \"Successfully Proved\"\n"+"else:\n"+"\tprint \"Failed To Prove\""
	#finalProgram+="if sat==_s.check():\n"+"\tprint \"Counter Example\"\n"+"\tprint _s.model()\n"+"elif unsat==_s.check():\n"+"\t_s.check()\n"+"\tprint \"Successfully Proved\"\n"+"else:\n"+"\tprint \"Failed To Prove\""
	#print finalProgram
	writtingFile( "z3query.py" , finalProgram )
	#writeLogFile( "j2llogs.logs" , "\nQuery to z3 \n"+str(finalProgram)+"\n" )
	try :
		proc = subprocess.Popen('python '+currentdirectory+'/z3query.py', stdout=subprocess.PIPE,shell=True)
		output = proc.stdout.read()
		status=output
	except OSError  as err:
		print 'dharilo1'
	return status

            
