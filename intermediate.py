
import sys
import os

currentdirectory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(currentdirectory+"/packages/pyparsing/")
sys.path.append(currentdirectory+"/packages/pycparser1/")
sys.path.append(currentdirectory+"/packages/pycparserext/")
sys.path.append(currentdirectory+"/packages/regex/")
sys.path.append(currentdirectory+"/packages/mpmath/")
sys.path.append(currentdirectory+"/packages/sympy/")


import fun_utiles
import FOL_translation

from pyparsing import *
from sympy.core.relational import Relational
from pycparser1 import parse_file,c_parser, c_ast, c_generator
from pycparserext.ext_c_parser import GnuCParser
from pycparserext.ext_c_generator import GnuCGenerator


def createASTStmt(expression):
    parser = c_parser.CParser()
    ast = parser.parse("void test(){"+expression+";}")
    statement_temp=ast.ext[0].body.block_items[0]
    return statement_temp






def construct_expressionC(postion,variable,e1,e2):
	expression=[]
        expression.append('i2')
        expression.append(postion)
        expression.append(variable)
        expression.append(e1)
        expression.append(e2)
	return expression

def construct_expression(tree,postion,variable):
	expression=""
	if type(tree) is m.Assignment:
		expression="['i2',"+str(postion)+",'"+variable+"',"+expressionCreator(tree.lhs)+","+expressionCreator(tree.rhs)+"]"
	return eval(expression)



def construct_expression_normalC(e):
	if e is not None:
		expression=[]
                expression.append('s0')
                expression.append(e)
		return expression
	else:
		return None



def construct_expression_normal(tree):
	if tree is not None:
		expression=""
		if type(tree) is m.Relational:
			expression="['s0',"+expressionCreator(tree)+"]"
		return eval(expression)
	else:
		return None




"""

Program Expression to a Array of Statement Compatible to Translator Program 

"""

fun_call_map={}
current_fun_call=None


def expressionCreator_C(statement):
    expression=""
    global defineMap
    global defineDetaillist
    global fun_call_map
    global current_fun_call
    if type(statement) is c_ast.ID:
    	if statement.name in defineMap.keys():
    		value = defineMap[statement.name]
    		return str(eval("FOL_translation.expres('"+value+"')"))
        else:
        	return str(eval("FOL_translation.expres('"+statement.name+"')"))
    elif type(statement) is c_ast.Constant:
    	if statement.type=='char':
                if str(statement.value)==str("'\\0'"):
                    return str(eval("FOL_translation.expres('0')"))
                else:
                    return "['char',FOL_translation.expres("+statement.value+")]"
    	elif statement.type=='float':
    		if statement.value[-1]=='f':
    			#return "FOL_translation.expres('"+str(round(float(statement.value[:-1]), 7))+"')"
                        return str(eval("FOL_translation.expres('"+str(statement.value[:-1])+"')"))
	        #return "FOL_translation.expres('"+str(float(statement.value))+"')"
                return str(eval("FOL_translation.expres('"+str(statement.value)+"')"))
	elif statement.type=='double':
                #return "FOL_translation.expres('"+str(float(statement.value))+"')"
                return str(eval("FOL_translation.expres('"+str(statement.value)+"')"))
    	else:
        	if fun_utiles.is_hex(statement.value) is not None:
        		return str(eval("FOL_translation.expres('"+fun_utiles.is_hex(statement.value)+"')"))
        	else:
        		return str(eval("FOL_translation.expres('"+statement.value+"')"))
    elif type(statement) is c_ast.FuncCall:
    	parameter=''
    	parameter_list=[]
    	defineDetaillist=[]
    	defineDetailtemp=[]
    	parameter_list.append('int')
	if statement.args is not None:
    		for param in statement.args.exprs:
    			if type(param) is c_ast.ID:
    				parameter_list.append('int')
    				if param.name in defineMap.keys():
    					param.name = defineMap[param.name]
    				if parameter=='':
		        		parameter = str(eval("FOL_translation.expres('"+param.name+"')"))
		        	else:
		        		parameter += ","+str(eval("FOL_translation.expres('"+param.name+"')"))
    			elif type(param) is c_ast.Constant:
    				parameter_list.append('int')
    		    		if parameter=='':
					if fun_utiles.is_hex(param.value) is not None:
						parameter = str(eval("FOL_translation.expres('"+fun_utiles.is_hex(param.value)+"')"))
					else:
						parameter = str(eval("FOL_translation.expres('"+param.value+"')"))
				else:
		        		if fun_utiles.is_hex(param.value) is not None:
		        			parameter += ","+str(eval("FOL_translation.expres('"+fun_utiles.is_hex(param.value)+"')"))
		        		else:
		        			parameter += ","+str(eval("FOL_translation.expres('"+param.value+"')"))
		        elif type(param) is c_ast.UnaryOp:
				if parameter=='':
                                    
			        	parameter = str(eval("FOL_translation.expres('"+param.op+"',["+expressionCreator_C(param.expr)+"])"))
			        else:
                                	parameter +=','+str(eval("FOL_translation.expres('"+param.op+"',["+expressionCreator_C(param.expr)+"])"))
		        
		        elif type(param) is c_ast.BinaryOp:
				if parameter=='':
			        	parameter =expressionCreator_C(param)
			        else:
                                	parameter +=','+expressionCreator_C(param)
                        elif type(param) is c_ast.FuncCall:
				if parameter=='':
			        	parameter =expressionCreator_C(param)
			        else:
                                	parameter +=','+expressionCreator_C(param)
			else:
				if type(param) is c_ast.ArrayRef:
					parameter_list.append('int')
				    	degree=0
				       	stmt,degree=createArrayList_C(param,degree)
    					if parameter=='':
						parameter = str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
					else:
		        			parameter += ","+str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
				
				#print '@@@@@@@@@@@RamRam'
				#print param.show()
				#print '@@@@@@@@@@@'
		defineDetailtemp.append(statement.name.name)
		defineDetailtemp.append(len(parameter_list)-1)
		defineDetailtemp.append(parameter_list)
		defineDetaillist.append(defineDetailtemp)
                
                if statement.name.name in fun_call_map.keys() and statement.name.name != current_fun_call and '__VERIFIER_nondet_' not in statement.name.name:
                    fc_count=fun_call_map[statement.name.name]
                    fc_count+=1
                    fun_call_map[statement.name.name]=fc_count
                    return "['"+statement.name.name+"_"+str(fc_count)+"',"+parameter+"]"
                else:
                    fun_call_map[statement.name.name]=0
                    return "['"+statement.name.name+"',"+parameter+"]"
	else:
		if '__VERIFIER_nondet_' not in statement.name.name:
                    defineDetailtemp.append(statement.name.name)
                    defineDetailtemp.append(len(parameter_list)-1)
                    defineDetailtemp.append(parameter_list)
                    defineDetaillist.append(defineDetailtemp)
		if statement.name.name in fun_call_map.keys() and statement.name.name != current_fun_call and '__VERIFIER_nondet_' not in statement.name.name:
                    fc_count=fun_call_map[statement.name.name]
                    fc_count+=1
                    fun_call_map[statement.name.name]=fc_count
                    return str(eval("FOL_translation.expres('"+statement.name.name+"_"+str(fc_count)+"'"+")"))
                else:
                    fun_call_map[statement.name.name]=0
                    return str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))
                    
    elif type(statement) is c_ast.ArrayRef:
    	degree=0
       	stmt,degree=createArrayList_C(statement,degree)
    	return str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
    else:
        if type(statement) is c_ast.Cast:
            if statement.to_type.type.type.names[0]=='float':
                return "['"+"_ToReal"+"',"+expressionCreator_C(statement.expr)+"]"
            elif statement.to_type.type.type.names[0]=='double':
                return "['"+"_ToReal"+"',"+expressionCreator_C(statement.expr)+"]"
            elif statement.to_type.type.type.names[0]=='int':
                return "['"+"_ToInt"+"',"+expressionCreator_C(statement.expr)+"]"
        else:
            
            if statement.op in ['+','-','*','/','%']:
                expression="FOL_translation.expres('"
                expression+=statement.op
                if type(statement) is c_ast.BinaryOp:
                    expression+="',["+expressionCreator_C(statement.left)
                    expression+=','+expressionCreator_C(statement.right)
                else:
                    expression+="',["+expressionCreator_C(statement.expr)
                expression+='])'
                expression=str(eval(expression))
                return expression
            else:
                #if statement.op == '!=':
                #    statement=c_ast.UnaryOp(op='!', expr=c_ast.BinaryOp(op='==',left=statement.left, right=statement.right))

                expression="['"
                if statement.op == '&&':
                    expression+='and'
                elif statement.op == '||':
                    expression+='or'
                elif statement.op == '!':
                    expression+='not'
                else:
                    expression+=statement.op
                if type(statement) is c_ast.BinaryOp:
                    expression+="',"+expressionCreator_C(statement.left)

                    expression+=','+expressionCreator_C(statement.right)
                    expression+=']'
                else:
                    expression="FOL_translation.expres('"
                    if statement.op == '!':
                            expression+='not'
                    else:
                            expression+=statement.op
                    expression+="',["+expressionCreator_C(statement.expr)+"]"
                    expression+=')'
                    expression=str(eval(expression))
                return expression




"""

Construct Array List

"""
def createArrayList_C(statement,degree):
	if type(statement) is c_ast.ArrayRef:
		degree=degree+1
		stmt=''
		if type(statement.name) is c_ast.ArrayRef:
			stmt,degree=createArrayList_C(statement.name,degree)
			if type(statement.subscript) is c_ast.ID:
				stmt+=",FOL_translation.expres('"+statement.subscript.name+"')"
                        elif type(statement.subscript) is c_ast.BinaryOp:
                                stmt+=","+expressionCreator_C(statement.subscript)
			else:
				stmt+=",FOL_translation.expres('"+statement.subscript.value+"')"
			return stmt,degree
		else:
			if type(statement.name) is c_ast.ID:
				if type(statement.subscript) is c_ast.ID:
					stmt+="FOL_translation.expres('"+statement.name.name+"')"+",FOL_translation.expres('"+statement.subscript.name+"')"
					return stmt,degree
				elif type(statement.subscript) is c_ast.BinaryOp:
					stmt+="FOL_translation.expres('"+statement.name.name+"')"+","+expressionCreator_C(statement.subscript)
					return stmt,degree
				else:
                                        if type(statement.subscript) is c_ast.ArrayRef:
                                            temp_degree=0
                                            temp_stmt,temp_degree=createArrayList_C(statement.subscript,temp_degree)
                                            stmt+="FOL_translation.expres('"+statement.name.name+"')"+","+"FOL_translation.expres('d"+str(temp_degree)+'array'+"',["+temp_stmt+"])"
                                            return stmt,degree 
                                        else:
                                            stmt+="FOL_translation.expres('"+statement.name.name+"')"+",FOL_translation.expres('"+statement.subscript.value+"')"
                                            return stmt,degree
			else:
				if type(statement.name) is c_ast.FuncCall:
					if type(statement.subscript) is c_ast.FuncCall:
						stmt+=expressionCreator_C(statement.name)+","+expressionCreator_C(statement.subscript)
					elif type(statement.subscript) is c_ast.BinaryOp:
						stmt+=expressionCreator_C(statement.name)+","+expressionCreator_C(statement.subscript)
					else:
						stmt+=expressionCreator_C(statement.name)+",FOL_translation.expres('"+statement.subscript.value+"')"
				else:
					stmt+="FOL_translation.expres('"+statement.name.value+"')"+",FOL_translation.expres('"+statement.subscript.value+"')"
				return stmt,degree
	else:
		return "FOL_translation.expres('"+statement.name+"')",degree
