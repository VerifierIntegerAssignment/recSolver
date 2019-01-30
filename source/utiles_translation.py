
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

import list_class
import fun_utiles
import prog_transform
import FOL_translation
import regex
import copy
from pyparsing import *
from sympy.core.relational import Relational
from pycparser1 import parse_file,c_parser, c_ast, c_generator
from pycparserext.ext_c_parser import GnuCParser
from pycparserext.ext_c_generator import GnuCGenerator
ParserElement.enablePackrat()




defineMap={}
count_for__VERIFIER_nondet=0
count_for__insert_flag=0
count_for__function_flag=0
line_count_trace=0
new_program_trace_var={}
line_no_stmt_map={}
back_line_no_stmt_map={}
main_line_no_stmt_ast_map={}
count_ast_line_no=0








def translate2IntForm(function_name,function_type,function_body,parametermap,tempory,function_body_pa,struct_map):
    global current_fun_call
    if function_body is None: 
        print "Empty Body"
	return None
        
    start_time=fun_utiles.current_milli_time()
    
    statements=function_body.block_items
       
    localvarmap=prog_transform.getVariables(function_body)
    
    
    print 'Program Body'
    
    generator = c_generator.CGenerator()
    

    
    print(generator.visit(tempory))
    #print(generator.visit(function_body))
    
    
    
    membermethod=list_class.membermethodclass(function_name,function_type,parametermap,localvarmap,function_body,0,0,tempory,function_body_pa,None)


    input_value_extract={}

    if membermethod.getAnalysis_module() is not None:
    
        input_value_extract=constructProgAssertAnalysis2(copy.deepcopy(membermethod.getAnalysis_module()),localvarmap,membermethod.getInputvar(),membermethod.getMethodname())

    
        membermethod.setAnalysis_module(constructProgAssertAnalysis(membermethod.getAnalysis_module(),localvarmap,membermethod.getInputvar()))
    

    #print '!!!!!!!!!!!!!!!!!!'
    #print(generator.visit(membermethod.getAnalysis_module()))
    #print '!!!!!!!!!!!!!!!!!!'

    
    print "Function Name:"
    print membermethod.getMethodname()
    print "Return Type:"
    print membermethod.getreturnType()
    print "Input Variables:"
    var_list="{"
    for x in membermethod.getInputvar():

        if membermethod.getInputvar()[x].getDimensions() is not None and len(membermethod.getInputvar()[x].getDimensions())>0:
            if membermethod.getInputvar()[x].getStructType() is None:
                var_list+=' '+x+':array'
            else:
                var_list+=' '+x+':array'
                #var_list+=' '+x+':'+membermethod.getInputvar()[x].getStructType()
	else:
	    var_list+=' '+x+':'+membermethod.getInputvar()[x].getVariableType()
    var_list+='}'
    print var_list
    print "Local Variables:"
    var_list="{"
    for x in membermethod.getLocalvar():
        if membermethod.getLocalvar()[x].getDimensions() is not None and len(membermethod.getLocalvar()[x].getDimensions())>0:
            if membermethod.getLocalvar()[x].getStructType() is None:
                var_list+=' '+x+':array'
            else:
                var_list+=' '+x+':array'
                #var_list+=' '+x+':'+membermethod.getLocalvar()[x].getStructType()
	else:
            var_list+=' '+x+':'+membermethod.getLocalvar()[x].getVariableType()
    var_list+='}'
    print var_list
    allvariable={}
    program_dec_start=""
    program_dec_end=""
    for lvap in localvarmap:
        var=localvarmap[lvap]
        if var is not None and var.getInitialvalue() is not None:
            #print var.getInitialvalue()
            #print type(var.getInitialvalue())
            #type(var.getInitialvalue()).show()
            
	    #if type(var.getInitialvalue()) is not c_ast.BinaryOp and '__VERIFIER_nondet' in var.getInitialvalue():
	    #	defineDetailtemp=[]
	    #	parameter_list=[]
	    #	parameter_list.append('int')
	    #	defineDetailtemp.append(var.getInitialvalue())
	    #	defineDetailtemp.append(0)
	    #	defineDetailtemp.append(parameter_list)
	    # 	defineDetaillist.append(defineDetailtemp)
            if program_dec_start=="":
            	if type(var.getInitialvalue()) is c_ast.BinaryOp:
            	        program_dec_start="['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+expressionCreator_C(var.getInitialvalue())+"]"
                	program_dec_end="]"
            	else:
            		if fun_utiles.is_hex(str(var.getInitialvalue())) is not None:
                		program_dec_start="['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+"FOL_translation.expres('"+fun_utiles.is_hex(str(var.getInitialvalue()))+"')]"
                	else:
                		program_dec_start="['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+"FOL_translation.expres('"+str(var.getInitialvalue())+"')]"
                	program_dec_end="]"
            else:
            	if type(var.getInitialvalue()) is c_ast.BinaryOp:
            	        program_dec_start+=",['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+expressionCreator_C(var.getInitialvalue())+"]"
                	program_dec_end+="]"
            	else:
            		if fun_utiles.is_hex(str(var.getInitialvalue())) is not None:
                		program_dec_start+=",['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+"FOL_translation.expres('"+fun_utiles.is_hex(str(var.getInitialvalue()))+"')]"
                	else:
                		program_dec_start+=",['-1','seq',['-1','=',FOL_translation.expres('"+str(var.getVariablename())+"'),"+"FOL_translation.expres('"+str(var.getInitialvalue())+"')]"
                	program_dec_end+="]"

    
    for x in membermethod.getInputvar():
        allvariable[x]=membermethod.getInputvar()[x]
    for x in membermethod.getLocalvar():
        allvariable[x]=membermethod.getLocalvar()[x]
    

    current_fun_call = membermethod.getMethodname()
       
    expressions=organizeStatementToObject_C(statements)
    
    primeStatement(expressions)
    variablesarray={}
    opvariablesarray={}
    count=0
    arrayFlag=False
    
    struct_var_def_map={}
    
    
    for variable in allvariable:
        count+=1
        if allvariable[variable].getDimensions() is not None and len(allvariable[variable].getDimensions())>0:
            if allvariable[variable].getStructType() is None:
                variablesarray[variable]=eval("['_y"+str(count)+"','array']")
                opvariablesarray[variable+"1"]=eval("['_y"+str(count)+"','array']")
                list_parameter="'array'"
                for i in range(0, len(allvariable[variable].getDimensions())):
                    if list_parameter=='':
                        list_parameter="'int'"
                    else:
                        list_parameter+=",'int'"
                list_parameter+=",'"+allvariable[variable].getVariableType()+"'"
                #key1=str(allvariable[variable].getDimensions())+'array'
                key1='d'+str(len(allvariable[variable].getDimensions()))+'array'
                arrayFlag=True
                if key1 not in variablesarray.keys():
                    count+=1
                    variablesarray[key1]=eval("['_y"+str(count)+"',"+list_parameter+"]")
                    opvariablesarray[key1+"1"]=eval("['_y"+str(count)+"',"+list_parameter+"]")
            else:
                variablesarray[variable]=eval("['_y"+str(count)+"','array']")
                opvariablesarray[variable+"1"]=eval("['_y"+str(count)+"','array']")
                #variablesarray[variable]=eval("['_y"+str(count)+"','"+allvariable[variable].getStructType()+"']")
                #opvariablesarray[variable+"1"]=eval("['_y"+str(count)+"','"+allvariable[variable].getStructType()+"']")
                if allvariable[variable].getStructType() in struct_map.keys():
                    var_mem_list=struct_map[allvariable[variable].getStructType()]
                    print var_mem_list.getName()
                    for var_mem in var_mem_list.getVariablemap().keys():
                        member_var=var_mem_list.getVariablemap()[var_mem]
                        struct_key=allvariable[variable].getStructType()+"_"+member_var.getVariablename()
                        if struct_key not in struct_var_def_map.keys():
                            count+=1
                            struct_var_def_map[struct_key]=eval("['_y"+str(count)+"',"+"'"+allvariable[variable].getStructType()+"','"+member_var.getVariableType()+"'"+"]")

                    #for var_men in var_mem_list:
                    #    print var_men
                    #    var_member=var_mem_list[var_men]
                    #    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                    #    print var_member
                    #    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                
        else:
            variablesarray[variable]=eval("['_y"+str(count)+"','"+allvariable[variable].getVariableType()+"']")
            opvariablesarray[variable+"1"]=eval("['_y"+str(count)+"','"+allvariable[variable].getVariableType()+"']")


    for element in struct_var_def_map.keys():
         variablesarray[element]=struct_var_def_map[element]
         opvariablesarray[element+"1"]=struct_var_def_map[element]
            
    if program_dec_start=="":
        str_program=programToinductiveDefination_C(expressions , allvariable)
    else:
        str_program=program_dec_start+','+programToinductiveDefination_C(expressions , allvariable)+program_dec_end
    


    program=eval(str_program)
    return program,variablesarray,membermethod.getMethodname(),membermethod.getInputvar(),opvariablesarray,membermethod.getAnalysis_module(),input_value_extract




"""

Organization of AST 

"""
               
def organizeStatementToObject_C(statements):
	count=0
	degree=0
	expressions=[]
	for statement in statements:
                if type(statement) is c_ast.Assignment:
			count=count+1
			expression=list_class.expressionclass(statement, count, True,degree)
			expressions.append(expression)
                elif type(statement) is c_ast.While:
                    blockexpressions=[]
                    if statement.stmt is not None:
                        degree=degree+1
			count,blockexpressions=blockToExpressions_C(statement.stmt.block_items, degree, count)
			degree=degree-1
		    block=list_class.blockclass( blockexpressions, statement.cond, count , True, degree)
		    expressions.append(block)
		else:
			if type(statement) is c_ast.If:
				count,ifclass=ifclassCreator_C(statement, degree, count)
				expressions.append(ifclass)
			else:
				count=count+1
				expression=list_class.expressionclass(statement, count, True,degree)
				expressions.append(expression)
					
     	return expressions



"""

Organization of AST 

"""


               
def organize__VERIFIER_nondet_C(statements,count):
	expressions=[]
	for statement in statements:
                if type(statement) is c_ast.Assignment:
			expressions.append(expression)
                elif type(statement) is c_ast.While:
                    blockexpressions=[]
                    if statement.stmt is not None:
			count,blockexpressions=organize__VERIFIER_nondet_C(statement.stmt.block_items,count)
		    block=list_class.blockclass( blockexpressions, statement.cond, count , True, degree)
		    expressions.append(block)
		else:
			if type(statement) is c_ast.If:
				count,ifclass=ifclassCreator_C(statement, degree, count)
				expressions.append(ifclass)
			else:
				count=count+1
				expression=list_class.expressionclass(statement, count, True,degree)
				expressions.append(expression)
					
     	return expressions,count

"""

Conditionl Loop to a Array of Statement Compatible to Translator Program 
IfClass Creator

"""

def ifclassCreator_C(statement, degree, count):
        blockexpressions1=None
	blockexpressions2=None
	predicate=statement.cond
	#print statement.iftrue.show()
	#print statement.iffalse.show()
        if statement.iftrue is not None:
        	if type(statement.iftrue) is c_ast.Compound:
            		count,blockexpressions1=blockToExpressions_C(statement.iftrue.block_items, degree, count)
            	else:
            		new_block_items=[]
            		new_block_items.append(statement.iftrue)
            		count,blockexpressions1=blockToExpressions_C(new_block_items, degree, count)
        if statement.iffalse is not None and type(statement.iffalse) is c_ast.If:
        	count,blockexpressions2=ifclassCreator_C(statement.iffalse, degree, count)
        else:
        	if statement.iffalse is not None:
        		if type(statement.iffalse) is c_ast.Compound:
        			count,blockexpressions2=blockToExpressions_C(statement.iffalse.block_items, degree, count)
        		else:
        			new_block_items=[]
        			new_block_items.append(statement.iffalse)
            			count,blockexpressions2=blockToExpressions_C(new_block_items, degree, count)
	ifclass=list_class.Ifclass(predicate, blockexpressions1, blockexpressions2, count ,True ,degree)
	return count,ifclass



"""

Converting code block,while loop ,conditional expression and expression to corresponding Classes

"""

def blockToExpressions_C(body, degree, count):
	expressions=[]
	if body is not None:
		for statement in body:
                    if type(statement) is c_ast.Assignment:
			count=count+1
			expression=list_class.expressionclass(statement, count, True,degree)
			expressions.append(expression)
                    elif type(statement) is c_ast.While:
                        blockexpressions=[]
                        if statement.stmt is not None:
                            degree=degree+1
                            count,blockexpressions=blockToExpressions_C(statement.stmt.block_items, degree, count)
                            degree=degree-1
                        block=list_class.blockclass( blockexpressions, statement.cond, count , True, degree)
                        expressions.append(block)
                    else:
			if type(statement) is c_ast.If:
				count,ifclass=ifclassCreator_C(statement, degree, count)
				expressions.append(ifclass)
	return count,expressions




"""

Block of Statement to Array of Statement Compatible to Translator Program 

"""
def programToinductiveDefination_C(expressions, allvariable):
	programsstart=""
	programsend=""
	statements=""
	for expression in expressions:
		if type(expression) is list_class.expressionclass:
			if type(expression.getExpression()) is c_ast.Assignment:
                                var=None
                                if type(expression.getExpression().lvalue) is c_ast.ID:
                                    var=str(eval("FOL_translation.expres('"+str(expression.getExpression().lvalue.name)+"')"))
                                elif type(expression.getExpression().lvalue) is c_ast.Constant:
                                    var=str(eval("FOL_translation.expres('"+str(expression.getExpression().lvalue.value)+"')"))
                                elif type(expression.getExpression().lvalue) is c_ast.ArrayRef:
                                    degree=0
       				    stmt,degree=createArrayList_C(expression.getExpression().lvalue,degree)
                                    var=str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
                                    
                                    
                                elif type(expression.getExpression().lvalue) is c_ast.FuncCall:
                                	parameter=''
				        statement=expression.getExpression().lvalue
					if statement.args is not None:
						for param in statement.args.exprs:
							if type(param) is c_ast.ID:
								if parameter=='':
									parameter = str(eval("FOL_translation.expres('"+param.name+"')"))
								else:
									parameter += ","+str(eval("FOL_translation.expres('"+param.name+"')"))
							elif type(param) is c_ast.Constant:
								if parameter=='':
									parameter = str(eval("FOL_translation.expres('"+param.value+"')"))
								else:
									parameter += ","+str(eval("FOL_translation.expres('"+param.value+"')"))
							elif type(param) is c_ast.BinaryOp:
							    	if parameter=='':
									parameter =expressionCreator_C(param)
								else:
					        			parameter += ","+expressionCreator_C(param)
                                                        else:
                                                            if type(param) is c_ast.ArrayRef:
                                                            #parameter_list.append('int')
                                                                degree=0
                                                                stmt,degree=createArrayList_C(param,degree)
                                                                if parameter=='':
                                                                    parameter = str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
                                                                else:
                                                                    parameter += ","+str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
					var="['"+statement.name.name+"',"+parameter+"]"
		
                                
				if expression.getIsPrime()==False:
                                    if programsstart=="":
                                        programsstart="['-1','seq',['-1','=',"+str(var)+","+str(expressionCreator_C(expression.getExpression().rvalue))+"]"
                                        programsend="]"
				    else:
					programsstart+=",['-1','seq',['-1','=',"+str(var)+","+str(expressionCreator_C(expression.getExpression().rvalue))+"]"
					programsend+="]"
				else:
                                    if programsstart=="":
                                        programsstart="['-1','=',"+str(var)+","+str(expressionCreator_C(expression.getExpression().rvalue))+"]"+programsend
                                    else:
                                        programsstart+=",['-1','=',"+str(var)+","+str(expressionCreator_C(expression.getExpression().rvalue))+"]"+programsend

                        elif type(expression.getExpression()) is c_ast.FuncCall:
                        	parameter=''
                        	statement=expression.getExpression()
				if statement.args is not None:
			    		for param in statement.args.exprs:
			    			if type(param) is c_ast.ID:
			    				if parameter=='':
					        		parameter = str(eval("FOL_translation.expres('"+param.name+"')"))
					        	else:
					        		parameter += ","+str(eval("FOL_translation.expres('"+param.name+"')"))
			    			elif type(param) is c_ast.Constant:
			    		    		if parameter=='':
								parameter = str(eval("FOL_translation.expres('"+param.value+"')"))
							else:
					        		parameter += ","+str(eval("FOL_translation.expres('"+param.value+"')"))
						elif type(param) is c_ast.BinaryOp:
			    		    		if parameter=='':
								parameter =expressionCreator_C(param)
							else:
					        		parameter += ","+expressionCreator_C(param)
                                                else:
                                                    if type(param) is c_ast.ArrayRef:
                                                        #parameter_list.append('int')
                                                        degree=0
                                                        stmt,degree=createArrayList_C(param,degree)
                                                        if parameter=='':
                                                            parameter = str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
                                                        else:
                                                            parameter += ","+str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
					
                                        if expression.getIsPrime()==False:
						if programsstart=="":
							programsstart="['-1','seq',"+"['"+statement.name.name+"',"+parameter+"]"
					                programsend="]"
						else:
							programsstart+=","+"['-1','seq',"+"['"+statement.name.name+"',"+parameter+"]"
							programsend+="]"
					else:
						if programsstart=="":
					        	programsstart="['-1','seq',"+"['"+statement.name.name+"',"+parameter+"]"+programsend
					        else:
                                        		programsstart+=","+"['-1','seq',"+"['"+statement.name.name+"',"+parameter+"]"+programsend
				else:
  					if expression.getIsPrime()==False:
						if programsstart=="":
							programsstart="['-1','seq',"+str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))
							programsend="]"
						else:
							programsstart+=","+"['-1','seq',"+str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))
							programsend+="]"
					else:
						if programsstart=="":
							programsstart="['-1','seq',"+str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))+programsend
						else:
                                        		programsstart+=","+"['-1','seq',"+str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))+programsend
		elif type(expression) is list_class.blockclass:
			predicatestmt="['-1','while',"+expressionCreator_C(expression.predicate)+","+programToinductiveDefination_C( expression.getExpression(), allvariable)+"]"
			if expression.getIsPrime()==False:
				if programsstart=="":
					programsstart="['-1','seq',"+predicatestmt
					programsend="]"
				else:
					programsstart+=",['-1','seq',"+predicatestmt
					programsend+="]"
			else:
				programsstart+=","+predicatestmt+programsend
		elif type(expression) is list_class.Ifclass:
			condition=expressionCreator_C(expression.predicate)
			expressionif=None
			expressionelse=None
			predicatestmt=""
			if expression.getExpressionif() is not None:
				expressionif=programToinductiveDefination_C( expression.getExpressionif(), allvariable)
			if expression.getExpressionelse() is not None:
				if type(expression.getExpressionelse()) is list_class.Ifclass:
					#expressionelse=programToinductiveDefination( expression.getExpressionelse().getExpressionif(), allvariable)
					expressionelse=programToinductiveDefinationIfElse_C( expression.getExpressionelse(), allvariable)
				else:
					expressionelse=programToinductiveDefination_C( expression.getExpressionelse(), allvariable)
			if expressionif is not None and expressionelse is not None:
                          	predicatestmt="['-1','if2',"+condition+","+expressionif+","+expressionelse+"]"
			elif expressionif is not None and expressionelse is None:
				predicatestmt="['-1','if1',"+condition+","+expressionif+"]"
			if expression.getIsPrime()==False:
				if programsstart=="":
					programsstart="['-1','seq',"+predicatestmt
					programsend="]"
				else:
					programsstart+=",['-1','seq',"+predicatestmt
					programsend+="]"
			else:
				if programsstart=="":
					programsstart=predicatestmt+programsend
				else:
					programsstart+=","+predicatestmt+programsend
	if programsstart[0]==',':
		programsstart=programsstart[1:]	
	return programsstart





"""

IfElse Block Statement to Array of Statement Compatible to Translator Program 

"""
def programToinductiveDefinationIfElse_C(expression, allvariable):
	programsstart=""
	programsend=""
	statements=""
	if type(expression) is list_class.expressionclass:
		if type(expression.getExpression()) is c_ast.Assignment:
                        var=None
                        if type(expression.getExpression().lvalue) is c_ast.ID:
                            var=str(eval("FOL_translation.expres('"+str(expression.getExpression().lvalue.name)+"')"))
                        elif type(expression.getExpression().lvalue) is c_ast.Constant:
                            var=str(eval("FOL_translation.expres('"+str(expression.getExpression().lvalue.value)+"')"))
                        elif type(expression.getExpression().lvalue) is c_ast.ArrayRef:
			    	degree=0
			       	stmt,degree=createArrayList_C(expression.getExpression().lvalue,degree)
    				var=str(eval("FOL_translation.expres('d"+str(degree)+'array'+"',["+stmt+"])"))
			if expression.getIsPrime()==False:
                            if programsstart=="":
                                programsstart="['-1','seq',['-1','=',"+str(var)+","+str(expressionCreator(expression.getExpression().rhs))+"]"
                                programsend="]"
			    else:
                                programsstart+=",['-1','seq',['-1','=',"+str(var)+","+str(expressionCreator(expression.getExpression().rhs))+"]"
                                programsend+="]"
                        else:
                            if programsstart=="":
                                programsstart+="['-1','=',"+str(var)+","+str(expressionCreator(expression.getExpression().rhs))+"]"+programsend
                            else:
                                programsstart+=",['-1','=',"+str(var)+","+str(expressionCreator(expression.getExpression().rhs))+"]"+programsend

	elif type(expression) is list_class.blockclass:
		predicatestmt="['-1','while',"+expressionCreator_C(expression.predicate)+","+programToinductiveDefination_C( expression.getExpression(), allvariable)+"]"
		if expression.getIsPrime()==False:
			if programsstart=="":
				programsstart="['-1','seq',"+predicatestmt
				programsend="]"
			else:
				programsstart+=",['-1','seq',"+predicatestmt
				programsend+="]"
		else:
			if programsstart=="":
				programsstart+=","+predicatestmt+programsend
			
	elif type(expression) is list_class.Ifclass:
		condition=expressionCreator_C(expression.predicate)
		expressionif=None
		expressionelse=None
		predicatestmt=""
		if expression.getExpressionif() is not None:
			expressionif=programToinductiveDefination_C( expression.getExpressionif(), allvariable)
		if expression.getExpressionelse() is not None:
			if type(expression.getExpressionelse()) is list_class.Ifclass:
				#expressionelse=programToinductiveDefination( expression.getExpressionelse().getExpressionif(), allvariable)
				expressionelse=programToinductiveDefinationIfElse_C( expression.getExpressionelse(), allvariable)
			else:
				expressionelse=programToinductiveDefination_C( expression.getExpressionelse(), allvariable)
		if expressionif is not None and expressionelse is not None:
                	predicatestmt="['-1','if2',"+condition+","+expressionif+","+expressionelse+"]"
		elif expressionif is not None and expressionelse is None:
			predicatestmt="['-1','if1',"+condition+","+expressionif+"]"
		if expression.getIsPrime()==False:
			if programsstart=="":
				programsstart="['-1','seq',"+predicatestmt
				programsend="]"
			else:
				programsstart+=",['-1','seq',"+predicatestmt
				programsend+="]"
		else:
			if programsstart=="":
				programsstart=predicatestmt+programsend
			else:
				programsstart+=","+predicatestmt+programsend
 	return programsstart







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
Reset 
"""
def resetGlobal():
    global fun_call_map
    global current_fun_call
    fun_call_map={}
    current_fun_call=None



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
                
                #if statement.name.name in fun_call_map.keys() and statement.name.name != current_fun_call and '__VERIFIER_nondet_' not in statement.name.name:
                #    fc_count=fun_call_map[statement.name.name]
                #    fc_count+=1
                #    fun_call_map[statement.name.name]=fc_count
                #    return "['"+statement.name.name+"_"+str(fc_count)+"',"+parameter+"]"
                #else:
                #    fun_call_map[statement.name.name]=0
                #    return "['"+statement.name.name+"',"+parameter+"]"
                return "['"+statement.name.name+"',"+parameter+"]"
	else:
		if '__VERIFIER_nondet_' not in statement.name.name:
                    defineDetailtemp.append(statement.name.name)
                    defineDetailtemp.append(len(parameter_list)-1)
                    defineDetailtemp.append(parameter_list)
                    defineDetaillist.append(defineDetailtemp)
		#if statement.name.name in fun_call_map.keys() and statement.name.name != current_fun_call and '__VERIFIER_nondet_' not in statement.name.name:
                #    fc_count=fun_call_map[statement.name.name]
                #    fc_count+=1
                #    fun_call_map[statement.name.name]=fc_count
                #    return str(eval("FOL_translation.expres('"+statement.name.name+"_"+str(fc_count)+"'"+")"))
                #else:
                #    fun_call_map[statement.name.name]=0
                #    return str(eval("FOL_translation.expres('"+statement.name.name+"'"+")"))
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


#Construct Program for Assetion Analysis

def constructProgAssertAnalysis(functionbody,localvariables,inputvariables):
    #arg_list=[]
    #arg_list.append(c_ast.Constant(type="string", value="\"j:%d\\n\""))
    #arg_list.append(c_ast.ID(name="j"))
    #print_function=c_ast.FuncCall(name=c_ast.ID(name="printf"), args=c_ast.ExprList(exprs=arg_list))
    temp_localvariables = getVariables(functionbody)
    functionbody=c_ast.Compound(block_items=addPrintStmt(functionbody.block_items,temp_localvariables,inputvariables))
    return functionbody




def constructProgAssertAnalysis2(functionbody,localvariables,inputvariables,methodname):
    global count_for__VERIFIER_nondet
    global count_for__insert_flag
    global count_for__function_flag
    global count_ast_line_no
    global new_program_trace_var
    global line_no_stmt_map
    global back_line_no_stmt_map
    global main_line_no_stmt_ast_map
    
    if line_no_stmt_map is None:
        
        return (functionbody,functionbody)
    
    
    back_line_no_stmt_map=copy.deepcopy(line_no_stmt_map)
    

    count_for__VERIFIER_nondet=0
    count_for__insert_flag=0
    count_for__function_flag=0
    new_program_trace_var={}
    all_variable_map={}
    update_statements=[]
    parser = c_parser.CParser()
    try:
        new_statements=copy.deepcopy(functionbody.block_items)
        
        statements = constructExcutionTraceBlock(copy.deepcopy(functionbody.block_items),all_variable_map,methodname,new_statements)
        
        for x in new_program_trace_var.keys():
            program_temp='int '+x+'=0;'
            temp_ast = parser.parse(program_temp)
            update_statements.append(temp_ast.ext[0])
        for x in statements:
             update_statements.append(x)
    except Exception as e:
        print e
    functionbody.block_items=modify__VERIFIER_nondet_block(functionbody.block_items)
    functionbody=c_ast.Compound(block_items=addPrintStmt2(functionbody.block_items,localvariables,inputvariables))
    functionbody1=c_ast.Compound(block_items=update_statements)
    return (functionbody,functionbody1)


def getLineNumber(stmt,fun_name):
    global back_line_no_stmt_map
    find_list=[]
    find_list_ast=[]
    
    value=None
    value1=None
    if fun_name is not None:
        z=None
        list=back_line_no_stmt_map[fun_name]
        for x in list:
            if getSpaceRemoveStr(stmt) in getSpaceRemoveStr(x[1]):
                z=x
                break;
        
        if z is not None:
            list.remove(z)
            back_line_no_stmt_map[fun_name]=list
            value=z[0]
            value1=z[1]

    else:
        z=None
        list=back_line_no_stmt_map.keys()
        for x in list:
            if getSpaceRemoveStr(stmt) in getSpaceRemoveStr(x):
                z=x
                break;
        if z is not None:
            value=back_line_no_stmt_map[z]
            value1=z
            del back_line_no_stmt_map[z]
    
    return value,value1





def getLineNumberAssert(stmt):
    global back_line_no_stmt_map
    find_list=[]
    find_list_ast=[]
    
    value=None
    value1=None
    z=None
    for y in back_line_no_stmt_map.keys():
        TEMP_LIST= back_line_no_stmt_map[y]
        if isinstance(TEMP_LIST,list)==True:
            
            TEMP_LIST=back_line_no_stmt_map[y]
            for x in TEMP_LIST:
                if getSpaceRemoveStr(stmt) in getSpaceRemoveStr(x[1]):
                    z=x
                    break;
            if z!=None:
                break;

    if z is not None:
        value=z[0]
        value1=z[1]
    
    return value,value1


def getLineNumber_terminate(stmt,fun_name):
    global line_no_stmt_map
    find_list=[]
    find_list_ast=[]
    
    value=None
    value1=None
    if fun_name is not None:
        z=None
        list=line_no_stmt_map[fun_name]
        for x in list:
            if getSpaceRemoveStr(stmt) in getSpaceRemoveStr(x[1]):
                z=x
                break;
        
        if z is not None:
            list.remove(z)
            line_no_stmt_map[fun_name]=list
            value=z[0]
            value1=z[1]

    else:
        z=None
        list=line_no_stmt_map.keys()
        for x in list:
            if getSpaceRemoveStr(stmt) in getSpaceRemoveStr(x):
                z=x
                break;
        if z is not None:
            value=line_no_stmt_map[z]
            value1=z
            del line_no_stmt_map[z]
    
    return value,value1



def modify__VERIFIER_nondet_block(statements):
    update_statements=[]
    for statement in statements:
        if type(statement) is c_ast.Assignment:
            update_statements.append(modify__VERIFIER_nondet_stmt(statement))
        elif type(statement) is c_ast.While:
            update_statements.append(c_ast.While(cond=modify__VERIFIER_nondet_stmt(statement.cond), stmt=c_ast.Compound(block_items=modify__VERIFIER_nondet_block(statement.stmt.block_items))))
        elif type(statement) is c_ast.If:
            update_statements.append(modify__VERIFIER_nondet_blockIf(statement))
        else:
            update_statements.append(statement)
    
    return update_statements
    
def modify__VERIFIER_nondet_blockIf(statement):
    If_stmt=None
    Else_stmt=None
    cond_stmt=modify__VERIFIER_nondet_stmt(statement.cond)
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Compound:
            new_block_temp=modify__VERIFIER_nondet_block(statement.iftrue.block_items)
            If_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            If_stmt=statement.iftrue
    if type(statement.iffalse) is c_ast.Compound:
        if statement.iffalse.block_items is not None:
            new_block_temp=modify__VERIFIER_nondet_block(statement.iffalse.block_items)
            Else_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            Else_stmt=statement.iffalse
    else:
        if type(statement.iffalse) is c_ast.If:
            Else_stmt=modify__VERIFIER_nondet_blockIf(statement.iffalse)
        else:
            Else_stmt=statement.iffalse
    return c_ast.If(cond=cond_stmt, iftrue=If_stmt, iffalse=Else_stmt)
    
    
    
def modify__VERIFIER_nondet_stmt(statement):
    global count_for__VERIFIER_nondet
    if type(statement) is c_ast.BinaryOp:
        return c_ast.BinaryOp(op=statement.op,left=modify__VERIFIER_nondet_stmt(statement.left),right=modify__VERIFIER_nondet_stmt(statement.right))
    elif type(statement) is c_ast.Assignment:
        return c_ast.Assignment(op=statement.op,lvalue=modify__VERIFIER_nondet_stmt(statement.lvalue),rvalue=modify__VERIFIER_nondet_stmt(statement.rvalue))
    elif type(statement) is c_ast.FuncCall:
        if '__VERIFIER_nondet' in statement.name.name:
            if statement.args is None:
                arg_list=[]
                count_for__VERIFIER_nondet=count_for__VERIFIER_nondet+1
                arg_list.append(c_ast.Constant(type="int", value=str(count_for__VERIFIER_nondet)))
                return c_ast.FuncCall(name=statement.name, args=c_ast.ExprList(exprs=arg_list))
            else:
                return statement
        else:
            return statement
    else:
        return statement
    


def getArrayRef_Name(statement):
    if type(statement.name) is c_ast.ArrayRef:
        return getArrayRef_Name(statement.name)
    else:
        return statement.name.name
        

def createPrint(statement,localvariables,inputvariables):
    generator = c_generator.CGenerator()
    arg_list=[]
    mod_operator=None
    if type(statement) is c_ast.ID:
        if statement.name in localvariables.keys():
            mod_operator=localvariables[statement.name].getVariableType()
        elif statement.name in inputvariables.keys():
            mod_operator=inputvariables[statement.name].getVariableType()
    elif type(statement) is c_ast.ArrayRef:
        array_name=getArrayRef_Name(statement)
        if array_name in inputvariables.keys():
            mod_operator=inputvariables[array_name].getVariableType()
        elif array_name in localvariables.keys():
            mod_operator=localvariables[array_name].getVariableType()
    if mod_operator is not None:
        if mod_operator=='int':
            mod_operator='%d'
        elif mod_operator=='unsigned':
            mod_operator='%u'
        elif mod_operator=='long':
             mod_operator='%ld'
        elif mod_operator=='float':
            mod_operator='%f'
        elif mod_operator=='double':
            mod_operator='%f'
        else:
            mod_operator='%d'
            
    else:
        mod_operator='%d'
    var_name=str(generator.visit(statement))
    arg_list.append(c_ast.Constant(type="string", value="\""+var_name+":"+mod_operator+"\\n\""))
    arg_list.append(statement)
    print_stmt=c_ast.FuncCall(name=c_ast.ID(name="printf"), args=c_ast.ExprList(exprs=arg_list))
    return print_stmt



"""

#Finding last expression or block inside a block

"""

def primeStatement(expressions):
	previous=None
	if type(expressions) is list_class.Ifclass:
		primeStatement(expressions.getExpressionif())
		primeStatement(expressions.getExpressionelse())
		previous=expressions
        else:
         	if expressions is not None:
         		for expression in expressions:
	 			if previous is not None:
	 				previous.setIsPrime(False)
	 			if type(expression) is list_class.blockclass:
	 				primeStatement(expression.getExpression())
	 			if type(expression) is list_class.Ifclass:
	 				primeStatement(expression.getExpressionif())
	 				if expression.getExpressionelse() is not None:
	 					primeStatement(expression.getExpressionelse())
				previous=expression





# expr_find(e,e1): find subterm e1 in e 

def expr_find(e,e1): #e,e1,e2: expr
    if e==e1:
        return True
    else:
    	for x in FOL_translation.expr_args(e):
    		flag=expr_find(x,e1)
    		if flag:
    			return flag
    	return False


# Find array in equation

def findArrayInEq(e,array_list):
	flag=False
	array_value=None
	for arr in array_list:
		flag = expr_find(e,eval("['=',['_x1'],['"+arr+"']]"))
		if flag:
			return flag,arr
	return flag,array_value
    
# Find array list  in equation

def findArrayInEqlist(e,array_list,ins_array_lsit):
	flag=False
	array_value=None
	for arr in array_list:
		flag = expr_find(e,eval("['=',['_x1'],['"+arr+"']]"))
		if flag:
                    ins_array_lsit.append(arr)
	return ins_array_lsit




# Find array in equation

def findArrayInEqSp(e,array):
	flag=False
	array_value=None
        flag = expr_find(e,eval("['=',['_x1'],['"+array+"']]"))
	return flag

# Find array in equation

def findAllArrayInEq(e,array_list):
	flag=False
	array_value=[]
	for arr in array_list:
		flag = expr_find(e,eval("['=',['_x1'],['"+arr+"']]"))
		if flag:
			array_value.append(arr)
	return array_value


