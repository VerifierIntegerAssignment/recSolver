

import sys
import os

currentdirectory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(currentdirectory+"/packages/mpmath/")
sys.path.append(currentdirectory+"/packages/sympy/")

from sympy import *
from sympy.core.relational import Relational
import fun_utiles
import copy


# base language (non dynamic, not changed by the program)
# do not use name with number in the end
# these names are not supposed to be used as prorgam variables

_base = ['=','==','!=','<','<=','>','>=','*','**','!','+','-','/', '%', 'ite', 'and', 'or', 'not', 'implies', 'all', 'some', 'null','>>','<<','&','|']
_infix_op = ['=','==','!=','<','<=','>','>=','*','**','+','-','/', '%', 'implies','<<','>>','&','|']






"""
RET for return value of a function
Temporary function names are constructed as: 
variable-name + TEMP + TC
Output function names are: 
variable-name + LABEL
for those with label, or
variable-name + OUT
for those without label.
 TC: TempCount, a global counter for naming temporary variables
 LC: LoopCount, a global counter for naming loop constants and variables
"""

RET='RET'
#OUT='Z' #so don't name variables xZ, yZ...
OUT='1' #so don't name variables x1, y1...
#TEMP = 'T' #so if x is a variable, then don't name variables xT, 
TEMP = '' #so if x is a variable, then don't name variables x2,x3,... (temp starts at 2)
LABEL = '_' #so if x is a variable, then don't name variables x_1,x_2, 
TC = 1  # for generating temporary functions to yield xt1,xt2,...
LC = 0  # for generating smallest macro constants in a loop _N1, _N2,... as well as
               # natural number variables _n1,_n2,...
"""
 Expressions: (f e1 ... ek) is represented as [f,e1,...,ek].
 Example: a+1 is ['+', ['a'],['1']]; constant a is ['a']; 
 sum(i+1,j) is ['sum', ['+', ['i'], ['1']], ['j']]
"""


#constructor: functor - a string like '+', '*', 'and', 
# or constants like '1', 'x'; args - a list of exprs
def expres(functor,args=[]):
    return [functor]+args

#accessor
def expr_op(e):
    return e[0]
def expr_args(e):
    return e[1:]

#prefix printing
def expr2string(e):
    if len(e)==1:
        return e[0]
    else:
        return '(' + e[0] +' '+ ' '.join(list(expr2string(x) for x in e[1:]))+ ')'

#normal infix printing
def expr2string1(e):
    args=expr_args(e)
    op=expr_op(e)
    if len(args)==0:
        return op
    else:
        if op=='and' or op=='or':
            if len(args)==1:
                return expr2string1(args[0])
            else:
                return '('+(' '+op+' ').join(list(expr2string1(x) for x in args))+')'
        elif op=='not' and len(args)==1:
            return 'not '+expr2string1(args[0])
        elif op=='implies' and len(args)==2:
            return expr2string1(args[0])+ ' -> '+expr2string1(args[1])
        elif op in _infix_op and len(args)==2:
            return '(' + expr2string1(args[0])+ op+expr2string1(args[1])+')'
        else:
            return op +'('+ ','.join(list(expr2string1(x) for x in args))+ ')'


#strip '(' at the beginning and matching ')' in the end of a string
def trim_p(s):
    if s.startswith('(') and s.endswith(')'):
        return trim_p(s[1:-1])
    else:
        return s


#normal infix printing
def expr2stringSimplify(e):
    args=expr_args(e)
    op=expr_op(e)
    if len(args)==0:
        return op
    else:
        if op=='and' or op=='or':
            if len(args)==1:
                return expr2stringSimplify(args[0])
            else:
                return '('+(' '+op+' ').join(list(expr2stringSimplify(x) for x in args))+')'
        elif op=='not' and len(args)==1:
            return 'not '+expr2stringSimplify(args[0])
        elif op=='implies' and len(args)==2:
            return expr2stringSimplify(args[0])+ ' -> '+expr2stringSimplify(args[1])
        elif op in _infix_op and len(args)==2:
            return '(' + expr2stringSimplify(args[0])+ op+expr2stringSimplify(args[1])+')'
        else:
            if op is 'ite':
            	expresion1 = expr2stringSimplify(args[1])
            	expresion2 =  expr2stringSimplify(args[2])
            	if ('and' not in expresion1 and 'or' not in expresion1 and 'ite' not in expresion1) and ('and' not in expresion2 and 'or' not in expresion2 and 'ite' not in expresion2) and simplify(expresion1+'=='+expresion2)==True:
            		
            		return expresion1
		else:
			return op +'('+ ','.join(list(expr2stringSimplify(x) for x in args))+ ')'
            else:
            	return op +'('+ ','.join(list(expr2stringSimplify(x) for x in args))+ ')'


"""
 Formulas:
 1. equations f(x) = e: ['e',e1,e2], 
    where e1 is expression for f(x) and e2 for e
 2. inductive definition:
 - base case f(x1,...,xk,0,...,xm)=e: ['i0',k,e1,e2] 
   where e1 is Expr for f(x1,...,xk,0,...,xm) and e2 the Expr for e
 - inductive case f(x1,...,xk,n+1,...,xm)=e: ['i1',k,'n',e1,e2] 
    where e1 is Expr for f(x1,...,xk,n+1,...,xm) and e2 the Expr for e
 3. inductive definition for functions that return natural numbers 
    (like N in smallest macro):
 - base case f(x) = 0 iff C: ['d0',e,c] 
   where e is the Expr for f(x) and c an expression for condition C
 - inductive case f(x) = n+1 iff C(n): ['d1','n',e,c] 
   where e is the Expr for f(x) and c an Expr for condition C
 4. any other axioms: A: ['a',e], where e is the Expr for A
 5. constraints from smallest macro smallest(N,n,e):
    ['s0', e(N)] 
    ['s1', forall n<N -> not e]

 Examples: a' = a+1: ['e', ['a\''], ['+',['a'],['1']]]
 N(x) = 0 if x<I else N(x-1)+1 is divided into two axioms:
 N(x) = 0 iff x<I:  
 ['d0', ['N',['x']], ['<', ['x'],['I']]] and
 N(x) = n+1 iff n=N(x-1): 
 ['d1','n', ['N',['x']], ['=',['n'], ['N', ['-', ['x'],['1']]]]]
"""


# constructors
def wff_e(e1,e2): #e1,e2: expr
    return ['e',e1,e2]

def wff_i0(k,e1,e2): #k: int; e1,e2: expr
    return ['i0',k,e1,e2]

def wff_i1(k,v,e1,e2): #k: int; v: string; e1,e2: expr
    return ['i1',k,v,e1,e2]

def wff_d0(e,c): #e: expr; c: expr
    return ['d0',e,c]

def wff_d1(v,e,c): #v: string, e and c: expr
    return ['d1',v,e,c]

def wff_a(e): #e: expr
    return ['a',e]

def wff_s0(e):
    return ['s0',e]
def wff_s1(e):
    return ['s1',e]
    
    
#print in prefix notation
def wff2string(w):
        if w[0] == 'e' or w[0] == 'i0' or w[0] == 'i1' or w[0] == 'i2' or w[0] == 'R':
            return '(= '+expr2string(w[-2])+' '+expr2string(w[-1]) +')'
        elif w[0] == 'd0':
            return '(iff (= '+expr2string(w[1])+' 0) '+ expr2string(w[2])+')'
        elif w[0] == 'd1':
            return '(iff (= '+expr2string(w[2])+' (+ '+w[1]+' 1)) '+expr2string(w[3])+')'
        elif w[0]=='a' or w[0]=='s0' or w[0]=='s1' or w[0]=='c1' or w[0] == 'R':
            return expr2string(w[1])

#print in normal infix notation
def wff2string1(w):
        if w[0] == 'e' or w[0] == 'i0' or w[0] == 'i1' or w[0] == 'i2' or w[0] == 'R':
            return expr2string1(w[-2])+' = '+ expr2string1(w[-1])
        elif w[0] == 'd0':
            return expr2string1(w[1])+'=0 <=> '+ expr2string1(w[2])
        elif w[0] == 'd1':
            return expr2string1(w[2])+'='+w[1]+'+1 <=> '+expr2string1(w[3])
        elif w[0]=='a' or w[0]=='s0' or w[0]=='s1' or w[0]=='c1':
            return expr2string1(w[1])


#Collect all Function and Variable defination for Translation 2

def getEqVariFunDetails(list,var_map):
	for x in list:
            wff2stringvfacteq(x,var_map)
            




#print in normal infix notation
def wff2stringvfacteq(w,var_map):
        if w[0] == 'e' or w[0] == 'i0' or w[0] == 'i1' or w[0] == 'R':
            expr2stringvfacteq(w[-2],var_map)
            expr2stringvfacteq(w[-1],var_map)
        elif w[0] == 'd0':
            expr2stringvfacteq(w[1],var_map)
            expr2stringvfacteq(w[2],var_map)
        elif w[0] == 'd1':
            expr2stringvfacteq(w[2],var_map)
            expr2stringvfacteq(w[3],var_map)
        elif w[0]=='a' or w[0]=='s0' or w[0]=='s1' or w[0]=='c1' :
            expr2stringvfacteq(w[1],var_map)




#Get all fact from equations
def expr2stringvfacteq(e,var_map):
    args=expr_args(e)
    op=expr_op(e)
    if len(args)==0:
    	if op not in var_map.keys() and fun_utiles.is_number(op)==False and fun_utiles.is_hex(op)==None and op not in _base:
    		element=[]
    		element.append(op)
        	element.append(0)
        	element_para=[]
        	element.append(element_para)
                element_para.append('int')
                #print '----------'
                #print op
                #print element
                #print '----------'
        	var_map[op]=element
    else:
        if op=='and' or op=='or':
            if len(args)==1:
                expr2stringvfacteq(args[0],var_map)
            else:
                for x in args:
                    expr2stringvfacteq(x,var_map)
        elif op=='not' and len(args)==1:
            expr2stringvfacteq(args[0],var_map)
        elif op=='implies' and len(args)==2:
            expr2stringvfacteq(args[0],var_map)
            expr2stringvfacteq(args[1],var_map)
        elif op in _infix_op and len(args)==2:
            expr2stringvfacteq(args[0],var_map)
            expr2stringvfacteq(args[1],var_map)
        else:
            if fun_utiles.isArrayFunction(op)==True:
            	count=0
            	element=[]
            	element.append(op)
            	element.append(len(args))
            	element_para=[]
            	array_type=None
            	for parameter in args:
            		if count==0:
            			element_para.append('array')
            			element_in=[]
                                expr2stringvfacteq(parameter,var_map)
            			para_value=expr2string1(parameter,var_map)
            			element_in.append(para_value)
            			element_in.append(0)
            			element_para_in=[]
            			element_para_in.append('array')
            			element_in.append(element_para_in)
            			var_map[para_value]=element_in
            			array_type='int'
            		else:
            			expr2stringvfacteq(parameter,var_map,allvariablelist,constraints)
            			typename='int'
                                element_para.append(typename)            					
 			count=count+1
                        
                element_para.append(array_type)
                
            	element.append(element_para)
                
            	var_map[op]=element
                
            else:
            	if op not in var_map.keys() and op is not 'ite' and op not in _base:
            		element=[]
            		element.append(op)
            		element.append(len(args))
            		element_para=[]
            		if len(args)>0:
            			for x in args:
                                        expr2stringvfacteq(x,var_map)
                                        element_para.append('int')
            		       	element_para.append('int')
            		else:
            			element_para.append('int')
                                
            		element.append(element_para)
            		var_map[op]=element
                        
            for x in args:
                expr2stringvfacteq(x,var_map)






#convert wff to z3 constraint
def wff2z3_update(w):
        if w[0] == 'e' or w[0] == 'i0' or w[0] == 'i1':
            var_cstr_map={}
            flag_constr=False
            lhs=expr2z3_update(w[-2],var_cstr_map)
            rhs=expr2z3_update(w[-1],var_cstr_map) 
            list_var_str=qualifier_list(var_cstr_map.keys())
            if fun_utiles.isArrayFunction(w[-2][0])==True:
            	if '_x1' in var_cstr_map.keys():
            		del var_cstr_map['_x1']
            	flag_constr=True
            if '_s1' in var_cstr_map.keys():
                del var_cstr_map['_s1']
            	flag_constr=True
            list_cstr_str=cstr_list(var_cstr_map.values())
            if 'Or' not in lhs and 'And' not in lhs and 'If' not in lhs and '/' not in lhs:
            	lhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(lhs))
            if 'Or' not in rhs and 'And' not in rhs and 'If' not in rhs and '/' not in rhs:
            	rhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(rhs))
            if w[-1][0] in ['==','<=','>=','>','<','!=','or','and']:
                rhs='If(('+rhs+')==0,0,1)'
            if list_var_str is not None and list_cstr_str is not None:
            	if w[0] == 'i1':
                	return "ForAll(["+list_var_str+"],Implies("+list_cstr_str+","+lhs+' == '+ rhs+"))"
                else:
                	if flag_constr==True:
                		return "ForAll(["+list_var_str+"],Implies("+list_cstr_str+","+lhs+' == '+ rhs+"))"
                	else:
                		return 'ForAll(['+list_var_str+'],'+lhs+' == '+ rhs+")"
            else:
                return lhs+' == '+ rhs
        elif w[0] == 'd0': # Bi-implications are represented using equality == in z3py
            var_cstr_map={}
	    lhs=expr2z3_update(w[1],var_cstr_map)
            rhs=expr2z3_update(w[2],var_cstr_map)
            list_var_str=qualifier_list(var_cstr_map.keys())
            list_cstr_str=cstr_list(var_cstr_map.values())
            if 'Or' not in lhs and 'And' not in lhs and 'If' not in lhs and '/' not in lhs:
	    	lhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(lhs))
	    if 'Or' not in rhs and 'And' not in rhs and 'If' not in rhs and '/' not in rhs:
            	rhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(rhs))
            if list_var_str is not None and list_cstr_str is not None:
                return 'ForAll(['+list_var_str+'],'+lhs+'=0 == '+ rhs+")"
            else:
                return lhs+'=0 == '+ rhs
        elif w[0] == 'd1': # Bi-implications are represented using equality == in z3py
            var_cstr_map={}
	    lhs=expr2z3_update(w[2],var_cstr_map)
            rhs=expr2z3_update(w[3],var_cstr_map)
            list_var_str=qualifier_list(var_cstr_map.keys())
            list_cstr_str=cstr_list(var_cstr_map.values())
            lhs=w[1]+'+1'
            if 'Or' not in lhs and 'And' not in lhs and 'If' not in lhs and '/' not in lhs:
	    	lhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(lhs))
	    if 'Or' not in rhs and 'And' not in rhs and 'If' not in rhs and '/' not in rhs:
            	rhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(rhs))
            if list_var_str is not None and list_cstr_str is not None:
                return "ForAll(["+list_var_str+"],"+lhs+' == '+rhs+")"
            else:
                return lhs+' == '+rhs
        elif w[0]=='a' or w[0]=='s0':
            var_cstr_map={}
	    expression=expr2z3_update(w[1],var_cstr_map)
            list_var_str=qualifier_list(var_cstr_map.keys())
            list_cstr_str=cstr_list(var_cstr_map.values())
            if 'Or' not in expression and 'And' not in expression and 'If' not in expression and '/' not in expression:
	    	expression=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression))
            if list_var_str is not None and list_cstr_str is not None:
                if 'Implies' in expression:
                    arg_list=fun_utiles.extract_args(expression)
                    constr=simplify(arg_list[0])
                    axms=str(constr).split('<')
                    axms[0]=axms[0].strip()
                    axms[1]=axms[1].strip()
                    arg_list[1]='Or('+axms[1]+'==0,'+arg_list[1].replace(axms[0],'('+axms[1]+'-1)')+')'
                    if list_var_str is not None and list_cstr_str is not None:
                        return 'ForAll(['+str(list_var_str)+'],Implies('+str(list_cstr_str)+','+arg_list[1]+'))'
                    else:
                        return arg_list[1]
                else:
                    return 'ForAll(['+list_var_str+'],Implies('+list_cstr_str+','+expression+'))'
                    
            else:
                return expression
        elif w[0]=='s1':
            var_cstr_map={}
            equations=[]
	    expression=expr2z3_update(w[1],var_cstr_map)
	    list_var_str=qualifier_list(var_cstr_map.keys())
            list_cstr_str=cstr_list(var_cstr_map.values())
            if 'Or' not in expression and 'And' not in expression and 'If' not in expression and '/' not in expression:
	    	expression=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression))
            if list_var_str is not None and list_cstr_str is not None:
                if 'Implies' in expression:
                    arg_list=fun_utiles.extract_args(expression)
                    constr=simplify(arg_list[0])
                    axms=str(constr).split('<')
                    axms[0]=axms[0].strip()
                    axms[1]=axms[1].strip()
                    var_cstr_map_mod={}
                    for x in var_cstr_map.keys():
                        if x!=axms[0]:
                            var_cstr_map_mod[x]=var_cstr_map[x]
                    list_var_str_new=qualifier_list(var_cstr_map_mod.keys())
                    list_cstr_str_new=cstr_list(var_cstr_map_mod.values())

                    new_w = copy.deepcopy(w)
                    for element in var_cstr_map.keys():
                    	fun=[]
                    	fun.append('_f')
                    	parameter=[]
                    	parameter.append(element)
                    	fun.append(parameter)
                    	sub=[]
                    	sub.append(element)
                    	new_w[1]=fun_utiles.expr_replace(new_w[1],sub,fun) #expr_replace_const(new_w[1],element,fun)
		    new_expression=expr2z3_update(new_w[1],var_cstr_map)
		    new_arg_list=fun_utiles.extract_args(new_expression)
                    
                    #old_arg_list=arg_list[1]
                    old_arg_list=new_arg_list[1]
                    arg_list[1]='Or('+axms[1]+'==0,'+fun_utiles.simplify_expand_sympy(arg_list[1].replace(axms[0],'('+axms[1]+'-1)'))+')'
                    if list_var_str_new is not None and list_cstr_str_new is not None:
                        return 'ForAll(['+str(list_var_str)+'],Implies(And('+arg_list[0]+','+str(list_cstr_str)+'),'+old_arg_list+'))'
                    else:
                    	return 'ForAll(['+str(list_var_str)+'],Implies(And('+arg_list[0]+','+str(list_cstr_str)+'),'+old_arg_list+'))'
                else:
                    return 'ForAll(['+list_var_str+'],Implies('+list_cstr_str+','+expression+'))'

        elif w[0]=='c1':
         	var_cstr_map={}
	      	equations=[]
	    	expression=expr2z3_update(w[1],var_cstr_map)
	    	list_var_str=qualifier_list(var_cstr_map.keys())
	    	list_cstr_str=cstr_list(var_cstr_map.values())
	    	if list_var_str is not None and list_cstr_str is not None:
        		 return 'ForAll(['+list_var_str+'],Implies('+list_cstr_str+','+expression+'))'
        	else:
        		 return expression
        elif w[0]=='L1':
        	var_cstr_map={}
        	flag_constr=False
            	lhs=expr2z3_update(w[-2],var_cstr_map)
            	rhs=expr2z3_update(w[-1],var_cstr_map)           
            	list_var_str=qualifier_list(var_cstr_map.keys())
            	if isArrayFunction(w[-2][0])==True:
            		if '_x1' in var_cstr_map.keys():
            			del var_cstr_map['_x1']
            		flag_constr=True
                if '_s1' in var_cstr_map.keys():
                    del var_cstr_map['_s1']
                    flag_constr=True
            	list_cstr_str=cstr_list(var_cstr_map.values())
            	list_cstr_str2=cstr_list(var_cstr_map.values())
            	if list_cstr_str is not None:
            		constant=w[2].replace('n','L')
            		list_cstr_str='And(And('+list_cstr_str+','+w[2]+'<'+constant+'),'+constant+'>0'+')'
            		list_cstr_str2='And(And('+list_cstr_str2+','+w[2]+'<'+constant+'+1),'+constant+'>0'+')'
            	if 'Or' not in lhs and 'And' not in lhs and 'If' not in lhs and '/' not in lhs:
            		lhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(lhs))
            	if 'Or' not in rhs and 'And' not in rhs and 'If' not in rhs and '/' not in rhs:
            		rhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(rhs))
            	if list_var_str is not None and list_cstr_str is not None:
            		if w[0] == 'i1':
                		return "Implies("+"ForAll(["+list_var_str+"],Implies("+list_cstr_str+","+lhs+' == '+ rhs+"))"+","+"ForAll(["+list_var_str+"],Implies("+list_cstr_str2+","+lhs+' == '+ rhs+"))"+")"
                	else:
                		if flag_constr==True:
                			return "Implies("+"ForAll(["+list_var_str+"],Implies("+list_cstr_str+","+lhs+' == '+ rhs+"))"+","+"ForAll(["+list_var_str+"],Implies("+list_cstr_str2+","+lhs+' == '+ rhs+"))"+")"
                		else:
                			return "Implies("+'ForAll(['+list_var_str+'],'+lhs+' == '+ rhs+")"+","+'ForAll(['+list_var_str+'],'+lhs+' == '+ rhs+")"+")"
            	else:
                	return "Implies("+lhs+' == '+ rhs+","+lhs+' == '+ rhs+")"
        elif w[0]=='L2':
        	var_cstr_map={}
        	flag_constr=False
            	lhs=expr2z3_update(w[2],var_cstr_map)
            	rhs=expr2z3_update(w[3],var_cstr_map)           
            	list_var_str=qualifier_list(var_cstr_map.keys())

            	list_cstr_str=cstr_list(var_cstr_map.values())
            	list_cstr_str2=cstr_list(var_cstr_map.values())

            	if list_cstr_str is not None:
            		constant=w[1].replace('n','L')
            		list_cstr_str='And(And('+list_cstr_str+','+w[1]+'<'+constant+'),'+constant+'>0'+')'
            		list_cstr_str2='And(And('+list_cstr_str+','+w[1]+'<'+constant+'+1),'+constant+'>0'+')'
            	if 'Or' not in lhs and 'And' not in lhs and 'If' not in lhs and '/' not in lhs:
            		lhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(lhs))
            	if 'Or' not in rhs and 'And' not in rhs and 'If' not in rhs and '/' not in rhs:
            		rhs=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(rhs))
            	if list_var_str is not None and list_cstr_str is not None:
            		return "Implies("+"ForAll(["+list_var_str+"],Implies("+list_cstr_str+","+lhs+"))"+","+"ForAll(["+list_var_str+"],Implies("+list_cstr_str2+","+rhs+"))"+")"
            	else:
                	return "Implies("+lhs+","+rhs+")"
        elif w[0] == 'R':
            var_cstr_map={}
            lhs=expr2z3_update(w[2],var_cstr_map)
            rhs=expr2z3_update(w[3],var_cstr_map)
            list_var_str=qualifier_list(w[1])
            if list_var_str is not None:
                return 'ForAll(['+list_var_str+'],'+lhs+' == '+ rhs+")"
            else:
                return lhs+' == '+ rhs
        elif w[0] == 'RE':
            var_cstr_map={}
            if len(w[2])==0:
                lhs=None
            else:
                lhs=expr2z3_update(w[2],var_cstr_map)
            rhs=expr2z3_update(w[3],var_cstr_map)
            if len(w[1])==0:
                list_var_str=None
            else:
                list_var_str=qualifier_list(w[1])
            if list_var_str is not None:
                if lhs!='' and lhs is not None:
                    return 'ForAll(['+list_var_str+'],Implies('+lhs+','+rhs+"))"
                else:
                    return 'ForAll(['+list_var_str+'],'+rhs+")"
            elif lhs!='' and lhs is not None:
                return 'Implies('+lhs+','+rhs+")"
            else:
                return rhs
        else:
            return expression



def expr2z3_update(e,var_cstr_map):
    args=expr_args(e)
    op=expr_op(e)
    if len(args)==0:
        if fun_utiles.isvariable(op)==True:
    		var_cstr_map[op]=op+">=0"
        return op
    else:
        if op=='and' or op=='or':
            if len(args)==1:
            	expression=expr2z3_update(args[0],var_cstr_map)
            	if '/' not in expression and 'Or' not in expression and '==' not in expression and 'And' not in expression and 'If' not in expression and 'Implies' not in expression:
            		expression=fun_utiles.simplify_expand_sympy(expression)
                return expression
            else:
                e_array=[]
                for x in args:
                	parameter1=expr2z3_update(x,var_cstr_map)
                    	if '/' not in parameter1 and 'Or' not in parameter1 and '==' not in parameter1 and 'And' not in parameter1 and 'If' not in parameter1 and 'Implies' not in parameter1:                    		
                    		parameter1=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(parameter1))
                                
                    	elif 'Or' not in parameter1 and 'And' not in parameter1 and 'If' not in parameter1 and 'Implies' not in parameter1:
                    		parameter1=fun_utiles.convert_pow_op_fun(parameter1)
                    	e_array.append(parameter1)
                if op=='or':
                	#return 'Or('+parameter1+','+parameter2+')'
                	return fun_utiles.constructAndOr(e_array,'Or')
                else:
                	if op=='and':
                		#return 'And('+parameter1+','+parameter2+')'
                		return fun_utiles.constructAndOr(e_array,'And')
        elif op=='not' and len(args)==1:
            expression=expr2z3_update(args[0],var_cstr_map)
            if '/' not in expression and 'Or' not in expression and '==' not in expression and 'And' not in expression and 'If' not in expression and 'Implies' not in expression:
            	expression=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression))
            elif 'Or' not in expression and 'And' not in expression and 'If' not in expression and 'Implies' not in expression:
            	expression=fun_utiles.convert_pow_op_fun(expression)
            return 'Not('+expression+')'
        elif op=='implies' and len(args)==2:
            if len(var_cstr_map)==0:
            	expression1=expr2z3_update(args[0],var_cstr_map)
            	expression2=expr2z3_update(args[1],var_cstr_map)
            	if '/' not in expression1 and 'Or' not in expression1 and '==' not in expression1 and 'And' not in expression1 and 'If' not in expression1 and 'Implies' not in expression1:
            		expression1=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression1))
            	elif 'Or' not in expression1 and 'And' not in expression1 and 'If' not in expression1 and 'Implies' not in expression1:
			expression1=fun_utiles.convert_pow_op_fun(expression1)
            	if '/' not in expression2 and 'Or' not in expression2 and '==' not in expression2 and 'And' not in expression2 and 'If' not in expression2 and 'Implies' not in expression2:
            		expression2=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression2))
            	elif 'Or' not in expression2 and 'And' not in expression2 and 'If' not in expression2 and 'Implies' not in expression2:
			expression2=fun_utiles.convert_pow_op_fun(expression2)
            	return 'Implies('+expression1+ ','+expression2+')'
            else:
            	list_constrn=""
                for x in var_cstr_map:
            		if list_constrn=="":
            			expression1=expr2z3_update(args[0],var_cstr_map)
            			if '/' not in expression1 and 'Or' not in expression1 and '==' not in expression1 and 'And' not in expression1 and 'If' not in expression1 and 'Implies' not in expression1:
            				expression1=fun_utiles.convert_pow_op_fun(fun_utiles.simplify_expand_sympy(expression1))
            			elif 'Or' not in expression1 and 'And' not in expression1 and 'If' not in expression1 and 'Implies' not in expression1:
					expression1=fun_utiles.convert_pow_op_fun(expression1)
            			list_constrn="And("+expression1+","+var_cstr_map[x]+")"
            		else:
            			list_constrn="And("+list_constrn+","+var_cstr_map[x]+")"
            	expression2=expr2z3_update(args[1],var_cstr_map)
            	if '/' not in expression2 and 'Or' not in expression2 and '==' not in expression2 and 'And' not in expression2 and 'If' not in expression2 and 'Implies' not in expression2:
            		expression1=fun_utiles.simplify_expand_sympy(expression2)
            	elif 'Or' not in expression2 and 'And' not in expression2 and 'If' not in expression2 and 'Implies' not in expression2:
			expression2=fun_utiles.convert_pow_op_fun(expression2)
            	return 'Implies('+list_constrn+ ','+expression2+')'
        elif op in _infix_op and len(args)==2:
        	expression1=expr2z3_update(args[0],var_cstr_map)
        	expression2=expr2z3_update(args[1],var_cstr_map)
        	if '/' not in expression1 and 'Or' not in expression1 and '==' not in expression1 and 'And' not in expression1 and 'If' not in expression1 and 'Implies' not in expression1:
        		expression1=fun_utiles.simplify_expand_sympy(expression1)
        	if '/' not in expression2 and 'Or' not in expression2 and '==' not in expression2 and 'And' not in expression2 and 'If' not in expression2 and 'Implies' not in expression2:
        		expression2=fun_utiles.simplify_expand_sympy(expression2)
        	if op=='/':
        		return '((' + expression1+')'+op+'('+expression2+'))'
                elif op=='**':
                        if expression2=='2':
                            return expression1+'*'+expression1
                        else:
                            return 'power((' + expression1+')'+','+'('+expression2+'))'
        	elif op=='=':
                    
        		return '((' + expression1+ ')==('+expression2+'))'
        	else:
        		if op=='*':
                            expression='((' + expression1+')'+ op+'('+expression2+'))'
                        else:
                            expression='((' + expression1+')'+ op+'('+expression2+'))'
        		if '/' not in expression and 'Or' not in expression and '==' not in expression and 'And' not in expression and '.' not in expression:
        			return fun_utiles.simplify_expand_sympy(expression)
        		else:
        			return expression
        else:
            if op=='ite':
            	return 'If('+ ','.join(list(fun_utiles.conditionSimplifyPower(expr2z3_update(x,var_cstr_map)) for x in args))+ ')'
            else:
            	if fun_utiles.isArrayFunction(op)==True:
            		parameter_list=[]
            		defineDetailtemp=[]
            		defineDetailtemp.append(op)
            		parameter_list.append('array')
            		for x in range(0, len(args)):
            			parameter_list.append('int')
            		defineDetailtemp.append(len(args))
            		defineDetailtemp.append(parameter_list)
            		defineDetaillist.append(defineDetailtemp)
            	return op +'('+ ','.join(list(expr2z3_update(x,var_cstr_map) for x in args))+ ')'



#print in normal infix notation
def wff2subslist(w):
        if w[0] == 'e':
            return expr2string1(w[-2]),expr2string1(w[-1])
 


#construct constraints for qualified variables
        
def qualifier_list(list_var):
    if len(list_var)==0:
        return None;
    else:
        var=list_var[-1]
        del list_var[-1]
        list_var_str=qualifier_list(list_var)
        if list_var_str is None:
            return var
        else:
            return var+","+list_var_str

#construct map of all array functions

def array_element_list(e,array_map): #e,e1,e2: expr
	if isArrayFunction(e[:1][0])==True:
            array_map[e[:1][0]]=e[:1][0]
            for x in expr_args(e):
                array_element_list(x,array_map)
        else:
            for x in expr_args(e):
                array_element_list(x,array_map)

#construct constraints for qualified variables

def cstr_list(list_cstr):
    if len(list_cstr)==0:
        return None;
    else:
        var=list_cstr[-1]
        del list_cstr[-1]
        list_cstr_str=cstr_list(list_cstr)
        if list_cstr_str is None:
            return var
        else:
            return "And("+var+","+list_cstr_str+")"
        
        
        
#construct constraints for qualified variables

def cstr_list_additional(list_cstr_str,list_cstr,const_var_map):
    if len(list_cstr)==0:
        return list_cstr_str;
    else:
        var=list_cstr[-1]
        del list_cstr[-1]
        if list_cstr_str is None:
            list_cstr_str=cstr_list_additional(list_cstr_str,list_cstr,const_var_map)
        else:
            list_cstr_str = cstr_list_additional(list_cstr_str,list_cstr,const_var_map)
        if var in const_var_map.keys():
            if list_cstr_str is None:
                return var+"<"+const_var_map[var]
            else:
                return "And("+var+"<"+const_var_map[var]+","+list_cstr_str+")"
        else:
            return list_cstr_str;
