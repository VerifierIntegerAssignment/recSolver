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


import xml.dom.minidom
import re
import random
#add by Pritom Rajkhowa
#import numpy as np
import resource
import hashlib
#import wolframalpha
#import sys
import itertools
import subprocess
from sympy import *
import regex
#import os
import copy
import time
import datetime
import ConfigParser
import SyntaxFilter
import commandclass
import fun_utiles
import graphclass
import list_class
import prog_transform
import utiles_translation
import viap_svcomp
from pyparsing import *
from sympy.core.relational import Relational
from pycparser1 import parse_file,c_parser, c_ast, c_generator
from pycparserext.ext_c_parser import GnuCParser
from pycparserext.ext_c_generator import GnuCGenerator
from itertools import permutations






def find_equiv(file_name1,file_name2):
    


	if not(os.path.exists(file_name1)): 
        	print "File 1 not exits"
		return
	if not(os.path.exists(file_name2)): 
        	print "File 2 not exits"
		return


	try:
		fd = open(file_name1)
		text = "".join(fd.readlines())
                original_program1=text
                
                
		fd = open(file_name2)
		text = "".join(fd.readlines())
                original_program2=text

                
	except SyntaxFilter.SLexerError as e:
                print 'Error(Find Error in Input File)'
		#print(e)
		return
            
            
	text1 = r""" """+original_program1
        
	text2 = r""" """+original_program2
        
	parser = GnuCParser()
        
        ast1 = parser.parse(text1)
        
        ast2 = parser.parse(text2)
        
        prog_transform.list_all_global_var()
        
        struct_map={}

    	counter=0 
        

        
    	externalvarmap1={}
        externalvarmap2={}
        
        externalvarmap={}
        
        externalarraymap1={}
        externalarraymap2={}
        
        externalarraymap={}
    
        functionvarmap_temp1={}
        functionvarmap_temp2={}
        
	functionvarmap={}
        
        function_vfacts=[]
        
	memberfunctionmap={}
	axiomeMap={}
	addition_array_map={}
	function_vfact_map={}
	witnessXml_map={}
	
    	counter=0 
       
        

        try:
            
            for e in ast1.ext:
                    if type(e) is c_ast.Decl:
                            if type(e.type) is c_ast.FuncDecl:
                                    parametermap={}
                                    structType=None
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
                                    if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                    if param_decl.name is not None:
                                                            structType=None
                                                            if type(param_decl.type) is c_ast.ArrayDecl:
                                                                    degree=0
                                                                    dimensionmap={}
                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                    variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                            else:
                                                                    try:
                                                                        variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                    except Exception as e:
                                                                        print 'Unknown'
                                                                        return
                                                            parametermap[param_decl.name]=variable

                                    membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,None,None,0,0,None,None,None)
                                    functionvarmap_temp1[membermethod.getMethodname()]=membermethod

                            elif type(e.type) is c_ast.TypeDecl:
                                    var_type=None
                                    initial_value=None
                                    structType=None
                                    e=prog_transform.change_var_name_decl(e)
                                    for child in e.children():
                                            if type(child[1].type) is c_ast.IdentifierType:
                                                    var_type=child[1].type.names[0]
                                            else:
                    				
                                                    initial_value=child[1].value

                                    variable=list_class.variableclass(e.name, var_type,None,None,initial_value,structType)
                                    program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                    externalvarmap1[e.name]=variable
                                    external_var_map1[e.name]=e.name
                            elif type(e.type) is c_ast.ArrayDecl:
                                program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                array_name=prog_transform.getArrayNameDecl(e.type)
                                externalarraymap1[array_name]=prog_transform.change_var_name_decl(e)
                                external_var_map1[array_name]=e.name
                    else:
                            if type(e) is c_ast.FuncDef:                          
                                    parametermap={}
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
    				
                                    function_decl=e.decl
                                
                                
                                    function_body = e.body
                                
                                    if function_body.block_items is not None:
                                        temp_statements=[]
                                        if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                temp_statements.append(param_decl)

                                        statements=function_body.block_items
                                        statements=temp_statements+statements
                                        statements=prog_transform.change_var_name(statements)
                                        function_body= c_ast.Compound(block_items=statements)
                                        localvarmap=prog_transform.getVariables(function_body)
                                        counter=counter+1
                                        if function_decl.type.args is not None:
                                                for param_decl in function_decl.type.args.params:
                                                        new_param_decl=prog_transform.declarationModifying(param_decl)
                                                        if new_param_decl is not None:
                                                            param_decl=new_param_decl
                                                        param_decl=prog_transform.change_var_name_decl(param_decl)
                                                        if param_decl.name is not None:
                                                                structType=None
                                                                if type(param_decl.type) is c_ast.ArrayDecl:
                                                                        #print param_decl.show()
                                                                        degree=0
                                                                        dimensionmap={}
                                                                        data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                        variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                elif type(param_decl.type) is c_ast.PtrDecl:
                                                                        stmt=pointerToArray(param_decl)
                                                                        #print stmt.show()
                                                                        if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                degree=0
                                                                                dimensionmap={}
                                                                                data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                                variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
                                                                else:				
                                                                        try:
                                                                            variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                        except Exception as e:
                                                                            print 'Error(Translation to Intermate Intermediate)'
                                                                            print e
                                                                            return
                                                                parametermap[param_decl.name]=variable
                                    if function_decl.name in functionvarmap_temp1.keys():
                                            if function_decl.name!='__VERIFIER_assert':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,None,function_decl)
                                                functionvarmap_temp1[function_decl.name]=membermethod
                                    else:
                                            if function_decl.type.args is not None:
                                                    for param_decl in function_decl.type.args.params:
                                                            new_param_decl=prog_transform.declarationModifying(param_decl)
                                                            if new_param_decl is not None:
                                                                param_decl=new_param_decl
                                                                param_decl=prog_transform.change_var_name_decl(param_decl)
                                                            if param_decl.name is not None:
                                                                    structType=None
                                                                    if type(param_decl.type) is c_ast.ArrayDecl:
                                                                            degree=0
                                                                            dimensionmap={}
                                                                            data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                            variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                    elif type(param_decl.type) is c_ast.PtrDecl:
                                                                            stmt=pointerToArray(param_decl)
                                                                            if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                    degree=0
                                                                                    dimensionmap={}
                                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap={})
                                                                                    variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
								
                                                                    else:	
                                                                            try:
                                                                                variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                            except Exception as e:
                                                                                print 'Error(Translation to Intermate Intermediate)'
                                                                                print e
                                                                                return
                                                                    parametermap[param_decl.name]=variable
                                            if function_decl.name!='__VERIFIER_assert' and function_decl.name!='exit':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,copy.deepcopy(function_body),function_decl)
                                                functionvarmap_temp1[membermethod.getMethodname()]=membermethod


            for e in ast2.ext:
                    if type(e) is c_ast.Decl:
                            if type(e.type) is c_ast.FuncDecl:
                                    parametermap={}
                                    structType=None
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
                                    if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                    if param_decl.name is not None:
                                                            structType=None
                                                            if type(param_decl.type) is c_ast.ArrayDecl:
                                                                    degree=0
                                                                    dimensionmap={}
                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                    variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                            else:
                                                                    try:
                                                                        variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                    except Exception as e:
                                                                        print 'Unknown'
                                                                        return
                                                            parametermap[param_decl.name]=variable

                                    membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,None,None,0,0,None,None,None)
                                    functionvarmap_temp2[membermethod.getMethodname()]=membermethod

                            elif type(e.type) is c_ast.TypeDecl:
                                    var_type=None
                                    initial_value=None
                                    structType=None
                                    e=prog_transform.change_var_name_decl(e)
                                    for child in e.children():
                                            if type(child[1].type) is c_ast.IdentifierType:
                                                    var_type=child[1].type.names[0]
                                            else:
                    				
                                                    initial_value=child[1].value
                                    variable=list_class.variableclass(e.name, var_type,None,None,initial_value,structType)
                                    program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                    externalvarmap2[e.name]=variable
                                    external_var_map[e.name]=e.name
                            elif type(e.type) is c_ast.ArrayDecl:
                                program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                array_name=prog_transform.getArrayNameDecl(e.type)
                                externalarraymap2[array_name]=prog_transform.change_var_name_decl(e)
                                external_var_map2[array_name]=e.name
                    else:
                            if type(e) is c_ast.FuncDef:                          
                                    parametermap={}
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
    				
                                    function_decl=e.decl
                                
                                
                                    function_body = e.body
                                
                                    if function_body.block_items is not None:
                                        
                                        temp_statements=[]
                                        if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                temp_statements.append(param_decl)
                                        statements=function_body.block_items
                                        statements=temp_statements+statements
                                        statements=prog_transform.change_var_name(statements)
                                        function_body= c_ast.Compound(block_items=statements)
                                        localvarmap=prog_transform.getVariables(function_body)
                                        counter=counter+1
                                        if function_decl.type.args is not None:
                                                for param_decl in function_decl.type.args.params:
                                                        new_param_decl=prog_transform.declarationModifying(param_decl)
                                                        if new_param_decl is not None:
                                                            param_decl=new_param_decl
                                                        param_decl=prog_transform.change_var_name_decl(param_decl)
                                                        if param_decl.name is not None:
                                                                structType=None
                                                                if type(param_decl.type) is c_ast.ArrayDecl:
                                                                        degree=0
                                                                        dimensionmap={}
                                                                        data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                        variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                elif type(param_decl.type) is c_ast.PtrDecl:
                                                                        stmt=pointerToArray(param_decl)
                                                                        if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                degree=0
                                                                                dimensionmap={}
                                                                                data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                                variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
                                                                else:				
                                                                        try:
                                                                            variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                        except Exception as e:
                                                                            print 'Error(Translation to Intermate Intermediate)'
                                                                            print e
                                                                            return
                                                                parametermap[param_decl.name]=variable
                                    if function_decl.name in functionvarmap_temp2.keys():
                                            if function_decl.name!='__VERIFIER_assert':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,None,function_decl)
                                                functionvarmap_temp2[function_decl.name]=membermethod
                                    else:
                                            if function_decl.type.args is not None:
                                                    for param_decl in function_decl.type.args.params:
                                                            new_param_decl=prog_transform.declarationModifying(param_decl)
                                                            if new_param_decl is not None:
                                                                param_decl=new_param_decl
                                                                param_decl=prog_transform.change_var_name_decl(param_decl)
                                                            if param_decl.name is not None:
                                                                    structType=None
                                                                    if type(param_decl.type) is c_ast.ArrayDecl:
                                                                            degree=0
                                                                            dimensionmap={}
                                                                            data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                            variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                    elif type(param_decl.type) is c_ast.PtrDecl:
                                                                            stmt=pointerToArray(param_decl)
                                                                            if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                    degree=0
                                                                                    dimensionmap={}
                                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap={})
                                                                                    variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
								
                                                                    else:	
                                                                            try:
                                                                                variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                            except Exception as e:
                                                                                print 'Error(Translation to Intermate Intermediate)'
                                                                                print str(e)
                                                                                return
                                                                    parametermap[param_decl.name]=variable
                                            if function_decl.name!='__VERIFIER_assert' and function_decl.name!='exit':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,copy.deepcopy(function_body),function_decl)
                                                functionvarmap_temp2[membermethod.getMethodname()]=membermethod





        except Exception as e:
            print 'Syntax Error'
            print e
            return
                
        
        
        for index in range(0,len(functionvarmap_temp1.keys())):
            
            parameters=None
            
            
            medthod1 = functionvarmap_temp1.keys()[index]
            membermethod1=functionvarmap_temp1[medthod1]
            parameters1 = membermethod1.getInputvar()
            
            medthod2 = functionvarmap_temp2.keys()[index]
            membermethod2=functionvarmap_temp2[medthod2]
            parameters2 = membermethod2.getInputvar()
            
            
            for index1 in range(0,len(parameters1)):
                
                parameter1 = parameters1.keys()
                
                parameter2 = parameters2.keys()
                
                if parameters is None:
                    parameters = c_ast.BinaryOp(op='==', left=c_ast.ID(name='p1_'+parameter1[index1]), right=c_ast.ID(name='p2_'+parameter2[index1]))
                else:
                    parameters = c_ast.BinaryOp(op='&&', left=parameters, right=c_ast.BinaryOp(op='==', left=c_ast.ID(name='p1_'+parameter1[index1]), right=c_ast.ID(name='p2_'+parameter2[index1])))
                    
            body1=membermethod1.getBody()
            
            if body1 is not None:
                
                if body1.block_items is not None:
                    
                    try:

                        statements1 = prog_transform.programTransformation(body1,functionvarmap_temp1,medthod1)
                        
                        statements1 = prog_transform.updatePointerStruct(statements1,struct_map)
                            
                        statements1 = prog_transform.update_var_name(statements1,'p1')
                        

                    except Exception as e:
                        #print 'Error(Translation to Intermate Intermediate)'
                        print 'Syntax Translation'
                        print str(e)
                        return
                       
                    for temp_method in externalarraymap1.keys():
                        if isVarPresnt(statements1,temp_method)==True:
                            new_statements=[]
                            new_statements.append(externalarraymap1[temp_method])
                            statements1=prog_transform.construct_program(new_statements+statements1)
                    body_comp1 = c_ast.Compound(block_items=statements1)
                    localvarmap1=prog_transform.getVariables(body_comp1)
                    statements1,localvarmap1=prog_transform.addAllExtVariables(statements1,externalvarmap1,localvarmap1)
                    statements1 = prog_transform.translateStruct(statements1,localvarmap1,struct_map)
                    #statements=pointerHandling(statements,pointer_list,array_list)
                    body_comp1 = c_ast.Compound(block_items=statements1)
                    membermethod1.setBody(body_comp1)
                    membermethod1.setLocalvar(localvarmap1)
                    
                else:
                    membermethod1.setBody(None)
                    membermethod1.setLocalvar(None)
            else:
                membermethod1.setBody(None)
                membermethod1.setLocalvar(None)

            body2=membermethod2.getBody()
                        
            if body2 is not None:
               
                if body2.block_items is not None:
                   
                    try:

                        statements2 = prog_transform.programTransformation(body2,functionvarmap_temp2,medthod2)
                        
                        statements2 = prog_transform.updatePointerStruct(statements2,struct_map)
                            
                        statements2 = prog_transform.update_var_name(statements2,'p2')
                        

                    except Exception as e:
                        #print 'Error(Translation to Intermate Intermediate)'
                        print 'Syntax Translation'
                        print str(e)
                        return
                       
                    for temp_method in externalarraymap2.keys():
                        if isVarPresnt(statements2,temp_method)==True:
                            new_statements=[]
                            new_statements.append(externalarraymap2[temp_method])
                            statements2=prog_transform.construct_program(new_statements+statements2)
                    body_comp2 = c_ast.Compound(block_items=statements2)
                    localvarmap2=prog_transform.getVariables(body_comp2)
                    statements2,localvarmap2=prog_transform.addAllExtVariables(statements2,externalvarmap2,localvarmap2)
                    statements2 = prog_transform.translateStruct(statements2,localvarmap2,struct_map)
                    #statements=pointerHandling(statements,pointer_list,array_list)
                    body_comp2 = c_ast.Compound(block_items=statements2)
                    membermethod2.setBody(body_comp2)
                    membermethod2.setLocalvar(localvarmap2)
                    
                else:
                    membermethod2.setBody(None)
                    membermethod2.setLocalvar(None)
            else:
                membermethod2.setBody(None)
                membermethod2.setLocalvar(None)
            
            if membermethod1.getreturnType()==membermethod1.getreturnType():
                
                local_var_map={}
                
                for x in membermethod1.getLocalvar():
                    
                    local_var_map[x]=membermethod1.getLocalvar()[x]

                for x in membermethod2.getLocalvar():
                    
                    local_var_map[x]=membermethod2.getLocalvar()[x]
                    


                body = prog_transform.construct_main_program(membermethod1.getBody(), membermethod2.getBody(), parameters)
                
                fun_utiles.writtingFile( '_eqv.i' , '' )
                generator = c_generator.CGenerator()
                fun_utiles.writtingFile( '_eqv.i' , "void main()\n"+generator.visit(body) )
                viap_svcomp.prove_auto('_eqv.i',property=None)
                #print(generator.visit(body))







def find_equiv1(file_name1,file_name2):
    


	if not(os.path.exists(file_name1)): 
        	print "File 1 not exits"
		return
	if not(os.path.exists(file_name2)): 
        	print "File 2 not exits"
		return


	try:
		fd = open(file_name1)
		text = "".join(fd.readlines())
                original_program1=text
                
                
		fd = open(file_name2)
		text = "".join(fd.readlines())
                original_program2=text

                
	except SyntaxFilter.SLexerError as e:
                print 'Error(Find Error in Input File)'
		#print(e)
		return
            
            
	text1 = r""" """+original_program1
        
	text2 = r""" """+original_program2
        
	parser = GnuCParser()
        
        ast1 = parser.parse(text1)
        
        ast2 = parser.parse(text2)
        
        prog_transform.list_all_global_var()
        
        struct_map={}

    	counter=0 
        

        
    	externalvarmap1={}
        externalvarmap2={}
        
        externalvarmap={}
        
        externalarraymap1={}
        externalarraymap2={}
        
        externalarraymap={}
    
        functionvarmap_temp1={}
        functionvarmap_temp2={}
        
	functionvarmap={}
        
        function_vfacts=[]
        
	memberfunctionmap={}
	axiomeMap={}
	addition_array_map={}
	function_vfact_map={}
	witnessXml_map={}
	
    	counter=0 
       
        

        try:
            
            for e in ast1.ext:
                    if type(e) is c_ast.Decl:
                            if type(e.type) is c_ast.FuncDecl:
                                    parametermap={}
                                    structType=None
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
                                    if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                    if param_decl.name is not None:
                                                            structType=None
                                                            if type(param_decl.type) is c_ast.ArrayDecl:
                                                                    degree=0
                                                                    dimensionmap={}
                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                    variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                            else:
                                                                    try:
                                                                        variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                    except Exception as e:
                                                                        print 'Unknown'
                                                                        return
                                                            parametermap[param_decl.name]=variable

                                    membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,None,None,0,0,None,None,None)
                                    functionvarmap_temp1[membermethod.getMethodname()]=membermethod

                            elif type(e.type) is c_ast.TypeDecl:
                                    var_type=None
                                    initial_value=None
                                    structType=None
                                    e=prog_transform.change_var_name_decl(e)
                                    for child in e.children():
                                            if type(child[1].type) is c_ast.IdentifierType:
                                                    var_type=child[1].type.names[0]
                                            else:
                    				
                                                    initial_value=child[1].value

                                    variable=list_class.variableclass(e.name, var_type,None,None,initial_value,structType)
                                    program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                    externalvarmap1[e.name]=variable
                                    external_var_map1[e.name]=e.name
                            elif type(e.type) is c_ast.ArrayDecl:
                                program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                array_name=prog_transform.getArrayNameDecl(e.type)
                                externalarraymap1[array_name]=prog_transform.change_var_name_decl(e)
                                external_var_map1[array_name]=e.name
                    else:
                            if type(e) is c_ast.FuncDef:                          
                                    parametermap={}
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
    				
                                    function_decl=e.decl
                                
                                
                                    function_body = e.body
                                
                                    if function_body.block_items is not None:
                                        statements=function_body.block_items
                                        statements=prog_transform.change_var_name(statements)
                                        function_body= c_ast.Compound(block_items=statements)
                                        localvarmap=prog_transform.getVariables(function_body)
                                        counter=counter+1
                                        if function_decl.type.args is not None:
                                                for param_decl in function_decl.type.args.params:
                                                        new_param_decl=prog_transform.declarationModifying(param_decl)
                                                        if new_param_decl is not None:
                                                            param_decl=new_param_decl
                                                        param_decl=prog_transform.change_var_name_decl(param_decl)
                                                        if param_decl.name is not None:
                                                                structType=None
                                                                if type(param_decl.type) is c_ast.ArrayDecl:
                                                                        #print param_decl.show()
                                                                        degree=0
                                                                        dimensionmap={}
                                                                        data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                        variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                elif type(param_decl.type) is c_ast.PtrDecl:
                                                                        stmt=pointerToArray(param_decl)
                                                                        #print stmt.show()
                                                                        if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                degree=0
                                                                                dimensionmap={}
                                                                                data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                                variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
                                                                else:				
                                                                        try:
                                                                            variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                        except Exception as e:
                                                                            print 'Error(Translation to Intermate Intermediate)'
                                                                            print e
                                                                            return
                                                                parametermap[param_decl.name]=variable
                                    if function_decl.name in functionvarmap_temp1.keys():
                                            if function_decl.name!='__VERIFIER_assert':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,None,function_decl)
                                                functionvarmap_temp1[function_decl.name]=membermethod
                                    else:
                                            if function_decl.type.args is not None:
                                                    for param_decl in function_decl.type.args.params:
                                                            new_param_decl=prog_transform.declarationModifying(param_decl)
                                                            if new_param_decl is not None:
                                                                param_decl=new_param_decl
                                                                param_decl=prog_transform.change_var_name_decl(param_decl)
                                                            if param_decl.name is not None:
                                                                    structType=None
                                                                    if type(param_decl.type) is c_ast.ArrayDecl:
                                                                            degree=0
                                                                            dimensionmap={}
                                                                            data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                            variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                    elif type(param_decl.type) is c_ast.PtrDecl:
                                                                            stmt=pointerToArray(param_decl)
                                                                            if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                    degree=0
                                                                                    dimensionmap={}
                                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap={})
                                                                                    variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
								
                                                                    else:	
                                                                            try:
                                                                                variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                            except Exception as e:
                                                                                print 'Error(Translation to Intermate Intermediate)'
                                                                                print e
                                                                                return
                                                                    parametermap[param_decl.name]=variable
                                            if function_decl.name!='__VERIFIER_assert' and function_decl.name!='exit':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,copy.deepcopy(function_body),function_decl)
                                                functionvarmap_temp1[membermethod.getMethodname()]=membermethod


            for e in ast2.ext:
                    if type(e) is c_ast.Decl:
                            if type(e.type) is c_ast.FuncDecl:
                                    parametermap={}
                                    structType=None
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
                                    if function_decl.type.args is not None:
                                            for param_decl in function_decl.type.args.params:
                                                    if param_decl.name is not None:
                                                            structType=None
                                                            if type(param_decl.type) is c_ast.ArrayDecl:
                                                                    degree=0
                                                                    dimensionmap={}
                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                    variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                            else:
                                                                    try:
                                                                        variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                    except Exception as e:
                                                                        print 'Unknown'
                                                                        return
                                                            parametermap[param_decl.name]=variable

                                    membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,None,None,0,0,None,None,None)
                                    functionvarmap_temp2[membermethod.getMethodname()]=membermethod

                            elif type(e.type) is c_ast.TypeDecl:
                                    var_type=None
                                    initial_value=None
                                    structType=None
                                    e=prog_transform.change_var_name_decl(e)
                                    for child in e.children():
                                            if type(child[1].type) is c_ast.IdentifierType:
                                                    var_type=child[1].type.names[0]
                                            else:
                    				
                                                    initial_value=child[1].value
                                    variable=list_class.variableclass(e.name, var_type,None,None,initial_value,structType)
                                    program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                    externalvarmap2[e.name]=variable
                                    external_var_map[e.name]=e.name
                            elif type(e.type) is c_ast.ArrayDecl:
                                program_analysis_var_decl=program_analysis_var_decl+str(generator.visit(e))+';\n'
                                array_name=prog_transform.getArrayNameDecl(e.type)
                                externalarraymap2[array_name]=prog_transform.change_var_name_decl(e)
                                external_var_map2[array_name]=e.name
                    else:
                            if type(e) is c_ast.FuncDef:                          
                                    parametermap={}
                                    new_e,pointer_list,array_list=prog_transform.pointerHandlingParameter(e)
                                    if new_e is None:
                                            function_decl=e
                                    else:
                                            function_decl=new_e
    				
                                    function_decl=e.decl
                                
                                
                                    function_body = e.body
                                
                                    if function_body.block_items is not None:

                                        statements=function_body.block_items
                                        statements=prog_transform.change_var_name(statements)
                                        function_body= c_ast.Compound(block_items=statements)
                                        localvarmap=prog_transform.getVariables(function_body)
                                        counter=counter+1
                                        if function_decl.type.args is not None:
                                                for param_decl in function_decl.type.args.params:
                                                        new_param_decl=prog_transform.declarationModifying(param_decl)
                                                        if new_param_decl is not None:
                                                            param_decl=new_param_decl
                                                        param_decl=prog_transform.change_var_name_decl(param_decl)
                                                        if param_decl.name is not None:
                                                                structType=None
                                                                if type(param_decl.type) is c_ast.ArrayDecl:
                                                                        degree=0
                                                                        dimensionmap={}
                                                                        data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                        variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                elif type(param_decl.type) is c_ast.PtrDecl:
                                                                        stmt=pointerToArray(param_decl)
                                                                        if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                degree=0
                                                                                dimensionmap={}
                                                                                data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                                variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
                                                                else:				
                                                                        try:
                                                                            variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                        except Exception as e:
                                                                            print 'Error(Translation to Intermate Intermediate)'
                                                                            print e
                                                                            return
                                                                parametermap[param_decl.name]=variable
                                    if function_decl.name in functionvarmap_temp2.keys():
                                            if function_decl.name!='__VERIFIER_assert':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,None,function_decl)
                                                functionvarmap_temp2[function_decl.name]=membermethod
                                    else:
                                            if function_decl.type.args is not None:
                                                    for param_decl in function_decl.type.args.params:
                                                            new_param_decl=prog_transform.declarationModifying(param_decl)
                                                            if new_param_decl is not None:
                                                                param_decl=new_param_decl
                                                                param_decl=prog_transform.change_var_name_decl(param_decl)
                                                            if param_decl.name is not None:
                                                                    structType=None
                                                                    if type(param_decl.type) is c_ast.ArrayDecl:
                                                                            degree=0
                                                                            dimensionmap={}
                                                                            data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap)
                                                                            variable=list_class.variableclass(param_decl.name, data_type,None,dimensionmap,None,structType)
                                                                    elif type(param_decl.type) is c_ast.PtrDecl:
                                                                            stmt=pointerToArray(param_decl)
                                                                            if stmt is not None and type(stmt.type) is c_ast.ArrayDecl:
                                                                                    degree=0
                                                                                    dimensionmap={}
                                                                                    data_type,degree,structType=prog_transform.getArrayDetails(param_decl,degree,dimensionmap={})
                                                                                    variable=list_class.variableclass(stmt.name, data_type,None,dimensionmap,None,structType)
								
                                                                    else:	
                                                                            try:
                                                                                variable=list_class.variableclass(param_decl.name, param_decl.type.type.names[0],None,None,None,structType)
                                                                            except Exception as e:
                                                                                print 'Error(Translation to Intermate Intermediate)'
                                                                                print str(e)
                                                                                return
                                                                    parametermap[param_decl.name]=variable
                                            if function_decl.name!='__VERIFIER_assert' and function_decl.name!='exit':
                                                membermethod=list_class.membermethodclass(function_decl.name,function_decl.type.type.type.names[0],parametermap,localvarmap,function_body,0,counter,None,copy.deepcopy(function_body),function_decl)
                                                functionvarmap_temp2[membermethod.getMethodname()]=membermethod





        except Exception as e:
            print 'Syntax Error'
            print e
            return
        for index in range(0,len(functionvarmap_temp1.keys())):
            
            parameters=None
            
            
            medthod1 = functionvarmap_temp1.keys()[index]
            membermethod1=functionvarmap_temp1[medthod1]
            parameters1 = membermethod1.getInputvar()
            
            medthod2 = functionvarmap_temp2.keys()[index]
            membermethod2=functionvarmap_temp2[medthod2]
            parameters2 = membermethod2.getInputvar()
            
            
            for index1 in range(0,len(parameters1)):
                
                parameter1 = parameters1.keys()
                
                parameter2 = parameters2.keys()
                                
                if parameters is None:
                    parameters = c_ast.BinaryOp(op='=', left=c_ast.ID(name=parameter1[index1]), right=c_ast.ID(name=parameter2[index1]))
                else:
                    parameters = c_ast.BinaryOp(op='&&', left=parameters, right=c_ast.BinaryOp(op='=', left=c_ast.ID(name=parameter1[index1]), right=c_ast.ID(name=parameter2[index1])))
                    
            body1=membermethod1.getBody()
            
            if body1 is not None:
                
                if body1.block_items is not None:
                    
                    try:

                        statements1 = prog_transform.programTransformation(body1,functionvarmap_temp1,medthod1)
                        
                        statements1 = prog_transform.updatePointerStruct(statements1,struct_map)
                            
                        statements1 = prog_transform.update_var_name(statements1,'p1')
                        

                    except Exception as e:
                        #print 'Error(Translation to Intermate Intermediate)'
                        print 'Syntax Translation'
                        print str(e)
                        return
                       
                    for temp_method in externalarraymap1.keys():
                        if isVarPresnt(statements1,temp_method)==True:
                            new_statements=[]
                            new_statements.append(externalarraymap1[temp_method])
                            statements1=prog_transform.construct_program(new_statements+statements1)
                    body_comp1 = c_ast.Compound(block_items=statements1)
                    localvarmap1=prog_transform.getVariables(body_comp1)
                    statements1,localvarmap1=prog_transform.addAllExtVariables(statements1,externalvarmap1,localvarmap1)
                    statements1 = prog_transform.translateStruct(statements1,localvarmap1,struct_map)
                    #statements=pointerHandling(statements,pointer_list,array_list)
                    body_comp1 = c_ast.Compound(block_items=statements1)
                    membermethod1.setBody(body_comp1)
                    membermethod1.setLocalvar(localvarmap1)
                    
                else:
                    membermethod1.setBody(None)
                    membermethod1.setLocalvar(None)
            else:
                membermethod1.setBody(None)
                membermethod1.setLocalvar(None)

            body2=membermethod2.getBody()
                        
            if body2 is not None:
               
                if body2.block_items is not None:
                   
                    try:

                        statements2 = prog_transform.programTransformation(body2,functionvarmap_temp2,medthod2)
                        
                        statements2 = prog_transform.updatePointerStruct(statements2,struct_map)
                            
                        statements2 = prog_transform.update_var_name(statements2,'p2')
                        

                    except Exception as e:
                        #print 'Error(Translation to Intermate Intermediate)'
                        print 'Syntax Translation'
                        print str(e)
                        return
                       
                    for temp_method in externalarraymap2.keys():
                        if isVarPresnt(statements2,temp_method)==True:
                            new_statements=[]
                            new_statements.append(externalarraymap2[temp_method])
                            statements2=prog_transform.construct_program(new_statements+statements2)
                    body_comp2 = c_ast.Compound(block_items=statements2)
                    localvarmap2=prog_transform.getVariables(body_comp2)
                    statements2,localvarmap2=prog_transform.addAllExtVariables(statements2,externalvarmap2,localvarmap2)
                    statements2 = prog_transform.translateStruct(statements2,localvarmap2,struct_map)
                    #statements=pointerHandling(statements,pointer_list,array_list)
                    body_comp2 = c_ast.Compound(block_items=statements2)
                    membermethod2.setBody(body_comp2)
                    membermethod2.setLocalvar(localvarmap2)
                    
                else:
                    membermethod2.setBody(None)
                    membermethod2.setLocalvar(None)
            else:
                membermethod2.setBody(None)
                membermethod2.setLocalvar(None)
            
            if membermethod1.getreturnType()==membermethod1.getreturnType():
                
                local_var_map={}
                
                for x in membermethod1.getLocalvar():
                    
                    local_var_map[x]=membermethod1.getLocalvar()[x]

                for x in membermethod2.getLocalvar():
                    
                    local_var_map[x]=membermethod2.getLocalvar()[x]

                body = prog_transform.construct_main_program(membermethod1.getBody(), membermethod2.getBody(), parameters)
                
                body
                generator = c_generator.CGenerator()
                print(generator.visit(body))

                
            
                #membermethod=list_class.membermethodclass('main', membermethod1.getreturnType(),{},local_var_map,body,0,membermethod1.getSerialNo(),None,None,function_decl)
                
                #functionvarmap['main']=membermethod
                
                #statements = prog_transform.programTransformation(body,functionvarmap,'main')
                
                #body_comp = c_ast.Compound(block_items=statements)
                #membermethod.setBody(body_comp)

                
                generator = c_generator.CGenerator()
                print(generator.visit(membermethod.getBody()))
                
            else:
                
                print 'Return Types are Different'
                return

    	temp_functionvarmap={}
    	
    	for medthod in functionvarmap.keys():
                membermethod=functionvarmap[medthod]
                in_var_map=membermethod.getInputvar()
                if len(in_var_map)>0:
                    for x in in_var_map:
                        variable=in_var_map[x]
                        if variable.getDimensions() is not None and len(variable.getDimensions())>0:
                            temp_functionvarmap[medthod]=functionvarmap[medthod]
                elif medthod=='main':
                        temp_functionvarmap[medthod]=functionvarmap[medthod]
                
    	
    	for medthod in functionvarmap.keys():
                membermethod=functionvarmap[medthod]
    		body=membermethod.getBody()
    		if body is not None:
                    if medthod=='main':
                        statements=body.block_items
                        statements = prog_transform.substituteFunBlock(statements,temp_functionvarmap,medthod,externalvarmap)
                        body_comp = c_ast.Compound(block_items=statements)
                        membermethod.setBody(body_comp)
                        #body_comp = c_ast.Compound(block_items=statements)
                        #generator = c_generator.CGenerator()
                        #print(generator.visit(body_comp))
                        if len(temp_functionvarmap)>0:
                            ret_body_comp,temp_status1,temp_status2 = prog_transform.reduceArraySize1("int main()"+generator.visit(body_comp))
                        
                            if ret_body_comp is not None and temp_status1==True and temp_status2:
                                body_comp = ret_body_comp.body
                                membermethod.setBody(body_comp)


    
    	#program in intermediate form
    	programeIF=[]

    	programeIF.append('-1')
    			
    	programeIF.append('prog')

    	programe_array=[]

    	variables_list_map={}
        
    	for medthod in functionvarmap.keys():
                f_vfact=[]
                f_vfact_para=[]
    		membermethod=functionvarmap[medthod]
                if membermethod.getreturnType() is not 'void':
                    f_vfact.append(medthod)
                    f_vfact_para.append(membermethod.getreturnType())
                    for iv in membermethod.getInputvar():
                        i_var=membermethod.getInputvar()[iv]
                        f_vfact_para.append(i_var.getVariableType())
                    f_vfact.append(len(f_vfact_para)-1)
                    f_vfact.append(f_vfact_para)
                    function_vfacts.append(f_vfact)

                
    		body=membermethod.getBody()
                
    		if body is not None:
    			new_variable={}
    			update_statements=[]
    			   		
	    		body_comp=body
	    		
	    		membermethod.setTempoary(body_comp)
	    		
	    		statements=body.block_items
	    		
	    		new_variable.clear()

	    		update_statements=[]
			
			for var in new_variable.keys():
				if isBoolVariable( var )==True:
			    	    	#temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['_Bool'])), init=c_ast.Constant(type='_Bool', value=None), bitsize=None)
                                        temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
			    		update_statements.append(temp)
			    	else:
			    		if type(new_variable[var]) is tuple:
                                            type_stmt,t_degree=new_variable[var]
                                            program_temp=type_stmt+' '+var
                                            for x in range(0,t_degree):
                                                program_temp+='[]'
                                            program_temp+=';'
                                            temp_ast = parser.parse(program_temp)
                                            update_statements.append(temp_ast.ext[0])
                                        else:
                                            if var in new_variable_array.keys():
                                                type_stmt='int'
                                                t_degree=new_variable_array[var]
                                                program_temp=type_stmt+' '+var
                                                for x in range(0,t_degree):
                                                    program_temp+='[]'
                                                program_temp+=';'
                                                temp_ast = parser.parse(program_temp)
                                                update_statements.append(temp_ast.ext[0])
                                            else:
                                                temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
                                                update_statements.append(temp)
			        	
			for statement in statements:
    				update_statements.append(statement)
                        
                        body_comp=c_ast.Compound(block_items=update_statements)
	    		
    			membermethod.setBody(body_comp)
   
    			
    			localvarmap=prog_transform.getVariables(body_comp)
    			
    			for var in externalvarmap.keys():
				variable=externalvarmap[var]
				localvarmap[var]=variable
    			
    			membermethod.setLocalvar(localvarmap)
    			membermethod=functionvarmap[medthod]
    			    			
    			function=[]
    			
    			function.append('-1')
    			
    			function.append('fun')    			
    			
    			functionName=[]
    			
    			allvariable={}
    			
    			for x in membermethod.getInputvar():
				allvariable[x]=membermethod.getInputvar()[x]
			for x in membermethod.getLocalvar():
        			allvariable[x]=membermethod.getLocalvar()[x]
    			if prog_transform.validationOfInput(allvariable)==True:
				print 'Unknown'
				#print "Please Rename variable Name {S,Q,N,in,is} to other Name"
          			return
    			

    			try:
                            
                            program,variablesarray,fname,iputmap,opvariablesarray,module_analysis,module_analysis2=utiles_translation.translate2IntForm(membermethod.getMethodname(),membermethod.getreturnType(),membermethod.getBody(),membermethod.getInputvar(),membermethod.getTempoary(),membermethod.getAnalysis_module(),struct_map)

                        except Exception as e:
                            #print 'Error(error occurred during translation intermediate format)'
                            print 'Unknown'
                            print (str(e))
                        #    print str(e)
                            return
		

			functionName.append(fname)

                        
                        if len(iputmap.keys())>0:
                            for x_i in range(0,len(iputmap.keys())):
                                    functionName.append(iputmap.keys()[len(iputmap.keys())-1-x_i])


			function.append(functionName)
                        
                        
			
			function.append(program)
                        

			programe_array.append(function)
		
			variables_list_map[fname]=variablesarray
			
			addition_array=[]
			
			addition_array.append(iputmap)
			
			addition_array.append(allvariable)
			
			addition_array.append(opvariablesarray)
			
			addition_array_map[fname]=addition_array
			
			memberfunctionmap[fname]=membermethod
                        
                        
			
			function_vfact_list=[]
			function_vfact=[]
			function_vfact.append(fname)
			function_vfact.append(len(iputmap))
			parameters_type=[]
			parameters_type.append(membermethod.getreturnType())
			for x in defineDetaillist:
				function_vfact_list.append(x)
					
			
			defineDetaillist=[]
			for element in iputmap.keys():
				variable=iputmap[element]
				if variable is not None:
					parameters_type.append(variable.getVariableType())
			function_vfact.append(parameters_type)
			function_vfact_list.append(function_vfact)
			function_vfact_map[fname]=function_vfact_list	
                        
                        resultfunction='__VERIFIER_nondet_int'
                        
                        filename=file_name
                        functionname=functionName
                        
                        witnessXml=getWitness(filename,fname,resultfunction)
                        witnessXml_map[fname]= witnessXml
                        
                        
                        
                        if program_analysis is not None:
                            #print '###########################3'
                            #print membermethod.getFun_decl().show()
                            #print '###########################3'
                            program_decl=programPrint(membermethod.getFun_decl())
                            #print '^^^^^^^^^^^^^^^^^^^'
                            #print membermethod.getMethodname()
                            #print membermethod.getreturnType()
                            #print program_decl
                            #print '^^^^^^^^^^^^^^^^^^^'
                            if 'main' not in program_decl:
                                program_analysis_decl+=programPrint(membermethod.getFun_decl())+';\n'
                            module_analysis_t1,module_analysis_t2=module_analysis2
                            program_analysis2=program_decl+programPrint(module_analysis_t1)+program_analysis2
                            program_analysis3=program_decl+programPrint(module_analysis_t2)+program_analysis3
                            program_analysis=program_decl+programPrint(module_analysis)+program_analysis
                            
        
        
        program_analysis=program_analysis_var_decl+program_analysis
        programeIF.append(programe_array)
        
        #print '--------------------------------'
        #print programeIF
        #print '--------------------------------'
        #print variables_list_map
        #print '--------------------------------'
        #return
        
        try:
            f_map,o_map,a_map,cm_map,assert_map,assume_map,assert_key_map=utiles_translation.translate1(programeIF,variables_list_map,1)
            #print a_map
        except Exception as e:
            print 'Error(Translation Failed)'
            writeLogFile( "j2llogs.logs" ,str(e))
            #print str(e)
            return

        #Comment me to use Z3
        #return
        f_list=f_map.keys()
        cycle_list=[]
        programgraph_map=construct_graph(f_map,o_map,a_map,f_list)
        programgraph = graphclass.Graph(programgraph_map)
        

        
        if programgraph.cyclic():
            cycle_list=list(itertools.chain.from_iterable(programgraph.getAllNodesInCycle()))
            

        f_list=removeCycles(f_list,cycle_list)
        

        
        for f_x in cycle_list:
            for x in o_map[f_x]:
                if o_map[f_x][x][0]=='e':
                    o_map[f_x][x][2] = reconstructRecurences(o_map[f_x][x][2],cycle_list)
                    
        for f_x in cycle_list:
            if f_x in fun_call_map.keys() and fun_call_map[f_x]==1:
                for x in o_map['main']:
                    if o_map['main'][x][0]=='e':
                        o_map['main'][x][2] = reconstructRecurences(o_map['main'][x][2],cycle_list)
        


        function_substitution_test('main',programgraph_map,f_map,o_map,a_map,assert_map,assume_map,cycle_list)
