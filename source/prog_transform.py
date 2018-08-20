import sys
import os

currentdirectory = os.path.dirname(os.path.realpath(__file__))

sys.path.append(currentdirectory+"/packages/pyparsing/")
sys.path.append(currentdirectory+"/packages/pycparser1/")
sys.path.append(currentdirectory+"/packages/pycparserext/")
sys.path.append(currentdirectory+"/packages/regex/")
sys.path.append(currentdirectory+"/packages/mpmath/")
sys.path.append(currentdirectory+"/packages/sympy/")


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
from pyparsing import *
from sympy.core.relational import Relational
from pycparser1 import parse_file,c_parser, c_ast, c_generator
from pycparserext.ext_c_parser import GnuCParser
from pycparserext.ext_c_generator import GnuCGenerator
from itertools import permutations




#Get all typedefination

typedef_map={}

def getAllTypeDef(ast):
	global typedef_map
	typedef_map={}
	generator = c_generator.CGenerator()
	for element in ast.ext:
		if type(element) is c_ast.Typedef: 
			if type(element.type.type) is c_ast.Struct:
				program_temp="struct "+ast.ext[0].type.type.name+";"
				temp_ast = parser.parse(program_temp)
				typedef_map[element.name]=generator.visit(temp_ast.ext[0])
			else:
				typedef_map[element.name]=generator.visit(element.type)	
				
				
				
				
				
def updateTypeDef(statement):
	global typedef_map
	parser = c_parser.CParser()
	pointer=None
	array=None
	if type(statement) is c_ast.Decl:
		if type(statement.type) is c_ast.PtrDecl:
			degree=0
    			type_stmt,degree,structType=getArrayDetails(statement,degree)
    			if type_stmt in typedef_map.keys():
				type_stmt=typedef_map[type_stmt]
			program_temp=type_stmt+' '+ statement.name
			for x in range(0,degree):
			    	program_temp+='[]'
    			pointer=statement.name
    			
    			program_temp+=';'
    			temp_ast = parser.parse(program_temp)
    			return temp_ast.ext[0],pointer,array
    		elif type(statement.type) is c_ast.ArrayDecl:
			degree=0
                        dimensionmap={}
    			type_stmt,degree,structType=getArrayDetails(statement,degree,dimensionmap)
			if type_stmt in typedef_map.keys():
				type_stmt=typedef_map[type_stmt]
			program_temp=type_stmt+' '+statement.name
			for x in range(0,degree):
				program_temp+='[]'
			program_temp+=';'
			array=statement.name
			temp_ast = parser.parse(program_temp)
    			#return temp_ast.ext[0],pointer,array
                        return statement,pointer,array
    		else:
    			type_stmt= statement.type.type.names[0]
    			if type_stmt in typedef_map.keys():
				type_stmt=typedef_map[type_stmt]
			program_temp=type_stmt+' '+ statement.name
			generator = c_generator.CGenerator()
			if statement.init is not None:
				value=generator.visit(statement.init)
				if value is not None:
					program_temp+='='+value
			program_temp+=';'
			temp_ast = parser.parse(program_temp)
    			return temp_ast.ext[0],pointer,array
	return None,pointer,array




def pointerHandlingParameter(ast):

	if type(ast) is c_ast.FuncDef:
		pointer_list=[]
		array_list=[]
		new_stmts=[]
		new_parameters=''
		generator = c_generator.CGenerator()
		parser = c_parser.CParser()
		if ast.decl.type.args is not None:
			parameters=ast.decl.type.args.params
			if parameters is not None:
				for parameter in parameters:
					if new_parameters=='':
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters=generator.visit(type_decl)
					else:
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters+=','+generator.visit(type_decl)
		return_type=generator.visit(ast.decl.type.type)
		function_name=ast.decl.name
    		new_fun=return_type+' '+ function_name+'('+ new_parameters +'){}'
    		new_fun=parser.parse(new_fun)
    		return new_fun.ext[0].decl,pointer_list,array_list
	else:
		return None,[],[]


def pointerHandlingDecl(function_body,pointer_list,array_list):
	update_statements=[]
	statements=function_body.block_items
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			new_stmt=None
			if pointer is not None:
				if statement.init is not None:
					if type(statement.init) is c_ast.InitList:
						new_statement=None
						new_stmt=None
					else:
						new_stmt=c_ast.Assignment(op='=', lvalue=c_ast.ID(name=pointer), rvalue=ref2function(statement.init))
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
				if new_stmt is not None:
					update_statements.append(new_stmt)
			else:
				update_statements.append(statement)
		else:
			update_statements.append(statement)
	fun_body=c_ast.Compound(block_items=update_statements)
	return fun_body
	




def pointerHandling(statements,pointer_list,array_list):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			if pointer is not None:
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
			else:
				update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(pointerHandlingIf(statement,pointer_list,array_list))
		elif type(statement) is c_ast.While:
			if statement.stmt.block_items is not None:
                		update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=pointerHandling(statement.stmt.block_items,pointer_list,array_list))))
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=defref2function(statement.lvalue,pointer_list,array_list),rvalue=defref2function(statement.rvalue,pointer_list,array_list)))
		else:
			update_statements.append(statement)
	return update_statements
	


	
def pointerHandlingIf(statement,pointer_list,array_list):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=defref2function(statement.iftrue.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iftrue.rvalue,pointer_list,array_list))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=pointerHandling(statement.iftrue.block_items,pointer_list,array_list)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iftrue=c_ast.Assignment(op=statement.iffalse.op,lvalue=defref2function(statement.iffalse.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iffalse.rvalue,pointer_list,array_list))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=pointerHandling(statement.iffalse.block_items,pointer_list,array_list)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=pointerHandlingIf(statement.iffalse,pointer_list,array_list)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
def pointerHandlingParameter(ast):

	if type(ast) is c_ast.FuncDef:
		pointer_list=[]
		array_list=[]
		new_stmts=[]
		new_parameters=''
		generator = c_generator.CGenerator()
		parser = c_parser.CParser()
		if ast.decl.type.args is not None:
			parameters=ast.decl.type.args.params
			if parameters is not None:
				for parameter in parameters:
					if new_parameters=='':
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters=generator.visit(type_decl)
					else:
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters+=','+generator.visit(type_decl)
		return_type=generator.visit(ast.decl.type.type)
		function_name=ast.decl.name
    		new_fun=return_type+' '+ function_name+'('+ new_parameters +'){}'
    		new_fun=parser.parse(new_fun)
    		return new_fun.ext[0].decl,pointer_list,array_list
	else:
		return None,[],[]


def pointerHandlingDecl(function_body,pointer_list,array_list):
	update_statements=[]
	statements=function_body.block_items
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			new_stmt=None
			if pointer is not None:
				if statement.init is not None:
					if type(statement.init) is c_ast.InitList:
						new_statement=None
						new_stmt=None
					else:
						new_stmt=c_ast.Assignment(op='=', lvalue=c_ast.ID(name=pointer), rvalue=ref2function(statement.init))
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
				if new_stmt is not None:
					update_statements.append(new_stmt)
			else:
				update_statements.append(statement)
		else:
			update_statements.append(statement)
	fun_body=c_ast.Compound(block_items=update_statements)
	return fun_body
	




def pointerHandling(statements,pointer_list,array_list):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			if pointer is not None:
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
			else:
				update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(pointerHandlingIf(statement,pointer_list,array_list))
		elif type(statement) is c_ast.While:
			if statement.stmt.block_items is not None:
                		update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=pointerHandling(statement.stmt.block_items,pointer_list,array_list))))
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=defref2function(statement.lvalue,pointer_list,array_list),rvalue=defref2function(statement.rvalue,pointer_list,array_list)))
		else:
			update_statements.append(statement)
	return update_statements
	


	
def pointerHandlingIf(statement,pointer_list,array_list):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=defref2function(statement.iftrue.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iftrue.rvalue,pointer_list,array_list))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=pointerHandling(statement.iftrue.block_items,pointer_list,array_list)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iftrue=c_ast.Assignment(op=statement.iffalse.op,lvalue=defref2function(statement.iffalse.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iffalse.rvalue,pointer_list,array_list))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=pointerHandling(statement.iffalse.block_items,pointer_list,array_list)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=pointerHandlingIf(statement.iffalse,pointer_list,array_list)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
def pointerHandlingParameter(ast):

	if type(ast) is c_ast.FuncDef:
		pointer_list=[]
		array_list=[]
		new_stmts=[]
		new_parameters=''
		generator = c_generator.CGenerator()
		parser = c_parser.CParser()
		if ast.decl.type.args is not None:
			parameters=ast.decl.type.args.params
			if parameters is not None:
				for parameter in parameters:
					if new_parameters=='':
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters=generator.visit(type_decl)
					else:
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters+=','+generator.visit(type_decl)
		return_type=generator.visit(ast.decl.type.type)
		function_name=ast.decl.name
    		new_fun=return_type+' '+ function_name+'('+ new_parameters +'){}'
    		new_fun=parser.parse(new_fun)
    		return new_fun.ext[0].decl,pointer_list,array_list
	else:
		return None,[],[]


def pointerHandlingDecl(function_body,pointer_list,array_list):
	update_statements=[]
	statements=function_body.block_items
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			new_stmt=None
			if pointer is not None:
				if statement.init is not None:
					if type(statement.init) is c_ast.InitList:
						new_statement=None
						new_stmt=None
					else:
						new_stmt=c_ast.Assignment(op='=', lvalue=c_ast.ID(name=pointer), rvalue=ref2function(statement.init))
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
				if new_stmt is not None:
					update_statements.append(new_stmt)
			else:
				update_statements.append(statement)
		else:
			update_statements.append(statement)
	fun_body=c_ast.Compound(block_items=update_statements)
	return fun_body
	




def pointerHandling(statements,pointer_list,array_list):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			if pointer is not None:
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
			else:
				update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(pointerHandlingIf(statement,pointer_list,array_list))
		elif type(statement) is c_ast.While:
			if statement.stmt.block_items is not None:
                		update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=pointerHandling(statement.stmt.block_items,pointer_list,array_list))))
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=defref2function(statement.lvalue,pointer_list,array_list),rvalue=defref2function(statement.rvalue,pointer_list,array_list)))
		else:
			update_statements.append(statement)
	return update_statements
	


	
def pointerHandlingIf(statement,pointer_list,array_list):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=defref2function(statement.iftrue.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iftrue.rvalue,pointer_list,array_list))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=pointerHandling(statement.iftrue.block_items,pointer_list,array_list)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iftrue=c_ast.Assignment(op=statement.iffalse.op,lvalue=defref2function(statement.iffalse.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iffalse.rvalue,pointer_list,array_list))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=pointerHandling(statement.iffalse.block_items,pointer_list,array_list)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=pointerHandlingIf(statement.iffalse,pointer_list,array_list)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
def pointerHandlingParameter(ast):

	if type(ast) is c_ast.FuncDef:
		pointer_list=[]
		array_list=[]
		new_stmts=[]
		new_parameters=''
		generator = c_generator.CGenerator()
		parser = c_parser.CParser()
		if ast.decl.type.args is not None:
			parameters=ast.decl.type.args.params
			if parameters is not None:
				for parameter in parameters:
					if new_parameters=='':
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters=generator.visit(type_decl)
					else:
						type_decl,pointer,array=updateTypeDef(parameter)
						if pointer is not None:
							pointer_list.append(pointer)
						if array is not None:
							array_list.append(array)
						new_parameters+=','+generator.visit(type_decl)
		return_type=generator.visit(ast.decl.type.type)
		function_name=ast.decl.name
    		new_fun=return_type+' '+ function_name+'('+ new_parameters +'){}'
    		new_fun=parser.parse(new_fun)
    		return new_fun.ext[0].decl,pointer_list,array_list
	else:
		return None,[],[]


def pointerHandlingDecl(function_body,pointer_list,array_list):
	update_statements=[]
	statements=function_body.block_items
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			new_stmt=None
			if pointer is not None:
				if statement.init is not None:
					if type(statement.init) is c_ast.InitList:
						new_statement=None
						new_stmt=None
					else:
						new_stmt=c_ast.Assignment(op='=', lvalue=c_ast.ID(name=pointer), rvalue=ref2function(statement.init))
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
				if new_stmt is not None:
					update_statements.append(new_stmt)
			else:
				update_statements.append(statement)
		else:
			update_statements.append(statement)
	fun_body=c_ast.Compound(block_items=update_statements)
	return fun_body
	




def pointerHandling(statements,pointer_list,array_list):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			new_statement,pointer,array=updateTypeDef(statement)
			if pointer is not None:
				pointer_list.append(pointer)
			if array is not None:
				array_list.append(array)
			if new_statement is not None:
				update_statements.append(new_statement)
			else:
				update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(pointerHandlingIf(statement,pointer_list,array_list))
		elif type(statement) is c_ast.While:
			if statement.stmt.block_items is not None:
                		update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=pointerHandling(statement.stmt.block_items,pointer_list,array_list))))
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=defref2function(statement.lvalue,pointer_list,array_list),rvalue=defref2function(statement.rvalue,pointer_list,array_list)))
		else:
			update_statements.append(statement)
	return update_statements
	


	
def pointerHandlingIf(statement,pointer_list,array_list):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=defref2function(statement.iftrue.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iftrue.rvalue,pointer_list,array_list))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=pointerHandling(statement.iftrue.block_items,pointer_list,array_list)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iftrue=c_ast.Assignment(op=statement.iffalse.op,lvalue=defref2function(statement.iffalse.lvalue,pointer_list,array_list),rvalue=defref2function(statement.iffalse.rvalue,pointer_list,array_list))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=pointerHandling(statement.iffalse.block_items,pointer_list,array_list)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=pointerHandlingIf(statement.iffalse,pointer_list,array_list)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)





def change_var_name(statements):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			if type(statement.type) is c_ast.ArrayDecl:
                                if checkingArrayName(statement.type)==True:
                                    statement=c_ast.Decl(name=statement.name+'_var', quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=renameArrayName(statement.type), init=statement.init, bitsize=statement.bitsize)
                                statement.type.dim=change_var_name_stmt(statement.type.dim)
			else:
                            if type(statement.type) is not c_ast.PtrDecl:
				if fun_utiles.is_number(statement.type.declname[-1])==True:
					statement=c_ast.Decl(name=statement.name+'_var', quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type), init=statement.init, bitsize=statement.bitsize)
				elif statement.type.declname in ['S','Q','N','in','is','limit']:
					statement=c_ast.Decl(name=statement.name+'_var', quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type), init=statement.init, bitsize=statement.bitsize)
			update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(change_var_nameIf(statement))
		elif type(statement) is c_ast.While:
                        if type(statement.stmt) is c_ast.Assignment:
                                new_block=[]
                                new_block.append(statement.stmt)
                                update_statements.append(c_ast.While(cond=change_var_name_stmt(statement.cond),stmt=c_ast.Compound(block_items=change_var_name(new_block))))
                        elif type(statement.stmt) is c_ast.UnaryOp:
                                new_block=[]
                                new_block.append(statement.stmt)
                                update_statements.append(c_ast.While(cond=change_var_name_stmt(statement.cond),stmt=c_ast.Compound(block_items=change_var_name(new_block))))
			elif statement.stmt.block_items is not None:
				update_statements.append(c_ast.While(cond=change_var_name_stmt(statement.cond),stmt=c_ast.Compound(block_items=change_var_name(statement.stmt.block_items))))	
			else:
				update_statements.append(c_ast.While(cond=change_var_name_stmt(statement.cond),stmt=c_ast.Compound(block_items=statement.stmt.block_items)))	
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=change_var_name_stmt(statement.lvalue),rvalue=change_var_name_stmt(statement.rvalue)))
		elif type(statement) is c_ast.Return:
                    statement.expr=change_var_name_stmt(statement.expr)
                    update_statements.append(statement)
                    #Return: [expr*]
		else:
			update_statements.append(statement)
	return update_statements
	


	
def change_var_nameIf(statement):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=change_var_name_stmt(statement.iftrue.lvalue),rvalue=change_var_name_stmt(statement.iftrue.rvalue))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=change_var_name(statement.iftrue.block_items)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iffalse=c_ast.Assignment(op=statement.iffalse.op,lvalue=change_var_name_stmt(statement.iffalse.lvalue),rvalue=change_var_name_stmt(statement.iffalse.rvalue))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=change_var_name(statement.iffalse.block_items)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=change_var_nameIf(statement.iffalse)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond= change_var_name_stmt(statement.cond), iftrue=new_iftrue, iffalse=new_iffalse)


def change_var_name_stmt(statement):
	if type(statement) is c_ast.BinaryOp:
		if type(statement.left) is c_ast.ID:
			if fun_utiles.is_number(statement.left.name[-1])==True:
				stmt_left=c_ast.ID(name=statement.left.name+'_var')
			elif statement.left.name in ['S','Q','N','in','is','limit']:
				stmt_left=c_ast.ID(name=statement.left.name+'_var')
			else:
				stmt_left=change_var_name_stmt(statement.left)
		else:
			stmt_left=change_var_name_stmt(statement.left)
		
		if type(statement.right) is c_ast.ID:
			if fun_utiles.is_number(statement.right.name[-1])==True:
				stmt_right=c_ast.ID(name=statement.right.name+'_var')
			elif statement.right.name in ['S','Q','N','in','is','limit']:
				stmt_right=c_ast.ID(name=statement.right.name+'_var')
			else:
				stmt_right=change_var_name_stmt(statement.right)
		else:
			stmt_right=change_var_name_stmt(statement.right)
		return c_ast.BinaryOp(op=statement.op, left=stmt_left, right=stmt_right)
	elif type(statement) is c_ast.UnaryOp:
		if type(statement.expr) is c_ast.ID:
			if fun_utiles.is_number(statement.expr.name[-1])==True:
				stmt=c_ast.ID(name=statement.expr.name+'_var')
			elif statement.expr.name in ['S','Q','N','in','is','limit']:
				stmt=c_ast.ID(name=statement.expr.name+'_var')
			else:
				stmt=change_var_name_stmt(statement.expr)
		else:
			stmt=change_var_name_stmt(statement.expr)
		return c_ast.UnaryOp(op=statement.op, expr=stmt)
	elif type(statement) is c_ast.ID:
		if fun_utiles.is_number(statement.name[-1])==True:
			return c_ast.ID(name=statement.name+'_var')
		elif statement.name in ['S','Q','N','in','is','limit']:
			return c_ast.ID(name=statement.name+'_var')
		else:
                        return statement
        elif type(statement) is c_ast.FuncCall:
            if statement.args is not None:
                new_expr=[]
                for exp in statement.args.exprs:
                    new_expr.append(change_var_name_stmt(exp))
                return c_ast.FuncCall(name=statement.name,args=c_ast.ExprList(exprs=new_expr))
            else:
                return statement
	
	else:
		if type(statement) is c_ast.ArrayRef:
                    return renameArrayName(statement)
                    #if checkingArrayName(statement)==True:
                    #    return renameArrayName(statement)
                    #else:
                    #    return statement
                elif type(statement) is c_ast.StructRef:
                    return c_ast.StructRef(name=change_var_name_stmt(statement.name),type=change_var_name_stmt(statement.type),field=statement.field)
                else:
                    return statement











def change_var_name_decl(statement):
    if type(statement) is c_ast.Decl:
        if type(statement.type) is c_ast.ArrayDecl:
            if fun_utiles.is_number(statement.name[-1])==True:
                statement.name=statement.name+'_var'
                renameArrayName(statement.type)
            elif statement.name in ['S','Q','N','in','is','limit']:
                statement.name=statement.name+'_var'
                renameArrayName(statement.type)
            else:
                statement.type.dim=change_var_name_stmt(statement.type.dim)
        else:
            if fun_utiles.is_number(statement.type.declname[-1])==True:
                statement.name=statement.name+'_var' 
                statement.type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type)
            elif statement.type.declname in ['S','Q','N','in','is','limit']:
                statement.name=statement.name+'_var'  
                statement.type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type)
        return statement
    return statement




def checkingArrayNameStmt(statement):
    if type(statement) is c_ast.BinaryOp:
        if checkingArrayNameStmt(statement.left)==True:
            return True
        if checkingArrayNameStmt(statement.right)==True:
            return True
    elif type(statement) is c_ast.UnaryOp:
        if checkingArrayNameStmt(statement.expr)==True:
            return True
    elif type(statement) is c_ast.ID:
        if is_number(statement.name[-1])==True:
            return True
        elif statement.name in ['S','Q','N','in','is']:
            return True
    else:
        return True


            
def renameArrayName(statement):
    if type(statement) is c_ast.ArrayDecl:
        if type(statement.type) is c_ast.TypeDecl:
            if is_number(statement.type.declname[-1])==True:
                statement=c_ast.ArrayDecl(type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type),dim=change_var_name_stmt(statement.dim), dim_quals=statement.dim_quals)
                return statement
            elif statement.type.declname in ['S','Q','N','in','is']:
                statement=c_ast.ArrayDecl(type=c_ast.TypeDecl(declname=statement.type.declname+'_var', quals=statement.type.quals, type=statement.type.type),dim=change_var_name_stmt(statement.dim), dim_quals=statement.dim_quals)
                return statement
            else:
                return statement
        elif type(statement.type) is c_ast.ArrayDecl:
            statement=c_ast.ArrayDecl(type=renameArrayName(statement.type),dim=change_var_name_stmt(statement.type.dim), dim_quals=statement.type.dim_quals)
            return statement
    elif type(statement) is c_ast.ArrayRef:
        if type(statement.name) is c_ast.ID:
            if is_number(statement.name.name[-1])==True:
                return c_ast.ArrayRef(name=c_ast.ID(name=statement.name.name+'_var'),subscript=change_var_name_stmt(statement.subscript))
            elif statement.name.name in ['S','Q','N','in','is']:
                return c_ast.ArrayRef(name=c_ast.ID(name=statement.name.name+'_var'),subscript=change_var_name_stmt(statement.subscript))
            else:
                return c_ast.ArrayRef(name=c_ast.ID(name=statement.name.name),subscript=change_var_name_stmt(statement.subscript))
        elif type(statement.name) is c_ast.ArrayRef:
            return c_ast.ArrayRef(name=renameArrayName(statement.name),subscript=change_var_name_stmt(statement.subscript))














def update_var_name(statements,pre_fix):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.Decl:
			if type(statement.type) is c_ast.ArrayDecl:
                                statement=c_ast.Decl(name=pre_fix+'_'+statement.name, quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=updateArrayName(statement.type), init=statement.init, bitsize=statement.bitsize)
                                statement.type.dim=update_var_name_stmt(statement.type.dim,pre_fix)
			else:
                            if type(statement.type) is not c_ast.PtrDecl:
                                statement=c_ast.Decl(name=pre_fix+'_'+statement.name, quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=c_ast.TypeDecl(declname=pre_fix+'_'+statement.type.declname, quals=statement.type.quals, type=statement.type.type), init=statement.init, bitsize=statement.bitsize)
			update_statements.append(statement)
		elif type(statement) is c_ast.If:
			update_statements.append(update_var_nameIf(statement,pre_fix))
		elif type(statement) is c_ast.While:
                        if type(statement.stmt) is c_ast.Assignment:
                                new_block=[]
                                new_block.append(statement.stmt)
                                update_statements.append(c_ast.While(cond=update_var_name_stmt(statement.cond,pre_fix),stmt=c_ast.Compound(block_items=update_var_name(new_block,pre_fix))))
                        elif type(statement.stmt) is c_ast.UnaryOp:
                                new_block=[]
                                new_block.append(statement.stmt)
                                update_statements.append(c_ast.While(cond=update_var_name_stmt(statement.cond,pre_fix),stmt=c_ast.Compound(block_items=update_var_name(new_block,pre_fix))))
			elif statement.stmt.block_items is not None:
				update_statements.append(c_ast.While(cond=update_var_name_stmt(statement.cond,pre_fix),stmt=c_ast.Compound(block_items=update_var_name(statement.stmt.block_items,pre_fix))))	
			else:
				update_statements.append(c_ast.While(cond=update_var_name_stmt(statement.cond,pre_fix),stmt=c_ast.Compound(block_items=statement.stmt.block_items)))	
		elif type(statement) is c_ast.Assignment:
			update_statements.append(c_ast.Assignment(op=statement.op,lvalue=update_var_name_stmt(statement.lvalue,pre_fix),rvalue=update_var_name_stmt(statement.rvalue,pre_fix)))
		elif type(statement) is c_ast.Return:
                    statement.expr=update_var_name_stmt(statement.expr,pre_fix)
                    update_statements.append(statement)
                    #Return: [expr*]
                elif type(statement) is c_ast.FuncCall:
                    if statement.args is not None:
                        new_expr=[]
                        for exp in statement.args.exprs:
                            new_expr.append(update_var_name_stmt(exp,pre_fix))
                        update_statements.append(c_ast.FuncCall(name=statement.name,args=c_ast.ExprList(exprs=new_expr)))

		else:
                    update_statements.append(statement)
	return update_statements
	


	
def update_var_nameIf(statement,pre_fix):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Assignment:
        	new_iftrue=c_ast.Assignment(op=statement.iftrue.op,lvalue=update_var_name_stmt(statement.iftrue.lvalue,pre_fix),rvalue=update_var_name_stmt(statement.iftrue.rvalue,pre_fix))
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=update_var_name(statement.iftrue.block_items,pre_fix)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
       
       
        if type(statement.iffalse) is c_ast.Assignment:
		new_iffalse=c_ast.Assignment(op=statement.iffalse.op,lvalue=change_var_name_stmt(statement.iffalse.lvalue,pre_fix),rvalue=update_var_name_stmt(statement.iffalse.rvalue,pre_fix))
	elif type(statement.iffalse) is c_ast.Compound:
		if statement.iffalse.block_items is not None:
	        	new_block_items=update_var_name(statement.iffalse.block_items,pre_fix)
	                new_iffalse=c_ast.Compound(block_items=new_block_items)
	        else:
	                new_iffalse=statement.iffalse
	elif type(statement.iffalse) is c_ast.If:
		new_iffalse=update_var_nameIf(statement.iffalse,pre_fix)
	else:
        	new_iffalse=statement.iffalse
        	
    return c_ast.If(cond= update_var_name_stmt(statement.cond,pre_fix), iftrue=new_iftrue, iffalse=new_iffalse)


def update_var_name_stmt(statement,pre_fix):
	if type(statement) is c_ast.BinaryOp:
		if type(statement.left) is c_ast.ID:
                        stmt_left=c_ast.ID(name=pre_fix+'_'+statement.left.name)
		else:
			stmt_left=update_var_name_stmt(statement.left,pre_fix)
		
		if type(statement.right) is c_ast.ID:
                        stmt_right=c_ast.ID(name=pre_fix+'_'+statement.right.name)
		else:
			stmt_right=update_var_name_stmt(statement.right,pre_fix)
                        
		return c_ast.BinaryOp(op=statement.op, left=stmt_left, right=stmt_right)
                
	elif type(statement) is c_ast.UnaryOp:
            
		if type(statement.expr) is c_ast.ID:
                        stmt=c_ast.ID(name=pre_fix+'_'+statement.expr.name)
		else:
			stmt=update_var_name_stmt(statement.expr,pre_fix)
                        
		return c_ast.UnaryOp(op=statement.op, expr=stmt)
	elif type(statement) is c_ast.ID:
            
                return c_ast.ID(name=pre_fix+'_'+statement.name)
                
        elif type(statement) is c_ast.FuncCall:
            if statement.args is not None:
                new_expr=[]
                for exp in statement.args.exprs:
                    new_expr.append(update_var_name_stmt(exp,pre_fix))
                return c_ast.FuncCall(name=statement.name,args=c_ast.ExprList(exprs=new_expr))
            else:
                return statement
	
	else:
		if type(statement) is c_ast.ArrayRef:
                    return updateArrayName(statement,pre_fix)
                elif type(statement) is c_ast.StructRef:
                    return c_ast.StructRef(name=update_var_name_stmt(statement.name,pre_fix),type=update_var_name_stmt(statement.type,pre_fix),field=statement.field)
                else:
                    return statement




def updateArrayName(statement,pre_fix):
    if type(statement) is c_ast.ArrayDecl:
        if type(statement.type) is c_ast.TypeDecl:
            statement=c_ast.ArrayDecl(type=c_ast.TypeDecl(declname=pre_fix+'_'+statement.type.declname, quals=statement.type.quals, type=statement.type.type),dim=update_var_name_stmt(statement.dim), dim_quals=statement.dim_quals)
            return statement
        elif type(statement.type) is c_ast.ArrayDecl:
            statement=c_ast.ArrayDecl(type=updateArrayName(statement.type,pre_fix),dim=update_var_name_stmt(statement.type.dim), dim_quals=statement.type.dim_quals)
            return statement
    elif type(statement) is c_ast.ArrayRef:
        if type(statement.name) is c_ast.ID:
            return c_ast.ArrayRef(name=c_ast.ID(name=pre_fix+'_'+statement.name.name),subscript=update_var_name_stmt(statement.subscript,pre_fix))
        elif type(statement.name) is c_ast.ArrayRef:
            return c_ast.ArrayRef(name=updateArrayName(statement.name,pre_fix),subscript=update_var_name_stmt(statement.subscript,pre_fix))







def update_var_name_decl(statement,pre_fix):
    if type(statement) is c_ast.Decl:
        if type(statement.type) is c_ast.ArrayDecl:
            statement.name=pre_fix+'_'+statement.name
            renameArrayName(statement.type)
            statement.type.dim=update_var_name_stmt(statement.type.dim)
        else:
            statement.name=pre_fix+'_'+statement.name 
            statement.type=c_ast.TypeDecl(declname=pre_fix+'_'+statement.type.declname, quals=statement.type.quals, type=statement.type.type)
        return statement
    return statement









"""

Validation of Variables

"""

def validationOfInput(allvariable):
	for variable in allvariable.keys():
		if variable=='S' or variable=='Q' or variable=='N' or variable=='in' or variable=='is':
			return True
	return False
























def getVariables(function_body):
    #statements=handlingPointer(function_body.block_items)
    statements=function_body.block_items
    #for decl in function_body.block_items:
    return getVariablesC(statements)


#Get Variable 

def getVariablesC(statements):
    localvarmap={}
    if statements is None:
        return localvarmap
    for decl in statements:
        if type(decl) is c_ast.Decl:
            var_type=None
            initial_value=None
            structType=None
            if type(decl.type) is c_ast.ArrayDecl:
                #if checkingArrayName(decl.type)==True:
                if fun_utiles.is_number(decl.name[-1])==True:
                    decl=c_ast.Decl(name=decl.name+'_var', quals=decl.quals, storage=decl.storage, funcspec=decl.funcspec, type=renameArrayName(decl.type), init=decl.init, bitsize=decl.bitsize)
                elif decl.name in ['S','Q','N','in','is']:
                    decl=c_ast.Decl(name=decl.name+'_var', quals=decl.quals, storage=decl.storage, funcspec=decl.funcspec, type=renameArrayName(decl.type), init=decl.init, bitsize=decl.bitsize)
            elif type(decl.type) is c_ast.PtrDecl:
                if type(decl.type.type) is c_ast.TypeDecl:
                    if fun_utiles.is_number(decl.type.type.declname[-1])==True:
                        decl.type.type=c_ast.TypeDecl(decl.type.type.declname+'_var', quals=decl.type.type.quals, type=decl.type.type.type)
                    elif decl.name in ['S','Q','N','in','is']:
                        decl.type.type=c_ast.TypeDecl(decl.type.type.declname+'_var', quals=decl.type.type.quals, type=decl.type.type.type)
            else:
                if fun_utiles.is_number(decl.type.declname[-1])==True :
                    decl=c_ast.Decl(name=decl.name+'_var', quals=decl.quals, storage=decl.storage, funcspec=decl.funcspec, type=c_ast.TypeDecl(declname=decl.type.declname+'_var', quals=decl.type.quals, type=decl.type.type), init=decl.init, bitsize=decl.bitsize)


            if type(decl.type) is c_ast.ArrayDecl:
            	degree=0
                dimensionmap={}
	    	var_type,degree,structType=getArrayDetails(decl,degree,dimensionmap)
		variable=list_class.variableclass(decl.name, var_type,None,dimensionmap,initial_value,structType)
	    elif type(decl.type) is c_ast.PtrDecl:
                degree=0
                dimensionmap={}
	    	var_type,degree,structType=getArrayDetails(decl,degree,dimensionmap)
		variable=list_class.variableclass(decl.name, var_type,'Pointer',dimensionmap,initial_value,structType)
	    else:
            	for child in decl.children():
            		if type(child[1]) is c_ast.TypeDecl:
                		if type(child[1].type) is c_ast.IdentifierType:
                    			var_type=child[1].type.names[0]
				else:
					if type(child[1].type) is c_ast.Struct:
						structType=child[1].type.name
                                                var_type=child[1].type.name
					else:
                    				initial_value=child[1].value
                    	else:
                    		if type(child[1]) is c_ast.FuncCall:
			    		parameter=''
					if child[1].args is not None:
			    			for param in child[1].args.exprs:
			    				if type(param) is c_ast.ID:
			    					if parameter=='':
					        			parameter = "expres('"+param.name+"')"
					        		else:
					        			parameter += ",expres('"+param.name+"')"
			    				elif type(param) is c_ast.Constant:
			    		    			if parameter=='':
									parameter = "expres('"+param.value+"')"
								else:
					        			parameter += ",expres('"+param.value+"')"
							else:
								if type(statement) is c_ast.ArrayRef:
									degree=0
									stmt,degree=createArrayList_C(statement,degree)
								    	if parameter=='':
										parameter = "expres('d"+str(degree)+'array'+"',["+stmt+"])"
									else:
		        							parameter += ","+"expres('d"+str(degree)+'array'+"',["+stmt+"])"
						#initial_value="['"+child[1].name.name+"',"+parameter+"]"
						initial_value="['"+child[1].name.name+"',"+parameter+"]"
					else:
						#initial_value="expres('"+child[1].name.name+"'"+")"
						initial_value=child[1].name.name
				else:
					if type(child[1]) is c_ast.Constant:
						initial_value=child[1].value
                                        elif type(child[1]) is c_ast.ID:
						initial_value=child[1].name
					else:
                                                #print expressionCreator_C(child[1])
						initial_value=child[1]
            	variable=list_class.variableclass(decl.name, var_type,None,None,initial_value,structType)
            localvarmap[decl.name]=variable
        elif type(decl) is c_ast.While:
        	localvarmap_temp=getVariablesC(decl.stmt.block_items)
        	for var in localvarmap_temp.keys():
        		localvarmap[var]=localvarmap_temp[var]
        elif type(decl) is c_ast.If:
        	localvarmap_temp=getVariablesC_If(decl)
        	for var in localvarmap_temp.keys():
        		localvarmap[var]=localvarmap_temp[var]
    return localvarmap


def getVariablesC_If(statement):
	localvarmap={}
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			localvarmap_temp=getVariablesC(statement.iftrue.block_items)
		        for var in localvarmap_temp.keys():
        			localvarmap[var]=localvarmap_temp[var]				
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				localvarmap_temp=getVariablesC(statement.iffalse.block_items)
				for var in localvarmap_temp.keys():
        				localvarmap[var]=localvarmap_temp[var]	
		else:
			if type(statement.iffalse) is c_ast.If:
				localvarmap_temp=getVariablesC_If(statement.iffalse)
				for var in localvarmap_temp.keys():
        				localvarmap[var]=localvarmap_temp[var]	
	return localvarmap
def declarationModifying(statement):
    if type(statement.type) is c_ast.PtrDecl:
        degree=0
        parser = c_parser.CParser()
        type_stmt,degree,structType=getArrayDetails(statement,degree)
        program_temp=type_stmt+' '+ statement.name
        for x in range(0,degree):
            program_temp+='[]'
        pointer=statement.name
        program_temp+=';'
        temp_ast = parser.parse(program_temp)
        return temp_ast.ext[0]
    else:
        return None




def list_all_global_var():
    
    global counter_variableMap
    global counter_variableMap_Conf
    global fail_count
    global error_count
    global assume_count
    global assert_count


    counter_variableMap={}
    
    counter_variableMap_Conf={}
 
   
    fail_count=0
    error_count=0
    assume_count=0
    assert_count=0



def programTransformation(function_body,functionMap,medthodname):

    generator = c_generator.CGenerator()   
   
    global break_count
    global continue_count
    global new_variable
    global dummyCount
    global count__VERIFIER_nondet
    
    new_variable={}
    
 
        
    #Handling Pointer
    
    #print '#######'
    #print(generator.visit(function_body))
    #print '#######'
    
    
    #statements= handlingPointer(function_body.block_items)
    
    #function_body.show()
    
    statements=function_body.block_items
        
    #Syntax translation of the function body
    
    #print '#######1'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######1'
        
    statements=syntaxTranslate(statements)

    #print '#######1'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######1'

    statements=arrangeEmptyStatement(statements)
    #print '#######11'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######11'
   
    #Convert Initiation to assignments   
    
    statements=construct_program(statements)
    
    
    statements=reconstructPreDefinedFun(statements)
    
    
    #pa_update_statements = organizeDeclaration(pa_update_statements)
    
    #pa_update_statements = getVariablesInit(pa_update_statements)
    
    
    
    
    
    #print '#######3'
    #print(generator.visit(c_ast.Compound(block_items=pa_update_statements)))
    #print '#######3'
    
    #print '#######3'
    #print(generator.visit(c_ast.Compound(block_items=pa_update_statements)))
    #print '#######3'
        
    #Replace return by goto statement
        
    statements=remove_return(statements,functionMap[medthodname])
    
    #print '#######4'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######4'
    
        
    #Replace goto structured statement
        
    statements=gotoremoval(statements)
    
    #print '#######5'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######5'
        
    update_statements=[]
        
    #Add new variable
        
    for var in new_variable.keys():
    	if fun_utiles.isBoolVariable( var )==True:
    	    	#temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['_Bool'])), init=c_ast.Constant(type='_Bool', value=None), bitsize=None)
                temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
    		update_statements.append(temp)
    	else:
    		temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
    		update_statements.append(temp)
        	
    for statement in statements:
    	update_statements.append(statement)
        	
    #print '#######6'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######6' 
      
      
    #Remove Empty If Loops  
    
    update_statements=removeEmptyIfLoop(update_statements)
        
    #Remove Dead Code
    
    #print '#######6'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######6'
    
    
    update_statements=removeDeadCode(update_statements)
    
    
    #print '#######7'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######7'
        
    #Simplify Conditions
        
    statements=simplifyProgram(update_statements)
    
    
    #print '#######8'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######8'
    
    #Add Break Removal Modules
    
    
    break_map={}
    break_count=0
    continue_count=0
    
    statements=getBreakStmt(statements,break_map)
    
    #print '#######9'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######9'
    
    
    statements=changeConditionProgram(statements)
    
    
    #print '#######10'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######10'
    
        
    update_statements=[]
    
    for var in new_variable.keys():
    	if fun_utiles.isBoolVariable( var )==True:
    	    	#temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['_Bool'])), init=c_ast.Constant(type='_Bool', value=None), bitsize=None)
                temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
       		update_statements.append(temp)
    	else:
    		temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
       		update_statements.append(temp)
        	
    for statement in statements:
    	update_statements.append(statement)
    
    dummyCount=0
    
    #print '#######10'
    #print(generator.visit(c_ast.Compound(block_items=update_statements)))
    #print '#######10'
    
    
    statements=functionToAssignment(update_statements,functionMap)
    
    
    
    
    #print '#######11'
    #print(generator.visit(c_ast.Compound(block_items=statements)))
    #print '#######11'
       
    update_statements=[]
    
    if dummyCount>0:
    	for x in range(0, dummyCount):
    		temp=c_ast.Decl(name='_'+str(x+1)+'DUMMY', quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname='_'+str(x+1)+'DUMMY', quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
       		update_statements.append(temp)
    for statement in statements:
    	update_statements.append(statement)
        
    #count__VERIFIER_nondet=0
    
    update_statements=getVariablesInit(update_statements)
    
    update_statements=change_var_name(update_statements)
    
    

    return update_statements







"""
 
Translate Syntax Code 
 
"""
 

"""

Syntax translation module

"""



def syntaxTranslate(statements):
        update_statements=[]
        for statement in statements:
                if type(statement) is c_ast.UnaryOp:
                        
                        if statement.op=='++' or statement.op=='p++':
                                update_statements.append(c_ast.Assignment(op='=',lvalue=statement.expr, rvalue=c_ast.BinaryOp(op='+',left=statement.expr, right=c_ast.Constant('int','1'))))
                        elif statement.op=='--' or statement.op=='p--':
                                update_statements.append(c_ast.Assignment(op='=',lvalue=statement.expr, rvalue=c_ast.BinaryOp(op='-',left=statement.expr, right=c_ast.Constant('int','1'))))
                        else:
                                update_statements.append(statement)
                elif type(statement) is c_ast.For:
                        if type(statement.init) is c_ast.DeclList:
                            for stmt in statement.init.decls:
                                update_statements.append(stmt)
                        else:
                            update_statements.append(statement.init)
                        if type(statement.stmt) is c_ast.Compound:
                        	new_block_items=statement.stmt.block_items
                        	if new_block_items is None:
                                    new_block_items=[]
                        	new_block_items.append(statement.next)
                        	new_block_items=syntaxTranslate(new_block_items)
                        	new_stmt=c_ast.Compound(block_items=new_block_items)
                        	update_while=c_ast.While(statement.cond,new_stmt)
                        	update_statements.append(update_while)
                        else:
                        	new_block_items=[]
                        	new_block_items.append(statement.stmt)
                        	new_block_items.append(statement.next)
				new_block_items=syntaxTranslate(new_block_items)
				new_stmt=c_ast.Compound(block_items=new_block_items)
				update_while=c_ast.While(statement.cond,new_stmt)
                        	update_statements.append(update_while)
                elif type(statement) is c_ast.DoWhile:
                	if type(statement.stmt) is c_ast.Compound:
		        	new_block_items=statement.stmt.block_items
		        	if new_block_items is None:
                                    new_block_items=[]
		        	for item in new_block_items:
		        		update_statements.append(item)
		        	new_block_items=syntaxTranslate(new_block_items)
		        	new_stmt=c_ast.Compound(block_items=new_block_items)
		        	update_while=c_ast.While(statement.cond,new_stmt)
                        	update_statements.append(update_while)
                        else:
                        	new_block_items=[]
                        	new_block_items.append(statement.stmt)
                        	for item in new_block_items:
					update_statements.append(item)
				new_block_items=syntaxTranslate(new_block_items)
				new_stmt=c_ast.Compound(block_items=new_block_items)
				update_while=c_ast.While(statement.cond,new_stmt)
                        	update_statements.append(update_while)
                elif type(statement) is c_ast.Switch:
                	stmts=statement.stmt.block_items
                	statement=convertToIfElse(stmts,statement.cond)
                	#update_statements.append(statement)
                        update_statements.append(syntaxTranslateIf(statement))
                elif type(statement) is c_ast.While:
                	if type(statement.stmt) is c_ast.Compound:
                		update_statements.append(c_ast.While(cond=syntaxTranslateStmt(statement.cond),stmt=c_ast.Compound(block_items=syntaxTranslate(statement.stmt.block_items))))
                	else:
                		new_block_items=[]
				new_block_items.append(statement.stmt)
				update_statements.append(c_ast.While(cond=syntaxTranslateStmt(statement.cond),stmt=c_ast.Compound(block_items=syntaxTranslate(new_block_items))))
                elif type(statement) is c_ast.If:
                	update_statements.append(syntaxTranslateIf(statement))
                elif type(statement) is c_ast.Assignment:
                	if statement.op=='+=':
                		if type(statement.lvalue) is c_ast.ID:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='+', left=c_ast.ID(name=statement.lvalue.name), right=statement.rvalue)))
                		else:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='+', left=statement.lvalue, right=statement.rvalue)))
                	elif statement.op=='-=':
                		if type(statement.lvalue) is c_ast.ID:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='-', left=c_ast.ID(name=statement.lvalue.name), right=statement.rvalue)))
                		else:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='-', left=statement.lvalue.name, right=statement.rvalue)))
                	elif statement.op=='/=':
                		if type(statement.lvalue) is c_ast.ID:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='/', left=c_ast.ID(name=statement.lvalue.name), right=statement.rvalue)))
                		else:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='/', left=statement.lvalue, right=statement.rvalue)))
                	elif statement.op=='%=':
                		if type(statement.lvalue) is c_ast.ID:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='%', left=c_ast.ID(name=statement.lvalue.name), right=statement.rvalue)))
                		else:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='%', left=statement.lvalue, right=statement.rvalue)))
                	elif statement.op=='*=':
                		if type(statement.lvalue) is c_ast.ID:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='*', left=c_ast.ID(name=statement.lvalue.name), right=statement.rvalue)))
                		else:
                			update_statements.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=c_ast.BinaryOp(op='*', left=statement.lvalue, right=statement.rvalue)))
                	
                	else:
                		if type(statement.rvalue) is c_ast.Assignment:
                			stmts=[]
                			separateAllAssignment(statement,stmts)
                			for stmt in stmts:
                				update_statements.append(stmt)
                		else:
                			if type(statement.lvalue) is c_ast.ID and type(statement.rvalue) is c_ast.TernaryOp:
                                            
                                            update_statements.append(syntaxTranslateStmtTernaryOp(statement))
                                            
                                        else:
                                            update_statements.append(c_ast.Assignment(op=statement.op, lvalue=statement.lvalue, rvalue=statement.rvalue))
                
                elif type(statement) is c_ast.ExprList:
                    statement=syntaxTranslate(statement.exprs)
                    for exp_stmt in statement:
                         update_statements.append(exp_stmt)
                elif type(statement) is c_ast.Label:
			update_statements.append(c_ast.Label(name=statement.name, stmt=None))
			if type(statement.stmt) is c_ast.Compound:
				new_block_items=syntaxTranslate(statement.stmt.block_items)
				for item in new_block_items:
					update_statements.append(item)	
			else:
				if statement.stmt is not None:
					new_block_items=[]
					new_block_items.append(statement.stmt)
					new_block_items=syntaxTranslate(new_block_items)
					for item in new_block_items:
						update_statements.append(item)

                elif type(statement) is c_ast.Compound:
                	new_stmts=syntaxTranslate(statement.block_items)
                	for stmt in new_stmts:
                		update_statements.append(stmt)
                	
                else:
                        if type(statement) is not c_ast.EmptyStatement:
                        	update_statements.append(statement)
        return update_statements



def syntaxTranslateIf(statement):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
				new_iftrue=c_ast.Compound(block_items=syntaxTranslate(statement.iftrue.block_items))
			else:
				new_iftrue=c_ast.Compound(block_items=[])
		else:
			if type(statement.iftrue) is c_ast.UnaryOp:
				new_iftrue=syntaxTranslateStmt(statement.iftrue)
			elif type(statement.iftrue) is c_ast.BinaryOp:
				new_iftrue=syntaxTranslateStmt(statement.iftrue)
			else:
				new_blocks=[]
				new_blocks.append(statement.iftrue)
				new_iftrue=c_ast.Compound(block_items=syntaxTranslate(new_blocks))
				
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_iffalse=c_ast.Compound(block_items=syntaxTranslate(statement.iffalse.block_items))
			else:
				new_iffalse=c_ast.Compound(block_items=[])
		else:
			if type(statement.iffalse) is c_ast.If:
				new_iffalse=syntaxTranslateIf(statement.iffalse)
			else:
				if type(statement.iffalse) is c_ast.UnaryOp:
					new_iffalse=syntaxTranslateStmt(statement.iffalse)
				elif type(statement.iffalse) is c_ast.BinaryOp:
					new_iffalse=syntaxTranslateStmt(statement.iffalse)
				else:
					new_blocks=[]
					new_blocks.append(statement.iffalse)
					new_iffalse=c_ast.Compound(block_items=syntaxTranslate(new_blocks))
	return c_ast.If(cond=syntaxTranslateStmt(statement.cond), iftrue=new_iftrue, iffalse=new_iffalse)


#
# Change Assignment statement to a list of Assignment statements
#


def separateAllAssignment(statement,stmts):
	if type(statement) is c_ast.Assignment:
		if type(statement.rvalue) is c_ast.Assignment:
			value=separateAllAssignment(statement.rvalue,stmts)
			stmts.append(c_ast.Assignment(op=statement.op, lvalue=statement.lvalue, rvalue=value))
			return value
		else:
			stmts.append(c_ast.Assignment(op=statement.op, lvalue=statement.lvalue, rvalue=statement.rvalue))
			return statement.rvalue
	return None
	

"""

Covert Switch Case to If-Else-If loop

"""



def convertToIfElse(statements,condition):
	if statements is not None and len(statements)>0:
		statement=statements[0]
		if type(statement) is not c_ast.Default:
			new_condition_left=constructCondition(statements,condition)
			new_condition_right,new_block_items,statements,is_break=constructBody(statements,condition)
			new_compund_left=c_ast.Compound(block_items=new_block_items)
			
			if new_condition_left is not None:
				new_Else_stmt=convertToIfElse(statements,condition)
				new_If_stmt=c_ast.If(cond=c_ast.BinaryOp(op='||', left=new_condition_left, right=new_condition_right),iftrue=new_compund_left,iffalse=new_Else_stmt)
				return new_If_stmt
			else:
				new_Else_stmt=convertToIfElse(statements,condition)
				new_If_stmt=c_ast.If(cond=new_condition_right,iftrue=new_compund_left,iffalse=new_Else_stmt)
				return new_If_stmt
		else:
			update_stmts=[]
			for stmt in statement.stmts:
				#if type(stmt) is not c_ast.Break:
                                update_stmts.append(stmt)
			return c_ast.Compound(block_items=update_stmts)
		

	return None


def syntaxTranslateStmt(statement):
	if type(statement) is c_ast.UnaryOp:
		if statement.op=='++' or statement.op=='p++':
	        	return c_ast.Assignment(op='=',lvalue=statement.expr, rvalue=c_ast.BinaryOp(op='+',left=statement.expr, right=c_ast.Constant('int','1')))
		elif statement.op=='--' or statement.op=='p--':
	        	return c_ast.Assignment(op='=',lvalue=statement.expr, rvalue=c_ast.BinaryOp(op='-',left=statement.expr, right=c_ast.Constant('int','1')))
	        else:
                        return statement
	else:
		if type(statement) is c_ast.BinaryOp:
			return c_ast.BinaryOp(op=statement.op,left=syntaxTranslateStmt(statement.left),right=syntaxTranslateStmt(statement.right))
		else:
			return statement



def syntaxTranslateStmtTernaryOp(statement):
    new_blocks_true=[]
    
    new_blocks_true.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=statement.rvalue.iftrue))
    new_iftrue=c_ast.Compound(block_items=syntaxTranslate(new_blocks_true))
                        
    new_blocks_false=[]
    
    new_blocks_false.append(c_ast.Assignment(op='=', lvalue=statement.lvalue, rvalue=statement.rvalue.iffalse))
    new_iffalse=c_ast.Compound(block_items=syntaxTranslate(new_blocks_false))
                        
    return c_ast.If(cond=statement.rvalue.cond,iftrue=new_iftrue,iffalse=new_iffalse)




"""

Covert Switch Case to If-Else-If loop

"""

	
def constructCondition(statements,condition):
	if statements is not None and len(statements)>0:
		statement=statements[0]
		if type(statement) is not c_ast.Default:
			if len(statement.stmts)==0:
				new_condition_left=c_ast.BinaryOp(op='==', left=condition, right=statement.expr)
				new_condition_right=constructCondition(statements[1:],condition)
				if new_condition_right is None:
					return new_condition_left
				else:
					return c_ast.BinaryOp(op='||', left=new_condition_left, right=new_condition_right)
			else:
				return None
		else:
			return None
	return None


"""

Covert Switch Case to If-Else-If loop

"""


def constructBody(statements,condition):
	if statements is not None and len(statements)>0:
		statement=statements[0]
		if type(statement) is not c_ast.Default:
			if len(statement.stmts)>0:
				update_stmts=[]
				new_condition=c_ast.BinaryOp(op='==', left=condition, right=statement.expr)
				is_break=False
				for stmt in statement.stmts:
					if type(stmt) is c_ast.Break:
						is_break=True;
					else:
						update_stmts.append(stmt)
				return new_condition,update_stmts,statements[1:],is_break
			else:
				return constructBody(statements[1:],condition)
		else:
			return None,None,None,False
	return None,None,None,False



			    
"""
 
Goto removal Modules Start

"""

new_variable={}

break_count=0

continue_count=0



def remove_return(statements,membermethod):
	end_label_map={}
	statements=returnReplacement(statements,end_label_map)
	update_statements=[]
        if isRetPresent(statements)==True:
            if membermethod is not None:
                if membermethod.getreturnType() is not None and membermethod.getreturnType() is not 'array':
                    temp=c_ast.Decl(name='RET', quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname='RET', quals=[], type=c_ast.IdentifierType(names=[membermethod.getreturnType()])), init=c_ast.Constant(type=membermethod.getreturnType(), value='0'), bitsize=None)
                    update_statements.append(temp)
                else:
                    temp=c_ast.Decl(name='RET', quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname='RET', quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
                    update_statements.append(temp)
	for statement in statements:
		update_statements.append(statement)
	for label in end_label_map.keys():
    		update_statements.append(c_ast.Label(name=label, stmt=None))
    	return update_statements



def isRetPresent(statements):
    status_flag=False
    for statement in statements:
        if type(statement) is c_ast.Assignment:
            if type(statement.lvalue) is not c_ast.UnaryOp and type(statement.lvalue.name) is str and 'RET' in statement.lvalue.name:
                status_flag=True
        elif type(statement) is c_ast.If:
            if isRetPresentIf(statement)==True:
                status_flag=True
    return status_flag

def isRetPresentIf(statement):
        status_flag=False
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
                                if isRetPresent(statement.iftrue.block_items)==True:
                                    status_flag=True
		else:
                    if type(statement.iftrue) is c_ast.Assignment:
                        if type(statement.iftrue.lvalue) is not c_ast.UnaryOp and type(statement.iftrue.lvalue.name) is str and 'RET' in statement.iftrue.lvalue.name:
                            status_flag=True
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
                            if isRetPresent(statement.iffalse.block_items)==True:
                                    status_flag=True
		elif type(statement.iffalse) is c_ast.If:
			new_iffalse=isRetPresentIf(statement.iffalse)
		else:
                    if type(statement.iffalse) is c_ast.Assignment:
                        if type(statement.iffalse.lvalue) is not c_ast.UnaryOp and type(statement.iffalse.lvalue.name) is str and 'RET' in statement.iffalse.lvalue.name:
                            status_flag=True
	return status_flag


"""

Is Variable is present and Type


"""

def isVarPresnt(statements,variable_name):
    status_flag=False
    for statement in statements:
        if type(statement) is c_ast.Assignment:
                flag_r=isVarPresntStmt(statement.rvalue,variable_name)
                flag_l=isVarPresntStmt(statement.lvalue,variable_name)
                if flag_r==True and flag_l==True:
                    return True
                elif flag_r==False and flag_l==True:
                    return True 
                elif flag_r==True and flag_l==False:
                    return True 
        elif type(statement) is c_ast.If:
            if isVarPresntIf(statement,variable_name)==True:
                return True
        elif type(statement) is c_ast.While:
            if type(statement.stmt) is c_ast.Compound:
                if isVarPresnt(statement.stmt.block_items,variable_name)==True:
                    return True
    return False

def isVarPresntIf(statement,variable_name):
        status_flag=False
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
                                if isVarPresnt(statement.iftrue.block_items,variable_name)==True:
                                    status_flag=True
		else:
                    if type(statement.iftrue) is c_ast.Assignment:
                        flag_r=isVarPresntStmt(statement.iftrue.rvalue,variable_name)
                        flag_l=isVarPresntStmt(statement.iftrue.lvalue,variable_name)
                        if flag_r==True and flag_l==True:
                            status_flag = True
                        elif flag_r==False and flag_l==True:
                            status_flag = True 
                        elif flag_r==True and flag_l==False:
                            status_flag = True
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
                            if isVarPresnt(statement.iffalse.block_items,variable_name)==True:
                                    status_flag=True
		elif type(statement.iffalse) is c_ast.If:
			if isVarPresntIf(statement.iffalse,variable_name):
                            status_flag=True
		else:
                    if type(statement.iffalse) is c_ast.Assignment:
                        flag_r=isVarPresntStmt(statement.iffalse.rvalue,variable_name)
                        flag_l=isVarPresntStmt(statement.iffalse.lvalue,variable_name)
                        if flag_r==True and flag_l==True:
                            status_flag = True
                        elif flag_r==False and flag_l==True:
                            status_flag = True 
                        elif flag_r==True and flag_l==False:
                            status_flag = True
	return status_flag


def isVarPresntStmt(statement,variable_name):
	if type(statement) is c_ast.UnaryOp:
                return isVarPresntStmt(statement.expr,variable_name)
        elif type(statement) is c_ast.BinaryOp:
                flag_r=isVarPresntStmt(statement.right,variable_name)
                flag_l=isVarPresntStmt(statement.left,variable_name)
                if flag_r==True and flag_l==True:
                    return True
                elif flag_r==False and flag_l==True:
                    return True 
                elif flag_r==True and flag_l==False:
                    return True 
                else:
                    return False 
        elif type(statement) is c_ast.ID:
            if variable_name==statement.name:
                return True
            else:
                return False
        elif type(statement) is c_ast.StructRef:
            return isVarPresntStmt(statement.name,variable_name)
        elif type(statement) is c_ast.ArrayRef:
            if variable_name == getArrayName(statement):
                return True
            else:
                return False
	else:
            return False









"""

Method for simplification of Condition

"""

def simplifyCondition(statement):
	if type(statement) is c_ast.UnaryOp:
		if statement.op=='!':
			if type(statement.expr) is c_ast.ID:
				return statement
			elif type(statement.expr) is c_ast.Constant:
				return statement
			elif type(statement.expr) is c_ast.ArrayRef:
				return statement
			elif type(statement.expr) is c_ast.FuncCall:
				return statement
			else:
				return getComplement(statement.expr)
		else:
			return c_ast.UnaryOp(op=statement.op,expr=simplifyCondition(statement.expr))
	elif type(statement) is c_ast.BinaryOp:
		return c_ast.BinaryOp(op=statement.op,left=simplifyCondition(statement.left), right=simplifyCondition(statement.right))
	else:
		return statement

"""

Method for Generate  Complement of Condition

"""


def getComplement(statement):
	if type(statement) is c_ast.UnaryOp:
		if statement.op=='!': 
			return simplifyCondition(statement.expr)
		else:
			return c_ast.UnaryOp(op=statement.op,expr=simplifyCondition(statement.expr))
	
	elif type(statement) is c_ast.BinaryOp:
		if statement.op=='<':
			return c_ast.BinaryOp(op='>=',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='>':
			return c_ast.BinaryOp(op='<=',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='<=':
			return c_ast.BinaryOp(op='>',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='>=':
			return c_ast.BinaryOp(op='<',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='!=':
			return c_ast.BinaryOp(op='==',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='==':
			return c_ast.BinaryOp(op='!=',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='&&':
			return c_ast.BinaryOp(op='||',left=getComplement(statement.left), right=getComplement(statement.right))
		elif statement.op=='||':
			return c_ast.BinaryOp(op='&&',left=getComplement(statement.left), right=getComplement(statement.right))
		else:
			return c_ast.BinaryOp(op=statement.op,left=getComplement(statement.left), right=getComplement(statement.right))


	else:
		return statement




"""

For Whole program

"""

def changeCondition(statement):
	if type(statement) is c_ast.ID:
		return c_ast.BinaryOp(op='>',left=statement,right=c_ast.Constant(type='int', value='0'))
	elif type(statement) is c_ast.Constant:
		return c_ast.BinaryOp(op='>',left=statement,right=c_ast.Constant(type='int', value='0'))
	elif type(statement) is c_ast.FuncCall:
		return c_ast.BinaryOp(op='>',left=statement,right=c_ast.Constant(type='int', value='0'))
	elif type(statement) is c_ast.ArrayRef:
		return c_ast.BinaryOp(op='>',left=statement,right=c_ast.Constant(type='int', value='0'))
	elif type(statement) is c_ast.UnaryOp:
		if statement.op=='!':
			if type(statement.expr) is c_ast.ID:
				return c_ast.BinaryOp(op='<=',left=statement.expr,right=c_ast.Constant(type='int', value='0'))
			elif type(statement.expr) is c_ast.Constant:
				return c_ast.BinaryOp(op='<=',left=statement.expr,right=c_ast.Constant(type='int', value='0'))
			elif type(statement.expr) is c_ast.FuncCall:
				return c_ast.BinaryOp(op='<=',left=statement.expr,right=c_ast.Constant(type='int', value='0'))
			elif type(statement.expr) is c_ast.ArrayRef:
				return c_ast.BinaryOp(op='<=',left=statement.expr,right=c_ast.Constant(type='int', value='0'))
			else:
				return statement
		else:
			return statement
	elif type(statement) is c_ast.BinaryOp:
                left_stmt=None
                right_stmt=None
                if statement.op=='||':
                    if type(statement.left) is c_ast.ID:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.Constant:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.FuncCall:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.ArrayRef:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    else:
                        left_stmt=changeCondition(statement.left)
                        
                    if type(statement.right) is c_ast.ID:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.Constant:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.FuncCall:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.ArrayRef:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    else:
                        right_stmt=changeCondition(statement.right)
                    return c_ast.BinaryOp(op=statement.op,left=left_stmt, right=right_stmt)
                elif statement.op=='&&':
                    if type(statement.left) is c_ast.ID:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.Constant:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.FuncCall:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.left) is c_ast.ArrayRef:
                        left_stmt=c_ast.BinaryOp(op='>',left=statement.left,right=c_ast.Constant(type='int', value='0'))
                    else:
                        left_stmt=changeCondition(statement.left)
                        
                    if type(statement.right) is c_ast.ID:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.Constant:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.FuncCall:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    elif type(statement.right) is c_ast.ArrayRef:
                        right_stmt=c_ast.BinaryOp(op='>',left=statement.right,right=c_ast.Constant(type='int', value='0'))
                    else:
                        right_stmt=changeCondition(statement.right)
                    return c_ast.BinaryOp(op=statement.op,left=left_stmt, right=right_stmt)
                else:
                 	return statement
                        
		
	else:
		return statement




def modificationOfCondition(statement):
	if type(statement) is c_ast.ID:
		return True,statement
	elif type(statement) is c_ast.Constant:
		return True,statement
	elif type(statement) is c_ast.FuncCall:
		return True,statement
	elif type(statement) is c_ast.UnaryOp:
		if statement.op=='!':
			status,statement.expr=modificationOfCondition(statement.expr)
			if status==True:
				return False,c_ast.BinaryOp(op='<=',left=statement.expr,right=c_ast.Constant(type='int', value='0'))
			else:
				return True,statement
		else:
			return True,statement
	elif type(statement) is c_ast.BinaryOp:
		left_stmt=None
                right_stmt=None
		if statement.op=='||':
			status,left_stmt=modificationOfCondition(statement.left)
			if status==True:
				left_stmt=c_ast.BinaryOp(op='>',left=left_stmt,right=c_ast.Constant(type='int', value='0'))
			status=False
			status,right_stmt=modificationOfCondition(statement.right)
			if status==True:
				right_stmt=c_ast.BinaryOp(op='>',left=right_stmt,right=c_ast.Constant(type='int', value='0'))
			return False,c_ast.BinaryOp(op=statement.op,left=left_stmt, right=right_stmt)
		elif statement.op=='&&':
			status,left_stmt=modificationOfCondition(statement.left)
			if status==True:
				left_stmt=c_ast.BinaryOp(op='>',left=left_stmt,right=c_ast.Constant(type='int', value='0'))
			status=False
			status,right_stmt=modificationOfCondition(statement.right)
			if status==True:
				right_stmt=c_ast.BinaryOp(op='>',left=right_stmt,right=c_ast.Constant(type='int', value='0'))
			return False,c_ast.BinaryOp(op=statement.op,left=left_stmt, right=right_stmt)
		elif statement.op=='>':
			return False,statement
		elif statement.op=='<':
			return False,statement
		elif statement.op=='>=':
			return False,statement
		elif statement.op=='<=':
			return False,statement
		elif statement.op=='=':
			return False,statement
		elif statement.op=='==':
			return False,statement
		elif statement.op=='!=':
			return False,statement
		else:
			status1,left_stmt=modificationOfCondition(statement.left)
			status2,right_stmt=modificationOfCondition(statement.right)
			if status1==True and status2==True:
				return True,c_ast.BinaryOp(op=statement.op,left=left_stmt,right=right_stmt)
			else:
				return False,c_ast.BinaryOp(op=statement.op,left=left_stmt,right=right_stmt)
			
	else:
		return False,statement
		


def changeConditionProgram(statements):
	if statements is not None:
		update_statements=[]
		for statement in statements:
			if type(statement) is c_ast.If:
				update_statements.append(changeConditionProgramIf(statement))
			elif type(statement) is c_ast.While:
				update_statements.append(c_ast.While(cond=changeCondition(statement.cond),stmt=c_ast.Compound(block_items=changeConditionProgram(statement.stmt.block_items))))
			else:
				update_statements.append(statement)
		return update_statements			
	return None



def changeConditionProgramIf(statement):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
				new_iftrue=c_ast.Compound(block_items=changeConditionProgram(statement.iftrue.block_items))
			else:
				new_iftrue=statement.iftrue
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_iffalse=c_ast.Compound(block_items=changeConditionProgram(statement.iffalse.block_items))
			else:
				new_iftrue=statement.iffalse
		elif type(statement.iffalse) is c_ast.If:
			new_iffalse=changeConditionProgramIf(statement.iffalse)
		else:
			new_iffalse=statement.iffalse
	return c_ast.If(cond=changeCondition(statement.cond),iftrue=new_iftrue,iffalse=new_iffalse)




def simplifyProgram(statements):
	if statements is not None:
		update_statements=[]
		for statement in statements:
			if type(statement) is c_ast.If:
				update_statements.append(simplifyProgram_If(statement))
			elif type(statement) is c_ast.While:
				update_statements.append(c_ast.While(cond=simplifyCondition(statement.cond),stmt=c_ast.Compound(block_items=simplifyProgram(statement.stmt.block_items))))
			else:
				update_statements.append(statement)
		return update_statements			
	return None



def simplifyProgram_If(statement):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
				new_iftrue=c_ast.Compound(block_items=simplifyProgram(statement.iftrue.block_items))
			else:
				new_iftrue=statement.iftrue
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_iffalse=c_ast.Compound(block_items=simplifyProgram(statement.iffalse.block_items))
			else:
				new_iftrue=statement.iffalse
		elif type(statement.iffalse) is c_ast.If:
			new_iffalse=simplifyProgram_If(statement.iffalse)
		else:
			new_iffalse=statement.iffalse
	return c_ast.If(cond=simplifyCondition(statement.cond),iftrue=new_iftrue,iffalse=new_iffalse)



def removeDeadCode(statements):
	update_statements=[]
	flag=False
	if statements is not None:
		for statement in statements:
			if type(statement) is c_ast.Goto:
				flag=True
			elif type(statement) is c_ast.Label:
				flag=False
				stmts=statement.stmt
				if stmts is not None:
					for stmt in stmts:
						update_statements.append(stmt)
			else:
				if flag==False:
					update_statements.append(statement)
	return update_statements



def gotoremoval(statements):
	if statements is not None:
		label_map=constructLabelTable(statements,0,0,0)
		updateLabelTable(statements,0,0,0,label_map)
		keys=label_map.keys()
		for key in keys:
			labelMap={}
			listL=label_map[key]
			if len(listL[3])>1:
		    		statements=removeMultipleLabel(statements,key,labelMap)
		    		statements=addMultipleLabel(statements,key,labelMap)
		    		label_map=constructLabelTable(statements,0,0,0)
    				updateLabelTable(statements,0,0,0,label_map)
    			else:
    				if len(listL[3])==0:
					#statements=removeOrphanLabel(statements,key)
					label_map=constructLabelTable(statements,0,0,0)
    					updateLabelTable(statements,0,0,0,label_map)
    			
		label_map=constructLabelTable(statements,0,0,0)
    		updateLabelTable(statements,0,0,0,label_map)
    		
    		
		blank_label_map1={}
		blank_label_map2={}
		for element in label_map.keys():
			temp_list=label_map[element]
			temp_temp_list=temp_list[3]
			temp_temp_list1=[]
			temp_temp_list2=[]
			for iteam in temp_temp_list:
				if iteam[3] is not None:
					temp_temp_list1.append(iteam)
				else:
					temp_temp_list2.append(iteam)
			
			
			if len(temp_temp_list1)>0:
				temp_list1=[]
				temp_list1.append(temp_list[0])
				temp_list1.append(temp_list[1])
				temp_list1.append(temp_list[2])
				temp_list1.append(temp_temp_list1)
				blank_label_map1[element]=temp_list1
			
			if len(temp_temp_list2)>0:
				temp_list2=[]
				temp_list2.append(temp_list[0])
				temp_list2.append(temp_list[1])
				temp_list2.append(temp_list[2])
				temp_list2.append(temp_temp_list2)
				blank_label_map2[element]=temp_list2
		

		label_map=blank_label_map1
		keys=label_map.keys()
		if len(keys)>0:
			item=keys[0]
			element = label_map[item]
    			lists = element[3]
    			for list in lists:
    				if element[0]>=list[0] and element[1]>=list[1]:
        				statements=goto_finder(statements,item)
    					statements=go_block_finder(statements,item)
    					statements=gotoremoval(statements)
    				else:
                                        if element[1]>=1:
    						statements=label_finder_inside(statements,item)
    						statements=go_block_finder(statements,item)
       						statements=gotoremoval(statements)
       					else:
						statements=label_finder(statements,item)
						statements=go_block_finder(statements,item)
       						statements=gotoremoval(statements)
    	return statements





#Finding Goto in a Block to Call gotomovein
#Parameter pass block of statement 
#Label
testcount=0

def go_block_finder(statements,label):
	if statements is not None:
		flag_block_label=check_label_block(statements,label)  
		flag_block_goto=check_goto_block_Sp(statements,label)
		if flag_block_label==True and flag_block_goto==True:
			return remove_goto_block(statements,label)
		else:
			update_statements=[]
			for statement in statements:
				if type(statement) is c_ast.If:
					update_statements.append(go_block_finder_if(statement,label))
				elif type(statement) is c_ast.While:
					update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=go_block_finder(statement.stmt.block_items,label))))
				else:
					update_statements.append(statement)
		return update_statements
	return statements
				


#Finding Goto in a If Block to Call gotomovein
#Parameter pass statement 
#Label

def go_block_finder_if(statement,label):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
				new_iftrue=c_ast.Compound(block_items=go_block_finder(statement.iftrue.block_items,label))
			else:
				new_iftrue=statement.iftrue
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_iffalse=c_ast.Compound(block_items=go_block_finder(statement.iffalse.block_items,label))
			else:
				new_iftrue=statement.iffalse
		elif type(statement.iffalse) is c_ast.If:
			new_iffalse=go_block_finder_if(statement.iffalse,label)
		else:
			new_iffalse=statement.iffalse
	return c_ast.If(cond=statement.cond,iftrue=new_iftrue,iffalse=new_iffalse)






#Method to Remove Goto 


def remove_goto_block(statements,label): 
	flag_block_label=check_label_block(statements,label)  
	flag_block_goto=check_goto_block_Sp(statements,label)
	flag_block2,condition=check_goto(statements,label)
	flag_label=False
	flag_goto=False
	new_statements1=[]
	new_statements2=[]
	process_part1=False
	process_part2=False
	if flag_block_label==True and flag_block_goto==True:
                #print '#######1234'
                #generator = c_generator.CGenerator() 
                #print(generator.visit(c_ast.Compound(block_items=statements)))
                #print '#######1234'
		for statement in statements:
			#print type(statement)
			#print flag_label
			#print flag_goto
			if type(statement) is c_ast.Label:
				if label==statement.name:
					process_part2=True			
					if flag_goto==True:
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2),iffalse=None))
						if type(statement.stmt) is c_ast.Assignment:
							new_statements1.append(statement.stmt)
						elif type(statement.stmt) is c_ast.Compound:
							if statement.stmt is not None and statement.stmt.block_items is not None:
								for stmt in statement.stmt.block_items:
									new_statements1.append(stmt)
						else:
							new_statements1.append(statement.stmt)
						flag_label=False
						flag_goto=False
					else:
						if type(statement.stmt) is c_ast.Assignment:
							new_statements2.append(statement.stmt)
						elif type(statement.stmt) is c_ast.Compound:
							if statement.stmt is not None and statement.stmt.block_items is not None:
								for stmt in statement.stmt.block_items:
									new_statements2.append(stmt)
						flag_label=True
				else:
					if flag_goto==True or flag_label==True:
						if type(statement.stmt) is c_ast.Assignment:
                                                        new_statements2.append(c_ast.Label(name=statement.name, stmt=None))
							new_statements2.append(statement.stmt)
						elif type(statement.stmt) is c_ast.Compound:
                                                        new_statements2.append(c_ast.Label(name=statement.name, stmt=None))
							if statement.stmt is not None and statement.stmt.block_items is not None:
								for stmt in statement.stmt.block_items:
									new_statements2.append(stmt)
                                                else:
                                                    new_statements2.append(statement)
					else:
						new_statements1.append(statement)
			elif type(statement) is c_ast.If:
				flag_block_goto=check_goto_block_If(statement,label)
				if flag_block_goto:
					process_part1=True
					if flag_label==True:
						statement=getRidOfGoto(statement,label)
						for stmt in new_statements2:
							new_statements1.append(stmt)
						new_statements1.append(statement)
						
						new_break_map={}
						new_statements2=reOrganizeBreaks(new_statements2,new_break_map)

						new_statements1.append(c_ast.While(cond=condition, stmt=c_ast.Compound(block_items=new_statements2)))
						new_statements1=addingBreakVariables(new_statements1,new_break_map)
						flag_label=False
						flag_goto=False
					else:
						statement=getRidOfGoto(statement,label)
						new_statements1.append(statement)
						flag_goto=True
				else:
					if flag_goto==True or flag_label==True:
						new_statements2.append(statement)
					else:
						new_statements1.append(statement)
			else:
				if flag_goto==True or flag_label==True:
					new_statements2.append(statement)
				else:
					new_statements1.append(statement)
	
	if process_part1==True and process_part2==True:
		return new_statements1
	else:
		return None
		#return None
				
				
def remove_goto_block_sp(statements,label): 
	flag_block_label=check_label_block(statements,label)  
	flag_block_goto=check_goto_block_Sp(statements,label)
	flag_block2,condition=check_goto(statements,label)
	flag_label=False
	flag_goto=False
	new_statements1=[]
	new_statements2=[]
	if flag_block_label==True and flag_block_goto==True:
		for statement in statements:
			if type(statement) is c_ast.If:
				flag_block_goto=check_goto_block_If(statement,label)
				flag_label_sp=check_label_block_If(statement,label)  
				if flag_label_sp==True and flag_block_goto==False:
					new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2),iffalse=None))
					stmt=update_If_removegoto(statement,label,condition)
					new_statements1.append(stmt)
				elif flag_block_goto:
					if flag_label==True:
						statement=getRidOfGoto(statement,label)
						for stmt in new_statements2:
							new_statements1.append(stmt)
						new_statements1.append(statement)
						
						new_break_map={}
						new_statements2=reOrganizeBreaks(new_statements2,new_break_map)

						new_statements1.append(c_ast.While(cond=condition, stmt=c_ast.Compound(block_items=new_statements2)))
						new_statements1=addingBreakVariables(new_statements1,new_break_map)
						flag_label=False
						flag_goto=False
					else:
						statement=getRidOfGoto(statement,label)
						new_statements1.append(statement)
						flag_goto=True
				else:
					if flag_goto==True or flag_label==True:
						new_statements2.append(statement)
					else:
						new_statements1.append(statement)
			else:
				if flag_goto==True or flag_label==True:
					new_statements2.append(statement)
				else:
					new_statements1.append(statement)
	
	return new_statements1



def update_If_removegoto(statement,label,condition):
	new_if_stmt=None
	new_else_stmt=None
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Label:
				if statement.iftrue.name==label:
                                        new_statements=[]
                                        new_statements.append(c_ast.If(cond=condition,iftrue=c_ast.Goto(name=label),iffalse=None))
                                        new_statements.append(statement.iftrue)
                                        new_if_stmt=c_ast.Compound(block_items=remove_goto_block(new_statements,label))
                                else:
                                	new_if_stmt=statement.iftrue
                                        
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			status=False
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Label:
                                                        if element.name==label:
                                                                status = True
                                        if status==True:
                                        	new_statements=[]
                                        	new_statements.append(c_ast.If(cond=condition,iftrue=c_ast.Goto(name=label),iffalse=None))
                                        	for element in statement.iftrue.block_items:
                                        		new_statements.append(element)
                                        	new_if_stmt=c_ast.Compound(block_items=remove_goto_block(new_statements,label))
                                        else:
                                        	new_if_stmt=statement.iftrue
                                        		
                                                                
			if type(statement.iffalse) is c_ast.Label:
                                if statement.iffalse.name==label:
                                         new_statements=[]
					 new_statements.append(c_ast.If(cond=condition,iftrue=c_ast.Goto(name=label),iffalse=None))
					 new_statements.append(statement.iftrue)
                                         new_if_stmt=c_ast.Compound(block_items=remove_goto_block(new_statements,label))
                                else:
                                	new_else_stmt=statement.iffalse
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			status=False
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Label:
	            					if element.name==label:
                                                                status = True
                                        if status==True:
						new_statements=[]
					        new_statements.append(c_ast.If(cond=condition,iftrue=c_ast.Goto(name=label),iffalse=None))
					        for element in statement.iffalse.block_items:
					        	new_statements.append(element)
					        new_else_stmt=c_ast.Compound(block_items=remove_goto_block(new_statements,label))
					else:
                                        	new_else_stmt=statement.iffalse
				else:
					if type(statement.iffalse) is c_ast.If:
						new_else_stmt=update_If_removegoto(statement.iffalse,label,condition)
	return c_ast.If(cond=c_ast.BinaryOp(op='&&', left=statement.cond, right=condition),iftrue=new_if_stmt,iffalse=new_else_stmt)







    
    
def constructLabelTable(statements,level,block,lineCount):
	label_map={}
	if statements is not None:
		for statement in statements:
			if type(statement) is c_ast.If:
				block=block+1
				label_map_temp=constructLabelTable_If(statement,level,block,lineCount)
	            		for item in label_map_temp:
            				label_map[item]=label_map_temp[item]
            			block=block-1
			elif type(statement) is c_ast.Label:
				lineCount=lineCount+1
			        info=[]
			        info.append(level)
	            		info.append(block)
	            		info.append(lineCount)
	            		info.append([])
				label_map[statement.name]=info
	        	else:
	        		if type(statement) is c_ast.While:
	        			level=level+1
	            			label_map_temp=constructLabelTable(statement.stmt.block_items,level,block,lineCount)
	            			for item in label_map_temp:
            					label_map[item]=label_map_temp[item]
            				level=level-1
            			else:
            				lineCount=lineCount+1
	return label_map




def constructLabelTable_If(statement,level,block,lineCount):
	label_map={}
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Label:
				lineCount=lineCount+1	            				
				info=[]
				info.append(level)
				info.append(block)
				info.append(lineCount)
				info.append([])
				label_map[statement.iftrue.name]=info
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Label:
							lineCount=lineCount+1	            				
	            					info=[]
	            					info.append(level)
	            					info.append(block)
	            					info.append(lineCount)
	            					info.append([])
	            					label_map[element.name]=info
	            				elif type(element) is c_ast.If:
	            					block=block+1
							label_map_temp=constructLabelTable_If(element,level,block,lineCount)
							for item in label_map_temp:
            							label_map[item]=label_map_temp[item]
            						block=block-1
						else:
							if type(element) is c_ast.While:
								level=level+1
						        	label_map_temp=constructLabelTable(element.stmt.block_items,level,block,lineCount)
						        	for item in label_map_temp:
					            			label_map[item]=label_map_temp[item]
            							level=level-1
            						else:
            							lineCount=lineCount+1
	
			if type(statement.iffalse) is c_ast.Label:
				lineCount=lineCount+1	            				
				info=[]
				info.append(level)
				info.append(block)
				info.append(lineCount)
				info.append([])
				label_map[statement.iffalse.name]=statement.iffalse.name
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Label:
	            					lineCount=lineCount+1
	            					info=[]
							info.append(level)
	            					info.append(block)
	            					info.append(lineCount)
	            					info.append([])
	            					label_map[element.name]=info
	            				elif type(element) is c_ast.If:
	            					block=block+1
							label_map_temp=constructLabelTable_If(element,level,block,lineCount)
							for item in label_map_temp:
            							label_map[item]=label_map_temp[item]
            						block=block-1
						else:
							if type(element) is c_ast.While:
								level=level+1
						        	label_map_temp=constructLabelTable(element.stmt.block_items,level,block,lineCount)
						        	for item in label_map_temp:
					            			label_map[item]=label_map_temp[item]
            							level=level-1
            						else:
            							lineCount=lineCount+1
				else:
					if type(statement.iffalse) is c_ast.If:
						label_map_temp=constructLabelTable_If(statement.iffalse,level,block,lineCount)
						for item in label_map_temp:
							label_map[item]=label_map_temp[item]
	return label_map

    
    

def updateLabelTable(statements,level,block,lineCount,label_map):
	if statements is not None:
		for statement in statements:
			if type(statement) is c_ast.If:
				updateLabelTable_If(statement,level,block,lineCount,label_map)
	        	else:
	        		if type(statement) is c_ast.While:
	        			level=level+1
	            			updateLabelTable(statement.stmt.block_items,level,block,lineCount,label_map)
            				level=level-1
            			elif type(statement) is c_ast.Goto:
                                    lineCount=lineCount+1	            				
                                    info=[]
                                    info.append(level)
                                    info.append(block)
                                    info.append(lineCount)
                                    info.append(None)
                                    if statement.name in label_map.keys():
					info_update=label_map[statement.name]
				        list=info_update[3]
				        list.append(info)	
            			
            			else:
            				lineCount=lineCount+1





def updateLabelTable_If(statement,level,block,lineCount,label_map):
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Goto:
				lineCount=lineCount+1	            				
				info=[]
				info.append(level)
				info.append(block)
				info.append(lineCount)
				info.append(statement.cond)
				if statement.iftrue.name in label_map.keys():
					info_update=label_map[statement.iftrue.name]
				        list=info_update[3]
				        list.append(info)		

			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Goto:
							lineCount=lineCount+1	            				
	            					info=[]
	            					info.append(level)
	            					info.append(block)
	            					info.append(lineCount)
	            					info.append(statement.cond)
	            					if element.name in label_map.keys():
	            						info_update=label_map[element.name]
	            						list=info_update[3]
	            						list.append(info)
	            				elif type(element) is c_ast.If:
	            					block=block+1
							updateLabelTable_If(element,level,block,lineCount,label_map)
            						block=block-1
						else:
							if type(element) is c_ast.While:
								level=level+1
						        	updateLabelTable(element.stmt.block_items,level,block,lineCount,label_map)
            							level=level-1
            						else:
            							lineCount=lineCount+1
	
			if type(statement.iffalse) is c_ast.Goto:
				lineCount=lineCount+1	            				
				info=[]
				info.append(level)
				info.append(block)
				info.append(lineCount)
				info.append(statement.cond)
				if statement.iffalse.name in label_map.keys():
					info_update=label_map[statement.iffalse.name]
					list=info_update[3]
					list.append(info)
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Goto:
	            					lineCount=lineCount+1
	            					info=[]
							info.append(level)
	            					info.append(block)
	            					info.append(lineCount)
	            					info.append(statement.cond)
	            					if element.name in label_map.keys():
	            						info_update=label_map[element.name]
	            						list=info_update[3]
	            						list.append(info)
	            				elif type(element) is c_ast.If:
	            					block=block+1
							updateLabelTable_If(element,level,block,lineCount,label_map)
            						block=block-1
						else:
							if type(element) is c_ast.While:
								level=level+1
						        	updateLabelTable(element.stmt.block_items,level,block,lineCount,label_map)
            							level=level-1
            						else:
            							lineCount=lineCount+1
				else:
					if type(statement.iffalse) is c_ast.If:
						updateLabelTable_If(statement.iffalse,level,block,lineCount,label_map)
					
					
#Check a label in a block of statement


def check_label_block(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.If:
                        temp_status=check_label_block_If(statement,label)
                        if temp_status==True:
                               status=True 
		elif type(statement) is c_ast.Label:
                        if statement.name==label:
                                status = True
	return status
	



def check_label_block_sp(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.Label:
                        if statement.name==label:
                                status = True
	return status

#Check a label in the blocks of statement of if loop
	
def check_label_block_If(statement,label):
        status=False
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Label:
				if statement.iftrue.name==label:
                                        status = True
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Label:
                                                        if element.name==label:
                                                                status = True
                                                                
			if type(statement.iffalse) is c_ast.Label:
                                if statement.iffalse.name==label:
                                        status = True
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Label:
	            					if element.name==label:
                                                                status = True
				else:
					if type(statement.iffalse) is c_ast.If:
						temp_status = check_label_block_If(statement.iffalse,label)
						if temp_status==True:
                                                	status=True
	return status



#Check a label in statement


def check_label(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.If:
                        temp_status=check_label_If(statement,label)
                        if temp_status==True:
                               status=True 
		elif type(statement) is c_ast.Label:
                        if statement.name==label:
                                status = True
	        else:
	        	if type(statement) is c_ast.While:
	            		temp_status= check_label(statement.stmt.block_items,label)
	            		if temp_status==True:
                                        status=True
	return status



def check_label_sp(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.If:
                        temp_status=check_label_If(statement,label)
                        if temp_status==True:
                               status=True 
		elif type(statement) is c_ast.Label:
                        if statement.name==label:
                                status = True
	return status



#Check a label in statement of if loop

def check_label_If(statement,label):
        status=False
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Label:
				if statement.iftrue.name==label:
                                        status = True
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Label:
                                                        if element.name==label:
                                                                status = True
	            				elif type(element) is c_ast.If:
							temp_status = check_label_If(element,label)
							if temp_status==True:
                                                               status=True
						else:
							if type(element) is c_ast.While:
						        	temp_status = check_label(element.stmt.block_items,label)
						        	if temp_status==True:
                                                                        status=True
	
			if type(statement.iffalse) is c_ast.Label:
                                if statement.iffalse.name==label:
                                        status = True
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Label:
	            					if element.name==label:
                                                                status = True
	            				elif type(element) is c_ast.If:
                                                        temp_status = check_label_If(element,label)
                                                        if temp_status==True:
                                                                status=True
						else:
							if type(element) is c_ast.While:
								temp_status = check_label(element.stmt.block_items,label)
								if temp_status==True:
                                                                        status=True

				else:
					temp_status = check_label_If(statement.iffalse,label)
					if temp_status==True:
                                                status=True
	return status





#Check a goto-label in a block of statement


def check_goto_block(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.Goto:
                        if statement.name==label:
                                status = True

	return status


def check_goto_block_Sp(statements,label):
        status=False
	for statement in statements:
		if type(statement) is c_ast.Goto:
                        if statement.name==label:
                                status = True
               	elif type(statement) is c_ast.If:
                	temp_status=check_goto_block_If(statement,label)
                	if temp_status==True:
                		status=True
	return status
	
	

#Check a label in the blocks of statement of if loop
	
def check_goto_block_If(statement,label):
        status=False
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Goto:
				if statement.iftrue.name==label:
                                        status = True
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Goto:
                                                        if element.name==label:
                                                                status = True
			if type(statement.iffalse) is c_ast.Label:
                                if statement.iffalse.name==label:
                                        status = True
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Goto:
	            					if element.name==label:
                                                                status = True
				else:
					if type(statement.iffalse) is c_ast.If:
						temp_status = check_goto_block_If(statement.iffalse,label)
						if temp_status==True:
                                                	status=True
	return status



#Check a label in statement


def check_goto(statements,label):
        status=False
        condition=None
	for statement in statements:
		if type(statement) is c_ast.If:
                        temp_status,temp_cond=check_goto_If(statement,label)
                        if temp_status==True:
                               status=True
                               condition=temp_cond
		elif type(statement) is c_ast.Goto:
                        if statement.name==label:
                                status = True
	        else:
	        	if type(statement) is c_ast.While:
	            		temp_status,temp_cond= check_goto(statement.stmt.block_items,label)
	            		if temp_status==True:
                                        status=True
                                        condition=temp_cond
	return status,condition




#Check a label in statement of if loop

def check_goto_If(statement,label):
        status=False
        condition=None
	if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Goto:
				if statement.iftrue.name==label:
                                        status = True
                                        condition=statement.cond
			else:
	            		if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
	            			for element in statement.iftrue.block_items:
	            				if type(element) is c_ast.Goto:
                                                        if element.name==label:
                                                                status = True
                                                                condition=statement.cond
	            				elif type(element) is c_ast.If:
							temp_status,temp_cond = check_goto_If(element,label)
							if temp_status==True:
                                                               status=True
                                                               #condition=temp_cond
                                                               condition=c_ast.BinaryOp(op='&&', left=temp_cond, right=statement.cond)
						else:
							if type(element) is c_ast.While:
						        	temp_status,temp_cond = check_goto(element.stmt.block_items,label)
						        	if temp_status==True:
                                                                        status=True
                                                                        condition=temp_cond
	
			if type(statement.iffalse) is c_ast.Goto:
                                if statement.iffalse.name==label:
                                        status = True
                                        condition = c_ast.UnaryOp(op='!', expr=statement.cond)
			else:
				if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
	            			for element in statement.iffalse.block_items:
	            				if type(element) is c_ast.Goto:
	            					if element.name==label:
                                                                status = True
                                                                condition = c_ast.UnaryOp(op='!', expr=statement.cond)
	            				elif type(element) is c_ast.If:
                                                        temp_status,temp_cond = check_goto_If(element,label)
                                                        if temp_status==True:
                                                                status=True
                                                                #condition=temp_cond
                                                                condition=c_ast.BinaryOp(op='&&', left=temp_cond, right=c_ast.UnaryOp(op='!', expr=statement.cond))
						else:
							if type(element) is c_ast.While:
								temp_status,temp_cond = check_goto(element.stmt.block_items,label)
								if temp_status==True:
                                                                        status=True
                                                                        condition=temp_cond

				else:
					temp_status,temp_cond = check_goto_If(statement.iffalse,label)
					if temp_status==True:
                                                status=True
                                                #condition=temp_cond
                                                condition=c_ast.BinaryOp(op='&&', left=temp_cond, right=c_ast.UnaryOp(op='!', expr=statement.cond))
	return status,condition






#Finding Goto in a Block to Call gotomovein
#Parameter pass block of statement 
#Label


def label_finder(statements,label):
	if statements is not None:
		flag_block1=check_label_block(statements,label)
		if flag_block1==True:
			return gotomoveout(statements,label)
		else:
			update_statements=[]
			if statements is not None:
				for statement in statements:
					if type(statement) is c_ast.If:
						update_statements.append(label_finder_if(statement,label))
					elif type(statement) is c_ast.While:
						update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=label_finder(statement.stmt.block_items,label))))
					else:
						update_statements.append(statement)
				return update_statements
			return statements
	return statements
				




#Finding Goto in a Block to Call gotomovein
#Parameter pass block of statement 
#Label


def label_finder_inside(statements,label):
	if statements is not None:
		flag_block1=check_label_block(statements,label)
		flag_block2=check_label_block_sp(statements,label)
		flag_block3=check_goto_block_Sp(statements,label)
		#if flag_block1==False and flag_block2==False and flag_block3==False:
		if flag_block2==False and flag_block3==False:
			status,condition=check_goto(statements,label)
			if status==True:
				statements=gotomoveout_inside(statements,label)
				flag_block1=check_label_block(statements,label)
				flag_block2=check_label_block_sp(statements,label)
				flag_block3=check_goto_block_Sp(statements,label)
				#if flag_block1==False and flag_block2==False and flag_block3==True:
				if flag_block2==False and flag_block3==True:
					statements=gotomovein(statements,label)
	return statements







#Finding Goto in a If Block to Call gotomovein
#Parameter pass statement 
#Label

def label_finder_if(statement,label):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if statement.iftrue.block_items is not None:
				new_iftrue=c_ast.Compound(block_items=label_finder(statement.iftrue.block_items,label))
			else:
				new_iftrue=statement.iftrue
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_iffalse=c_ast.Compound(block_items=label_finder(statement.iffalse.block_items,label))	
			else:
				new_iffalse=statement.iffalse
		elif type(statement.iffalse) is c_ast.If:
			new_iffalse=label_finder_if(statement.iffalse,label)
		else:
			new_iffalse=statement.iffalse
	return c_ast.If(cond=statement.cond,iftrue=new_iftrue,iffalse=new_iffalse)






#Method to Move Goto Outside
#Parameter pass statement 
#Label


def gotomoveout(statements,label):
	flag_block1=check_label_block(statements,label)
	update_statements=[]
	condition=None
	if flag_block1==True:
		for statement in statements:
			if type(statement) is c_ast.If:
				flag_block2,condition=check_goto_If(statement,label)
				flag_stmt2=check_goto_block_If(statement,label)
				if flag_block2==True and flag_stmt2==False:
					statement=gotomoveoutrec_if(statement,label)
			                update_statements.append(statement)
			                update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
				elif flag_block2==True and flag_stmt2==True:
					statement=getRidOfGoto(statement,label)
			                if statement is not None:
			                	update_statements.append(statement)
			                	update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
			        else:
					update_statements.append(statement)
			
			elif type(statement) is c_ast.While:
				flag_block2,condition=check_goto(statement.stmt.block_items,label)
				flag_stmt2=check_goto_block(statement.stmt.block_items,label)
				if flag_block2==True and flag_stmt2==False:
					stmts=gotomoveoutrec(statement.stmt.block_items,label)
					stmts.append(c_ast.If(cond=condition, iftrue=c_ast.Break(), iffalse=None))
					statement=c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=stmts))
					update_statements.append(statement)
					update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
				elif flag_block2==True and flag_stmt2==True:
			                update_statements.append(statement)
			        else:
					update_statements.append(statement)
			                       
			else:
				update_statements.append(statement)
                                
		return update_statements




#Method to Move Goto Outside
#Parameter pass statement 
#Label


def gotomoveout_inside(statements,label):
	update_statements=[]
	condition=None
	for statement in statements:
		if type(statement) is c_ast.If:
			flag_block2,condition=check_goto_If(statement,label)
			flag_stmt2=check_goto_block_If(statement,label)
			if flag_block2==True and flag_stmt2==False:
				statement=gotomoveoutrec_if(statement,label)
			        update_statements.append(statement)
			        update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
			elif flag_block2==True and flag_stmt2==True:
				statement=getRidOfGoto(statement,label)
			        if statement is not None:
			                update_statements.append(statement)
			                update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
			else:
				update_statements.append(statement)
			
		elif type(statement) is c_ast.While:
			flag_block2,condition=check_goto(statement.stmt.block_items,label)
			flag_stmt2=check_goto_block(statement.stmt.block_items,label)
			if flag_block2==True and flag_stmt2==False:
				stmts=gotomoveoutrec(statement.stmt.block_items,label)
				stmts.append(c_ast.If(cond=condition, iftrue=c_ast.Break(), iffalse=None))
				statement=c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=stmts))
				update_statements.append(statement)
				update_statements.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
			elif flag_block2==True and flag_stmt2==True:
			        update_statements.append(statement)
			else:
				update_statements.append(statement)
			                       
		else:
			update_statements.append(statement)
                                
	return update_statements












#Method to Move Goto Outside Recursive
#Parameter pass statement 
#Label

def gotomoveoutrec(statements,label):
	new_statements1=[]
	new_statements2=[]
	flag=False
	condition=None
	for statement in statements:
		if type(statement) is c_ast.If:
			flag_block2,condition_new=check_goto_If(statement,label)
			flag_stmt2=check_goto_block_If(statement,label)
			if condition_new is not None:
				condition=condition_new
			if flag_block2==True and flag_stmt2==False:
				statement=gotomoveoutrec_if(statement,label)
                        	new_statements1.append(statement)
                        	flag=True
			elif flag_block2==True and flag_stmt2==True:
				statement=getRidOfGoto(statement,label)
                                flag=True
                                if statement is not None:
                                	new_statements1.append(statement)
                        else:
                        	if flag==True:
					new_statements2.append(statement)
				else:
                        		new_statements1.append(statement)

		elif type(statement) is c_ast.While:
			flag_block2,condition_new=check_goto(statement.stmt.block_items,label)
			flag_stmt2=check_goto_block(statement.stmt.block_items,label)
			if condition_new is not None:
				condition=condition_new
			if flag_block2==True and flag_stmt2==False:
				stmts=gotomoveoutrec(statement.stmt.block_items,label)
				stmts.append(c_ast.If(cond=condition, iftrue=c_ast.Break(), iffalse=None))
				statement=c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=stmts))
				new_statements1.append(statement)
			elif flag_block2==True and flag_stmt2==True:
                                flag=True
                                new_statements1.append(statement)
                        else:
                        	if flag==True:
					new_statements2.append(statement)
				else:
                        		new_statements1.append(statement)
                       
                else:
                	if flag==True:
				new_statements2.append(statement)
			else:
                        	new_statements1.append(statement)
	if condition is not None:
                if len(new_statements2)>0:
                	new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
        	statements=new_statements1

        return statements



#Finding Goto in a Block to Call gotomovein
#Parameter pass block of statement 
#Label
				
				
def gotomoveoutrec_if(statement,label):
	#print statement.show()
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Goto:
			if statement.iftrue.name==label:
	                	status = True
		else:
		        if type(statement.iftrue) is c_ast.Compound and statement.iftrue.block_items is not None:
		        	flag_block2,condition=check_goto(statement.iftrue.block_items,label)
				flag_stmt2=check_goto_block(statement.iftrue.block_items,label)
				if flag_block2==True and flag_stmt2==False:
					statement.iftrue.block_items=gotomoveoutrec(statement.iftrue.block_items,label)
					statement.iftrue=c_ast.Compound(block_items=statement.iftrue.block_items)
				elif flag_block2==True and flag_stmt2==True:
					statement.iftrue=c_ast.Compound(block_items=statement.iftrue.block_items)
	                                                                
		if type(statement.iffalse) is c_ast.Label:
	        	if statement.iffalse.name==label:
	                	status = True
		else:
			if type(statement.iffalse) is c_ast.Compound and statement.iffalse.block_items is not None:
				flag_block2,condition=check_goto(statement.iffalse.block_items,label)
				flag_stmt2=check_goto_block(statement.iffalse.block_items,label)
				if flag_block2==True and flag_stmt2==False:
					statement.iffalse.block_items=gotomoveoutrec(statement.iffalse.block_items,label)
					statement.iffalse=c_ast.Compound(block_items=statement.iffalse.block_items)
				elif flag_block2==True and flag_stmt2==True:
					statement.iffalse=c_ast.Compound(block_items=statement.iffalse.block_items)
			else:
				if type(statement.iffalse) is c_ast.If: 
					gotomoveoutrec_if(statement.iffalse,label)
	#print statement.show()
	return c_ast.If(cond=statement.cond, iftrue=statement.iftrue, iffalse=statement.iffalse)
				



#Updating Each If Else for Goto
#Parameter pass statement 
#Label
		
	
def getRidOfGoto(statement,label):
	generator = c_generator.CGenerator()
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Goto:
			if statement.iftrue.name==label:
	                	new_iftrue=None
		else:
		        if type(statement.iftrue) is c_ast.Compound:
		        	new_block=[]
				for stmt in statement.iftrue.block_items:
					if type(stmt) is c_ast.Goto:
						if stmt.name!=label:
							new_block.append(stmt)
					else:
						new_block.append(stmt)
				new_iftrue=c_ast.Compound(block_items=new_block)
                                     
		
		if type(statement.iffalse) is c_ast.Label:
	        	if statement.iffalse.name==label:
	                	new_iffalse=None
		else:
			if type(statement.iffalse) is c_ast.Compound:
				new_block=[]
				for stmt in statement.iffalse.block_items:
					if type(stmt) is c_ast.Goto:
						if stmt.name!=label:
							new_block.append(stmt)
					else:
						new_block.append(stmt)
				new_iffalse=c_ast.Compound(block_items=new_block)
			else:
				if type(statement.iffalse) is c_ast.If:
					new_iffalse=getRidOfGoto(statement.iffalse,label)
	if new_iftrue is not None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
	else:
		return None





#Finding Goto in a Block to Call gotomovein
#Parameter pass block of statement 
#Label


def goto_finder(statements,label):
	flag_block1=check_goto_block_Sp(statements,label)
	if flag_block1==True:
		flag_block1=check_label_block_sp(statements,label)
		if flag_block1==True:
			return statements
		else:
			return gotomovein(statements,label)
	else:
		update_statements=[]
		for statement in statements:
			if type(statement) is c_ast.If:
				update_statements.append(goto_finder_if(statement,label))
			elif type(statement) is c_ast.While:
				update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=goto_finder(statement.stmt.block_items,label))))
			else:
				update_statements.append(statement)
		return update_statements


#Finding Goto in a If Block to Call gotomovein
#Parameter pass statement 
#Label

def goto_finder_if(statement,label):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement) is c_ast.If:
			if type(statement.iftrue) is c_ast.Compound:
				if statement.iftrue.block_items is not None:
					new_iftrue=c_ast.Compound(block_items=goto_finder(statement.iftrue.block_items,label))
				else:
					new_iftrue=statement.iftrue				
			else:
				new_iftrue=statement.iftrue
			if type(statement.iffalse) is c_ast.Compound:
				if statement.iffalse.block_items is not None:
					new_iffalse=c_ast.Compound(block_items=goto_finder(statement.iffalse.block_items,label))
				else:
					new_iffalse=statement.iffalse
			elif type(statement.iffalse) is c_ast.If:
				new_iffalse=goto_finder_if(statement.iffalse,label)
			else:
				new_iffalse=statement.iffalse
	return c_ast.If(cond=statement.cond,iftrue=new_iftrue,iffalse=new_iffalse)




#Method to Move Goto Inside
#Parameter pass statement 
#Label

def gotomovein(statements,label):
	flag_block1=check_goto_block_Sp(statements,label)
	new_statements1=[]
	new_statements2=[]
	flag=False
	if flag_block1==True:
		flag_block1,condition=check_goto(statements,label)
		for statement in statements:
			if type(statement) is c_ast.If:
				flag_stmt3=check_goto_block_If(statement,label)				
				flag_block2=check_label_If(statement,label)
				flag_stmt2=check_label_block_If(statement,label)
				if flag_stmt3==True:
					if flag_block2==True and flag_stmt2==True:
						new_statements1.append(statement)
					else:
						para_list=[]
                                                para_list.append(condition)
						newFun=c_ast.FuncCall(name=c_ast.ID(name='_Bool2Int'), args=c_ast.ExprList(exprs=para_list))
						new_statement=c_ast.Assignment(op='=', lvalue=c_ast.ID(name='bool_go_'+label), rvalue=newFun)
						new_variable['bool_go_'+label]='bool_go_'+label
						condition=c_ast.BinaryOp(op='>', left=c_ast.ID(name='bool_go_'+label), right=c_ast.Constant(type='int', value='0'))
						new_statements1.append(new_statement)
						flag=True
				else:
					if flag_block2==True and flag_stmt2==False:
						flag=False
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
						new_statements1.append(updateIfBlock(statement,label,condition))

						new_statements2=[]
					else:
						if flag_block2==True and flag_stmt2==True:
							flag=False
							new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
							new_statements1.append(updateIfBlock(statement,label,condition))
							new_statements2=[]
						else:
							if flag==False:
								new_statements1.append(statement)
							else:
								new_statements2.append(statement)
			elif type(statement) is c_ast.While:
				flag_block2=check_label(statement.stmt.block_items,label)
				#flag_stmt2=check_label_block(statement.stmt.block_items,label)
				flag_stmt2=check_label_block_sp(statement.stmt.block_items,label)			
				if flag_block2==False and flag_stmt2==False:
					statement=c_ast.While(cond=statement.cond, stmt=statement.stmt)
				elif flag_block2==True and flag_stmt2==True:
					if len(new_statements2)>0:
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
					new_cond=c_ast.BinaryOp(op='||', left=condition, right=statement.cond)
					new_blocks=[]
					new_blocks.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.stmt.block_items:
						new_blocks.append(stmt)
					new_blocks.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='bool_go_'+label) , rvalue= c_ast.Constant(type='int', value='0')))
					statement=c_ast.While(cond=new_cond, stmt=c_ast.Compound(block_items=new_blocks))
					flag=False
					new_statements2=[]
				elif flag_block2==True and flag_stmt2==False:
					if len(new_statements2)>0:
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
					new_cond=c_ast.BinaryOp(op='||', left=condition, right=statement.cond)
					new_blocks=[]
					new_blocks.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.stmt.block_items:
						new_blocks.append(stmt)
					new_blocks.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='bool_go_'+label) , rvalue= c_ast.Constant(type='int', value='0')))
					new_blocks=gotomoveinrec(new_blocks,label,condition)
					statement=c_ast.While(cond=new_cond, stmt=c_ast.Compound(block_items=new_blocks))
					flag=False
					new_statements2=[]
				else:
					statement=c_ast.While(cond=statement.cond, stmt=statement.stmt)
				if flag==False:
					new_statements1.append(statement)
				else:
					new_statements2.append(statement)
			else:
				if flag==False:
					new_statements1.append(statement)
				else:
					new_statements2.append(statement)

		return new_statements1
	else:
		return statements



#Method to Move Goto Inside Recursive 
#Parameter pass statement 
#Label


def gotomoveinrec(statements,label,condition):
	flag_block1,condition=check_goto(statements,label)
	new_statements1=[]
	new_statements2=[]
	flag=False
	if flag_block1==True:
		for statement in statements:
			if type(statement) is c_ast.If:
				flag_stmt3=check_goto_block_If(statement,label)				
				flag_block2=check_label_If(statement,label)
				flag_stmt2=check_label_block_If(statement,label)
				if flag_stmt3==True:
					if flag_block2==True and flag_stmt2==True:
						new_statements1.append(statement)
					else:
						flag=True
				else:
					if flag_block2==True and flag_stmt2==False:
						flag=False
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
						new_statements1.append(updateIfBlock(statement,label,condition))

						new_statements2=[]
					else:
						if flag_block2==True and flag_stmt2==True:
							flag=False
							if len(new_statements2)>0:
								new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
							new_statements1.append(updateIfBlock(statement,label,condition))
							new_statements2=[]
						else:
							if flag==False:
								new_statements1.append(statement)
							else:
								new_statements2.append(statement)
			elif type(statement) is c_ast.While:
				flag_block2=check_label(statement.stmt.block_items,label)
				#flag_stmt2=check_label_block(statement.stmt.block_items,label)
				flag_stmt2=check_label_block_sp(statement.stmt.block_items,label)
				if flag_block2==False and flag_stmt2==False:
					statement=c_ast.While(cond=statement.cond, stmt=statement.stmt)
				elif flag_block2==True and flag_stmt2==True:
					if len(new_statements2)>0:
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
					new_cond=c_ast.BinaryOp(op='||', left=condition, right=statement.cond)
					new_blocks=[]
					new_blocks.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.stmt.block_items:
						new_blocks.append(stmt)
					new_blocks.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='bool_go_'+label) , rvalue= c_ast.Constant(type='int', value='0')))
					statement=c_ast.While(cond=new_cond, stmt=c_ast.Compound(block_items=new_blocks))
					flag=False
					new_statements2=[]
				elif flag_block2==True and flag_stmt2==False:
					if len(new_statements2)>0:
						new_statements1.append(c_ast.If(cond=c_ast.UnaryOp(op='!', expr=condition), iftrue=c_ast.Compound(block_items=new_statements2), iffalse=None))
					new_cond=c_ast.BinaryOp(op='||', left=condition, right=statement.cond)
					new_blocks=[]
					new_blocks.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.stmt.block_items:
						new_blocks.append(stmt)
					new_blocks.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='bool_go_'+label) , rvalue= c_ast.Constant(type='int', value='0')))
					new_blocks=gotomoveinrec(new_blocks,label,condition)
					statement=c_ast.While(cond=new_cond, stmt=c_ast.Compound(block_items=new_blocks))
					flag=False
					new_statements2=[]
				else:
					statement=c_ast.While(cond=statement.cond, stmt=statement.stmt)
				if flag==False:
					new_statements1.append(statement)
				else:
					new_statements2.append(statement)
			else:
				if flag==False:
					new_statements1.append(statement)
				else:
					new_statements2.append(statement)
		return new_statements1
	else:
		return statements




#Updating Each If Else for Goto
#Parameter pass statement 
#Label

def updateIfBlock(statement,label,condition):
	new_iftrue=None
	new_iffalse=None
	new_condtion=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Goto:
			if statement.iftrue.name==label:
				new_block=[]
				new_block.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
				new_block.append(statement.iftrue)
		        	new_iftrue=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iftrue) is c_ast.Compound:
				flag_stmt=check_label(statement.iftrue.block_items,label)
				flag_stmt_block=check_label_block_sp(statement.iftrue.block_items,label)
			        if flag_stmt==True:
			        	new_block=[]
			        	new_block.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.iftrue.block_items:
						new_block.append(stmt)
					if flag_stmt_block==False:
						new_block=gotomoveinrec(new_block,label,condition)
					new_iftrue=c_ast.Compound(block_items=new_block)
				else:
					new_condtion=c_ast.BinaryOp(op='&&', left=c_ast.UnaryOp(op='!', expr=condition), right=statement.cond)
					new_iftrue=statement.iftrue
                         
			
		if type(statement.iffalse) is c_ast.Label:
			new_block=[]
			new_block.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
			new_block.append(statement.iffalse)
		        new_iftrue=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iffalse) is c_ast.Compound:
				flag_stmt=check_label(statement.iffalse.block_items,label)
				flag_stmt_block=check_label_block_sp(statement.iffalse.block_items,label)
				if flag_stmt==True:
			        	new_block=[]
			        	new_block.append(c_ast.If(cond=condition, iftrue=c_ast.Goto(name=label), iffalse=None))
					for stmt in statement.iffalse.block_items:
						new_block.append(stmt)
					if flag_stmt_block==False:
						new_block=gotomoveinrec(new_block,label,condition)
					new_iffalse=c_ast.Compound(block_items=new_block)
				else:
					new_condtion=c_ast.BinaryOp(op='&&', left=c_ast.UnaryOp(op='!', expr=condition), right=statement.cond)
					new_iffalse=statement.iffalse
			else:
				if type(statement.iffalse) is c_ast.If:
					new_iffalse=updateIfBlock(statement.iffalse,label,condition)
	if new_condtion is not None:
		return c_ast.If(cond=new_condtion, iftrue=new_iftrue, iffalse=new_iffalse)
	else:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
	
	
	

def reOrganizeBreaks(statements,new_break_map):
	update_statement=[]
	if statements is not None:
		for statement in statements:
			if type(statement) is c_ast.If:
				statement=reOrganizeBreaksIf(statement,new_break_map)
				update_statement.append(statement)
			elif type(statement) is c_ast.Break:
				update_statement.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='do_break'+str(len(new_break_map.keys())+1)), rvalue=c_ast.Constant(type='int', value='1')))
				new_break_map['do_break'+str(len(new_break_map.keys())+1)]='do_break'+str(len(new_break_map.keys())+1)
				update_statement.append(statement)
			else:
				update_statement.append(statement)
		return update_statement
	else:
		return None


def reOrganizeBreaksIf(statement,new_break_map):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Break:
			new_block=[]
			new_block.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='do_break'+str(len(new_break_map.keys())+1)), rvalue=c_ast.Constant(type='int', value='1')))
			new_break_map['do_break'+str(len(new_break_map.keys())+1)]='do_break'+str(len(new_break_map.keys())+1)
			new_block.append(statement.iftrue)
			new_iftrue=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iftrue) is c_ast.Compound:
				new_block=reOrganizeBreaks(statement.iftrue.block_items,new_break_map)
				new_iftrue=c_ast.Compound(block_items=new_block)
		
		if type(statement.iffalse) is c_ast.Break:
			new_block=[]
			new_block.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='do_break'+str(len(new_break_map.keys())+1)), rvalue=c_ast.Constant(type='int', value='1')))
			new_break_map['do_break'+str(len(new_break_map.keys())+1)]='do_break'+str(len(new_break_map.keys())+1)
			new_block.append(statement.iffalse)
			new_iffalse=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iffalse) is c_ast.Compound:
				new_block=reOrganizeBreaks(statement.iffalse.block_items,new_break_map)
				new_iffalse=c_ast.Compound(block_items=new_block)
			else:
				if type(statement.iffalse) is c_ast.If:
					new_iffalse=reOrganizeBreaksIf(statement.iffalse,new_break_map)
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
		
		
		
def addingBreakVariables(statements,new_break_map):
	for variable in new_break_map.keys():
		global new_variable
		new_variable[variable]=variable
		new_block=[]
		new_block.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=variable), rvalue=c_ast.Constant(type='int', value='0')))
		new_block.append(c_ast.Break())
		new_iftrue=c_ast.Compound(block_items=new_block)
		statements.append(c_ast.If(cond=c_ast.BinaryOp(op='==', left=c_ast.ID(name=variable), right=c_ast.Constant(type='int', value='1')), iftrue=new_iftrue, iffalse=None))
	return statements
	
	

def removeEmptyIfLoop(statements):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.If:
			statement=removeEmptyIfLoop_If(statement)
			if statement is not None:
				update_statements.append(statement)
		elif type(statement) is c_ast.While:
			new_block_items=removeEmptyIfLoop(statement.stmt.block_items)
			update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=new_block_items)))
		else:
			if statement is not None:
				if type(statement) is not c_ast.EmptyStatement:
					update_statements.append(statement)
	return update_statements
			
			
			
def removeEmptyIfLoop_If(statement):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			if len(statement.iftrue.block_items)==0:
				new_iftrue=None
			else:
				new_block=removeEmptyIfLoop(statement.iftrue.block_items)
				if len(new_block)==0:
					new_iftrue=None
				else:
					new_iftrue=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iftrue) is c_ast.EmptyStatement:
				new_iftrue=None
			else:
				new_iftrue=statement.iftrue
				
		if type(statement.iffalse) is c_ast.Compound:
			if len(statement.iffalse.block_items)==0:
				new_iffalse=None
			else:
				new_block=removeEmptyIfLoop(statement.iffalse.block_items)
				if len(new_block)==0:
					new_iffalse=None 
				else:
					new_iffalse=c_ast.Compound(block_items=new_block) 
		elif type(statement.iffalse) is c_ast.If:
			result=removeEmptyIfLoop_If(statement.iffalse)
			if result is not None:
				new_iffalse=result
		else:
			if type(statement.iffalse) is c_ast.EmptyStatement:
				new_iftrue=None
			else:
				new_iffalse=statement.iffalse
	
	
	if new_iftrue is not None and new_iffalse is None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=None)
	elif new_iftrue is not None and new_iffalse is not None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.Compound:
		return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=new_iffalse, iffalse=None)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.If:
		return new_iffalse
	else:
		return None

		
		
def returnReplacement(statements,end_label_map):
	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.If:
			statement=returnReplacementIf(statement,end_label_map)
			if statement is not None:
				update_statements.append(statement)
		elif type(statement) is c_ast.While:
			new_block_items=returnReplacement(statement.stmt.block_items,end_label_map)
			update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=new_block_items)))
		elif type(statement) is c_ast.Return:
			if statement.expr is not None:
				label='Label'+str(len(end_label_map.keys())+1)
				update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='RET'), rvalue=statement.expr))
				update_statements.append(c_ast.Goto(name=label))
				end_label_map[label]=label
			else:
				label='Label'+str(len(end_label_map.keys())+1)
				update_statements.append(c_ast.Goto(name=label))
				end_label_map[label]=label
		elif type(statement) is c_ast.Label:
			update_statements.append(c_ast.Label(name=statement.name, stmt=None))
			if type(statement.stmt) is c_ast.Return:
				if statement.stmt.expr is not None:
					label='Label'+str(len(end_label_map.keys())+1)
					update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='RET'), rvalue=statement.stmt.expr))
					update_statements.append(c_ast.Goto(name=label))
					end_label_map[label]=label
				else:
					label='Label'+str(len(end_label_map.keys())+1)
					update_statements.append(c_ast.Goto(name=label))
					end_label_map[label]=label
			else:
				if statement.stmt is not None:
					update_statements.append(statement.stmt)
			
		else:
			update_statements.append(statement)
	return update_statements
	
	
	
	
	
	
def returnReplacementIf(statement,end_label_map):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Return:
			new_block=[]
			if statement.iftrue.expr is not None:
				label='Label'+str(len(end_label_map.keys())+1)
				new_block.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='RET'), rvalue=statement.iftrue.expr))
				new_block.append(c_ast.Goto(name=label))
				end_label_map[label]=label
			else:
				label='Label'+str(len(end_label_map.keys())+1)
				new_block.append(c_ast.Goto(name=label))
				end_label_map[label]=label
			new_iftrue=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iftrue) is c_ast.Compound:
				new_block=returnReplacement(statement.iftrue.block_items,end_label_map)
				new_iftrue=c_ast.Compound(block_items=new_block)
			else:
                                new_iftrue=statement.iftrue
			
		if type(statement.iffalse) is c_ast.Return:
			new_block=[]
			if statement.iffalse.expr is not None:
				label='Label'+str(len(end_label_map.keys())+1)
				new_block.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='RET'), rvalue=statement.iffalse.expr))
				new_block.append(c_ast.Goto(name=label))
				end_label_map[label]=label
			else:
				label='Label'+str(len(end_label_map.keys())+1)
				new_block.append(c_ast.Goto(name=label))
				end_label_map[label]=label
			new_iffalse=c_ast.Compound(block_items=new_block)
		else:
			if type(statement.iffalse) is c_ast.Compound:
				new_block=returnReplacement(statement.iffalse.block_items,end_label_map)
				new_iffalse=c_ast.Compound(block_items=new_block)
			else:
				if type(statement.iffalse) is c_ast.If:
					new_iffalse=returnReplacementIf(statement.iffalse,end_label_map)
				else:
                                        new_iffalse=statement.iffalse
	return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)









"""
 
Goto removal Modules End 

"""


break_count=0

continue_count=0	
	


def getBreakStmt(statements,break_map):
	update_statement1=[]
	update_statement2=[]
	flag=False
	global break_count
	global continue_count
        global new_variable
	for statement in statements:
		if type(statement) is c_ast.If:
			if flag==False:
				break_map_temp={}
				statement=getBreakStmtIf(statement,break_map_temp)
				for e_break in break_map_temp.keys():
					break_map[e_break]=break_map_temp[e_break]
				update_statement1.append(statement)
				if len(break_map_temp.keys())>0:
					flag=True
			else:
				update_statement2.append(statement)
		elif type(statement) is c_ast.While:
			break_map_temp={}
			new_block_items1=getBreakStmt(statement.stmt.block_items,break_map_temp)
			new_block_items2=[]
			new_condtion=statement.cond
			if len(break_map_temp.keys())>0:
				for var_name in break_map_temp.keys():
                                        new_block_items2.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='0')))
					if break_map_temp[var_name]=='Break':
						temp_new_condition=c_ast.BinaryOp(op='&&', left=new_condtion, right=c_ast.BinaryOp(op='==', left=c_ast.ID(name=var_name), right=c_ast.Constant(type='int', value='0')))
						new_condtion=temp_new_condition
			
                        for item in new_block_items1:
                            new_block_items2.append(item)
			if flag==False:
				update_statement1.append(c_ast.While(cond=new_condtion, stmt=c_ast.Compound(block_items=new_block_items2)))
			else:
				update_statement2.append(c_ast.While(cond=new_condtion, stmt=c_ast.Compound(block_items=new_block_items2)))
		elif type(statement) is c_ast.Break:
                        break_count=break_count+1
                        var_name='break_'+str(break_count)+'_flag'
                        new_variable[var_name]=var_name
                        update_statement1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Break'
		elif type(statement) is c_ast.Continue:
		        continue_count=continue_count+1
		       	var_name='continue_'+str(continue_count)+'_flag'
		        new_variable[var_name]=var_name
		        update_statement1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Continue'
		else:
			if flag==False:
				update_statement1.append(statement)
			else:
				update_statement2.append(statement)
	if flag==True:
		update_condition=None
		for var_name in break_map.keys():
			if update_condition is None:
				update_condition=c_ast.BinaryOp(op='==', left=c_ast.ID(name=var_name), right=c_ast.Constant(type='int', value='0'))
			else:
				update_condition=c_ast.BinaryOp(op='&&', left=update_condition, right=c_ast.BinaryOp(op='==', left=c_ast.ID(name=var_name), right=c_ast.Constant(type='int', value='0')))
		if len(update_statement2)>0:
			update_statement1.append(c_ast.If(cond=update_condition, iftrue=c_ast.Compound(block_items=update_statement2), iffalse=None))
		
		return getBreakStmt(update_statement1,break_map)
	else:
		return update_statement1
			
		




def getBreakStmtIf(statement,break_map):
	new_iftrue=None
	new_iffalse=None
	global break_count
	global new_variable
	global continue_count
	if type(statement) is c_ast.If:
			
		if type(statement.iftrue) is c_ast.Break:
                        new_block_items=[]
                        break_count=break_count+1
                        var_name='break_'+str(break_count)+'_flag'
                        new_variable[var_name]=var_name
                        new_block_items.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Break'
			new_iftrue=c_ast.Compound(block_items=new_block_items)
		elif type(statement.iftrue) is c_ast.Continue:
		        new_block_items=[]
		        break_count=break_count+1
		        var_name='continue_'+str(continue_count)+'_flag'
		        new_variable[var_name]=var_name
		        new_block_items.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Continue'
			new_iftrue=c_ast.Compound(block_items=new_block_items)
		elif type(statement.iftrue) is c_ast.Compound:
			new_block_items=getBreakStmt(statement.iftrue.block_items,break_map)
			new_iftrue=c_ast.Compound(block_items=new_block_items)
		else:
			new_iftrue=statement.iftrue
			
		if type(statement.iffalse) is c_ast.Break:
                        new_block_items=[]
                        break_count=break_count+1
                        var_name='break_'+str(break_count)+'_flag'
                        new_variable[var_name]=var_name
                        new_block_items.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Break'
			new_iffalse=c_ast.Compound(block_items=new_block_items)
		elif type(statement.iffalse) is c_ast.Continue:
		        new_block_items=[]
		        continue_count=continue_count+1
		        var_name='continue_'+str(continue_count)+'_flag'
		        new_variable[var_name]=var_name
		        new_block_items.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var_name), rvalue=c_ast.Constant(type='int', value='1')))
			break_map[var_name]='Continue'
			new_iffalse=c_ast.Compound(block_items=new_block_items)	
		elif type(statement.iffalse) is c_ast.Compound:
			new_block_items=getBreakStmt(statement.iffalse.block_items,break_map)
			new_iffalse=c_ast.Compound(block_items=new_block_items)
		else:
			if type(statement.iffalse) is c_ast.If:
				new_iffalse=getBreakStmtIf(statement.iffalse,break_map)
			else:
				new_iffalse=statement.iffalse
	if new_iftrue is not None and new_iffalse is None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=None)
	elif new_iftrue is not None and new_iffalse is not None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.Compound:
		return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=new_iffalse, iffalse=None)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.If:
		return new_iffalse
	else:
		return None





def arrangeEmptyStatement(statements):
    update_statements=[]
    for statement in statements:
        if type(statement) is c_ast.If:
            stmt=arrangeEmptyStatementIf(statement)
            if stmt is not None:
            	update_statements.append(stmt)
        elif type(statement) is c_ast.While:
            if type(statement.stmt) is c_ast.EmptyStatement:
                update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=[])))
            elif statement.stmt.block_items is not None:
            	stmt=arrangeEmptyStatement(statement.stmt.block_items)
            	if stmt is not None:
                	update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=stmt)))
                else:
                	update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=[])))
            else:
                update_statements.append(statement)
        else:
            update_statements.append(statement)
    return update_statements
           

    


def arrangeEmptyStatementIf(statement):
    new_iftrue=None
    new_iffalse=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.EmptyStatement:
            if type(statement.iffalse) is c_ast.Compound:
                return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=statement.iffalse, iffalse=None)
            else:
                return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=statement.iffalse, iffalse=None)
        elif type(statement.iftrue) is c_ast.Compound:
            if statement.iftrue.block_items is not None:
                new_block_items=arrangeEmptyStatement(statement.iftrue.block_items)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
            else:
                new_iftrue=statement.iftrue
        else:
            new_iftrue=statement.iftrue
            
        if type(statement.iffalse) is c_ast.Compound:
            if statement.iffalse.block_items is not None:
                new_block_items=arrangeEmptyStatement(statement.iffalse.block_items)
                new_iffalse=c_ast.Compound(block_items=new_block_items)
            else:
                new_iffalse=statement.iffalse
        elif type(statement.iffalse) is c_ast.If:
            new_iffalse=arrangeEmptyStatementIf(statement.iffalse)
        else:
            new_iffalse=statement.iffalse
            
    if new_iftrue is not None and new_iffalse is None:
        return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=None)
    elif new_iftrue is not None and new_iffalse is not None:
        return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
    elif new_iffalse is not None and type(new_iffalse) is c_ast.Compound:
	return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=new_iffalse, iffalse=None)
    elif new_iffalse is not None and type(new_iffalse) is c_ast.If:
	return new_iffalse
    else:
	return None




#
#Convert Initiation to assignments   
#

def construct_program(statements):
    update_statements=[]
    for statement in statements:
    	if type(statement) is c_ast.Decl:
    		if type(statement.type) is c_ast.ArrayDecl:
                        if statement.init is not None:
                        	program=''                        	
			        d_list=[]
			        a_list=[]
			        
			        if statement.type.dim is None:
			        	d_list_update,a_list_update=getDimesnion4Init(statement.init)
			        	for x1 in d_list_update:
			        		d_list.append('initial_value'+x1)
			        	for x1 in a_list_update:
			        		a_list.append(x1)
			        else:
			        	for x in range(0, int(statement.type.dim.value)):
			        		d_list.append('initial_value.exprs['+str(x)+']')
			                	a_list.append('['+str(x)+']') 
			        	d_list,a_list=getDimesnion(statement.type,d_list,a_list)
                        	initial_value=statement.init
                        	for x1 in range(0, len(d_list)):
                                        stmt_value=eval(d_list[x1])
                                        if type(stmt_value) is c_ast.Constant:
                                            program=program+statement.name+a_list[x1]+'='+str(eval(d_list[x1]+'.value'))+';'
                                        else:
                                            if type(stmt_value) is c_ast.UnaryOp: 
                                                program=program+statement.name+a_list[x1]+'= '+stmt_value.op+str(eval(d_list[x1]+'.expr.value'))+';'
                        	
                        	program='int main{'+program+'}'
                        	parser = c_parser.CParser()
                        	ast1 = parser.parse(program)
                        	function_body = ast1.ext[0].body                        	
                        	statement.init=None
                        	update_statements.append(statement)
                        	for new_statement in function_body.block_items:
                        		update_statements.append(new_statement)
                        else:
                        	update_statements.append(statement)
                        
                else:
                	update_statements.append(statement)
        else:
        	update_statements.append(statement)
    return update_statements




dummyCount=0
    
def functionToAssignment(statements,functionMap):
 	global dummyCount
 	update_statements=[]
	for statement in statements:
		if type(statement) is c_ast.FuncCall:
			if  '__VERIFIER' not in statement.name.name:
				dummyCount=dummyCount+1
				update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='_'+str(dummyCount)+'DUMMY'), rvalue=statement))
			else:
				update_statements.append(statement)
		elif type(statement) is c_ast.If:
	                	update_statements.append(functionToAssignmentIf(statement,functionMap))
	        elif type(statement) is c_ast.While:
	        	if type(statement.stmt) is c_ast.Compound:
	                	update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=functionToAssignment(statement.stmt.block_items,functionMap))))
			else:
				if statement.stmt is not None:
					if type(statement) is c_ast.EmptyStatement:
						new_block=[]
						update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=new_block)))	
					else:
						new_block=[]
						new_block.append(statement.stmt)
						update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=functionToAssignment(new_block,functionMap))))
				else:
			        	update_statements.append(statement)
		else:
                	update_statements.append(statement)
        return update_statements
                	
                	
                	
def functionToAssignmentIf(statement,functionMap):
      new_iftrue=None
      new_iffalse=None
      global dummyCount
      if type(statement) is c_ast.If:
          if type(statement.iftrue) is c_ast.Compound:
	  	new_block_items=functionToAssignment(statement.iftrue.block_items,functionMap)
                new_iftrue=c_ast.Compound(block_items=new_block_items)
          elif type(statement.iftrue) is c_ast.FuncCall:
          	if  '__VERIFIER' not in statement.iftrue.name.name:
	  		dummyCount=dummyCount+1
	  		new_iftrue=c_ast.Assignment(op='=',lvalue=c_ast.ID(name='_'+str(dummyCount)+'DUMMY'), rvalue=statement.iftrue)
	  	else:
	  		new_iftrue=statement.iftrue
          else:
               new_iftrue=statement.iftrue
              
          if type(statement.iffalse) is c_ast.Compound:
              if statement.iffalse.block_items is not None:
                  new_block_items=functionToAssignment(statement.iffalse.block_items,functionMap)
                  new_iffalse=c_ast.Compound(block_items=new_block_items)
              else:
                  new_iffalse=statement.iffalse
          elif type(statement.iffalse) is c_ast.FuncCall:
          	if  '__VERIFIER' not in statement.iffalse.name.name:
	      		dummyCount=dummyCount+1
	      		new_iffalse=c_ast.Assignment(op='=',lvalue=c_ast.ID(name='_'+str(dummyCount)+'DUMMY'), rvalue=statement.iffalse)
	      	else:
	      		new_iffalse=statement.iffalse
          elif type(statement.iffalse) is c_ast.If:
              new_iffalse=functionToAssignmentIf(statement.iffalse,functionMap)
          else:
              new_iffalse=statement.iffalse
      return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
      
      


def getDummyFunction(f,o,a,cm):
	new_o={}
	for eq in o.keys():
		if o[eq][0]=='e':
			lefthandstmt=expr2string1(o[eq][1])
			if 'DUMMY' in lefthandstmt:
				new_eq=[]
				new_eq.append('s0')
				new_eq.append(o[eq][2])
				new_o[eq]=new_eq
			else:
				new_o[eq]=o[eq]
		else:
			new_o[eq]=o[eq]
	#return f,new_o,a,cm
	return f,o,a,cm


#def update__VERIFIER_nondet(f,o,a,cm):
#    for eq in a:
#        if eq[0]=='i1':
#            var_cstr_map={}
#            lhs=expr2z3(eq[3],var_cstr_map)
#            eq[4]=update__VERIFIER_nondet_stmt(eq[4],var_cstr_map)
#    return f,o,a,cm




def update__VERIFIER_nondet_stmt(e,var_map):
    args=expr_args(e)
    if '__VERIFIER_nondet' in e[0] and len(args)==0:
        if e[0] in var_map.keys():
            VC=var_map[e[0]]
            VC=VC+1
            key=e[0]
            var_map[key]=VC
            e[0] = e[0]+str(VC)
            return e
        else:
            key=e[0]
            var_map[key]=2
            e[0] = e[0]+str(2)
            return e
    else:
        return e[:1]+list(update__VERIFIER_nondet_stmt(x,var_map) for x in expr_args(e))







def getVariablesInit(statements):
    update_statement=[]
    for decl in statements:
        if type(decl) is c_ast.Decl:
            if type(decl.type) is not c_ast.ArrayDecl:
                if decl.init is not None and '_PROVE' not in decl.name:
                    new_word=None
                    if new_word is None:
                        new_word=copy.deepcopy(decl.init)
                    decl=c_ast.Decl(name=decl.name, quals=decl.quals, storage=decl.storage, funcspec=decl.funcspec, type=c_ast.TypeDecl(declname=decl.type.declname, quals=decl.type.quals, type=decl.type.type), init=None, bitsize=decl.bitsize)
                    update_statement.append(decl)
                    if '_PROVE' not in decl.name:
                        if new_word is not None:
                            update_statement.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=decl.name), rvalue=new_word))
                else:
                    update_statement.append(decl)
            else:
                update_statement.append(decl)
        elif type(decl) is c_ast.While:
        	new_block_temp=getVariablesInit(decl.stmt.block_items)
                update_statement.append(c_ast.While(cond=decl.cond, stmt=c_ast.Compound(block_items=new_block_temp)))
        elif type(decl) is c_ast.If:
                update_statement.append(getVariablesInit_If(decl))
        else:
             update_statement.append(decl)
    return update_statement


def getVariablesInit_If(statement):
	If_stmt=None
        Else_stmt=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			new_block_temp=getVariablesInit(statement.iftrue.block_items)
                        If_stmt=c_ast.Compound(block_items=new_block_temp)
                else:
                    If_stmt=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			if statement.iffalse.block_items is not None:
				new_block_temp=getVariablesInit(statement.iffalse.block_items)
				Else_stmt=c_ast.Compound(block_items=new_block_temp)
                        else:
                            Else_stmt=statement.iffalse
		else:
			if type(statement.iffalse) is c_ast.If:
				Else_stmt=getVariablesInit_If(statement.iffalse)
                        else:
                                Else_stmt=statement.iffalse
	return c_ast.If(cond=statement.cond, iftrue=If_stmt, iffalse=Else_stmt)



#Get All Struct Variables

def updatePointerStruct(statements,struct_map):
    update_statements=[]
    for statement in statements:
        if type(statement) is c_ast.Decl:
            if type(statement.type.type) is c_ast.Struct:
                if statement.type.type.name in struct_map.keys():
                    structobject=struct_map[statement.type.type.name]
                    if structobject.getIsPointer()==True:
                        statement=c_ast.Decl(name=statement.name, quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=c_ast.PtrDecl(quals=[], type=statement.type), init=statement.init, bitsize=statement.bitsize)
                        update_statements.append(statement)
                    else:
                        update_statements.append(statement)
                else:
                    update_statements.append(statement)
            else:
                update_statements.append(statement)
        elif type(statement) is c_ast.Assignment:
            if type(statement.rvalue) is c_ast.Cast:
                if type(statement.rvalue.to_type.type.type) is c_ast.Struct:
                    if statement.rvalue.to_type.type.type.name in struct_map.keys():
                        structobject=struct_map[statement.rvalue.to_type.type.type.name]
                        if structobject.getIsPointer()==True:
                            stmt=c_ast.Typename(name = statement.rvalue.to_type.name, quals = statement.rvalue.to_type.quals, type=c_ast.PtrDecl(quals=[], type=statement.rvalue.to_type.type))
                            update_statements.append(c_ast.Assignment(op=statement.op,lvalue=statement.lvalue,rvalue=c_ast.Cast(to_type=stmt, expr=statement.rvalue.expr)))
                        else:
                            update_statements.append(statement)
                    else:
                        update_statements.append(statement)
                else:
                    update_statements.append(statement)
            else:
                update_statements.append(statement)
        elif type(statement) is c_ast.While:
            stmts = updatePointerStruct(statement.stmt.block_items,struct_map)
            statement=c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=stmts))
            update_statements.append(statement)
        elif type(statement) is c_ast.If:
            update_statements.append(updatePointerStructIf(statement,struct_map))
        else:
            update_statements.append(statement)
    return update_statements






def declarationModifying(statement):
    if type(statement.type) is c_ast.PtrDecl:
        degree=0
        parser = c_parser.CParser()
        type_stmt,degree,structType=getArrayDetails(statement,degree)
        program_temp=type_stmt+' '+ statement.name
        for x in range(0,degree):
            program_temp+='[]'
        pointer=statement.name
        program_temp+=';'
        temp_ast = parser.parse(program_temp)
        return temp_ast.ext[0]
    else:
        return None









def updatePointerStructIf(statement,struct_map):
    If_stmt=None
    Else_stmt=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Compound:
            new_block_temp=updatePointerStruct(statement.iftrue.block_items,struct_map)
            If_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            If_stmt=statement.iftrue
    if type(statement.iffalse) is c_ast.Compound:
        if statement.iffalse.block_items is not None:
            new_block_temp=updatePointerStruct(statement.iffalse.block_items,struct_map)
            Else_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            Else_stmt=statement.iffalse
    else:
        if type(statement.iffalse) is c_ast.If:
            Else_stmt=updatePointerStructIf(statement.iffalse,struct_map)
        else:
            Else_stmt=statement.iffalse
    return c_ast.If(cond=statement.cond, iftrue=If_stmt, iffalse=Else_stmt)





















#Add External Variables


def addAllExtVariables(statements,externalvariables,localvarmap):
	update_statements=[]
	for var in externalvariables.keys():
		variable=externalvariables[var]
		temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=[variable.getVariableType()])), init=None, bitsize=None)
		update_statements.append(temp)
		localvarmap[var]=variable
		if variable.getInitialvalue() is not None:
			update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name=var), rvalue=c_ast.Constant(type=variable.getVariableType(), value=variable.getInitialvalue())))
	for element in statements:
		update_statements.append(element)
	return update_statements,localvarmap




def translateStruct(statements,variable_map,struct_map):
    update_statements=[]
    for statement in statements:
        if type(statement) is c_ast.Assignment:
            statement=c_ast.Assignment(op=statement.op,lvalue=translateStructStmt(statement.lvalue,variable_map,struct_map), rvalue=translateStructStmt(statement.rvalue,variable_map,struct_map))
            update_statements.append(statement)
        elif type(statement) is c_ast.While:
            cond=translateStructStmt(statement.cond,variable_map,struct_map)
            stmts=translateStruct(statement.stmt.block_items,variable_map,struct_map)
            statement=c_ast.While(cond=cond, stmt=c_ast.Compound(block_items=stmts))
            update_statements.append(statement)
        elif type(statement) is c_ast.If:
            update_statements.append(translateStructIf(statement,variable_map,struct_map))
        else:
             update_statements.append(statement)
    return update_statements
            

def translateStructIf(statement,variable_map,struct_map):
    If_stmt=None
    Else_stmt=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Compound:
            new_block_temp=translateStruct(statement.iftrue.block_items,variable_map,struct_map)
            If_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            If_stmt=statement.iftrue
    if type(statement.iffalse) is c_ast.Compound:
        if statement.iffalse.block_items is not None:
            new_block_temp=translateStruct(statement.iffalse.block_items,variable_map,struct_map)
            Else_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            Else_stmt=statement.iffalse
    else:
        if type(statement.iffalse) is c_ast.If:
            Else_stmt=translateStructIf(statement.iffalse,variable_map,struct_map)
        else:
            Else_stmt=statement.iffalse
    return c_ast.If(cond=translateStructStmt(statement.cond,variable_map,struct_map), iftrue=If_stmt, iffalse=Else_stmt)





def translateStructStmt(statement,variable_map,struct_map):
    if type(statement) is c_ast.BinaryOp:
        return c_ast.BinaryOp(op=statement.op, left=translateStructStmt(statement.left,variable_map,struct_map), right=translateStructStmt(statement.right,variable_map,struct_map))
    elif type(statement) is c_ast.FuncCall:
        para_list=[]
        if statement.args is not None:
            for para_meter in statement.args.exprs:
                para_list.append(translateStructStmt(para_meter,variable_map,struct_map))
            return c_ast.FuncCall(name=statement.name, args=c_ast.ExprList(exprs=para_list))
        else:
            return statement
    elif type(statement) is c_ast.StructRef:
        if type(statement.name) is c_ast.ID and type(statement.field) is c_ast.ID:
            if statement.name.name in variable_map.keys():
                variable=variable_map[statement.name.name]
                struct_name=variable.getStructType()
                if struct_name is not None:
                    para_list=[]
                    para_list.append(statement.name)
                    return c_ast.FuncCall(name=c_ast.ID(name=struct_name+"_"+statement.field.name), args=c_ast.ExprList(exprs=para_list))
                    #return c_ast.FuncCall(name=c_ast.ID(name=struct_name+"_"+statement.field.name), args=c_ast.ParamList(params=ExprList(exprs=para_list)))
        elif type(statement.name) is c_ast.ArrayRef and type(statement.field) is c_ast.ID:
            s_array_name=getArrayName(statement.name)
            if s_array_name in variable_map.keys():
                variable=variable_map[s_array_name]
                struct_name=variable.getStructType()
                if struct_name is not None:
                    para_list=[]
                    para_list.append(statement.name)
                    return c_ast.FuncCall(name=c_ast.ID(name=struct_name+"_"+statement.field.name), args=c_ast.ExprList(exprs=para_list))
        else:
            return statement
    elif type(statement) is c_ast.Cast:
        if type(statement.to_type.type) is c_ast.PtrDecl:
            if type(statement.to_type.type.type.type) is c_ast.Struct:
                if type(statement.expr) is c_ast.FuncCall and statement.expr.name.name =='malloc':
                    if type(statement.expr.args.exprs[0]) is c_ast.UnaryOp and statement.expr.args.exprs[0].op == 'sizeof':
                        if statement.expr.args.exprs[0].expr.type.type.name in struct_map.keys():
                            structobject=struct_map[statement.expr.args.exprs[0].expr.type.type.name]
                            return c_ast.ID(name='_Address_Block_Type_'+statement.expr.args.exprs[0].expr.type.type.name)
                        else:
                            return c_ast.ID(name='_Address_Block_Type_'+statement.expr.args.exprs[0].expr.type.type.name)
                    else:
                        return statement
                else:
                    return statement
            else:
                return statement

        else:
            if type(statement.to_type.type.type) is c_ast.Struct:
                if type(statement.expr) is c_ast.FuncCall and statement.expr.name.name =='malloc':
                    if type(statement.expr.args.exprs[0]) is c_ast.UnaryOp and statement.expr.args.exprs[0].op == 'sizeof':
                        if statement.expr.args.exprs[0].expr.type.name in struct_map.keys():
                            if statement.expr.args.exprs[0].expr.type.name in struct_map.keys():
                                if statement.expr.args.exprs[0].expr.type.type.name in struct_map.keys():
                                    structobject=struct_map[statement.expr.args.exprs[0].expr.type.name]
                                    return c_ast.ID(name='_Address_Block_Type_'+statement.expr.args.exprs[0].expr.type.name)
                                else:
                                    return c_ast.ID(name='_Address_Block_Type_'+statement.expr.args.exprs[0].expr.type.name)
                            else:
                                return statement
                        else:
                            return statement
                    else:
                            return statement
                else:
                     return statement
            else:
                if type(statement.to_type.type.type) is c_ast.IdentifierType:
                    if 'char' in statement.to_type.type.type.names:
                        if type(statement.expr) is c_ast.Constant and statement.expr.type=='int':
                            return statement.expr
                        else:
                            #return statement
                            return statement.expr
                    elif 'int' in statement.to_type.type.type.names:
                        if type(statement.expr) is c_ast.Constant and statement.expr.type=='int':
                            return statement.expr
                        else:
                            #return statement
                            return statement.expr
                    elif 'short' in statement.to_type.type.type.names:
                        if type(statement.expr) is c_ast.Constant and statement.expr.type=='int':
                            return statement.expr
                        else:
                            #return statement
                            return statement.expr
                    elif 'long' in statement.to_type.type.type.names:
                        if type(statement.expr) is c_ast.Constant and statement.expr.type=='int':
                            return statement.expr
                        else:
                            #return statement
                            return statement.expr
                    else:
                        return statement
                else:
                    return statement
    else:
        return statement

#
#Reconstruct Program by Removing assert,assume,error
#

def reconstructPreDefinedFun(statements):
	global fail_count
	global error_count
	global assume_count
	global assert_count
	global new_variable
        global counter_variableMap
        global counter_variableMap_Conf
        global array_size_variableMap
        
        counter_variableMap={}

        counter_variableMap_Conf={}

        array_size_variableMap={}
        
	statements=getPreDefinedFun(statements,0,{})
    	update_statements=[]
        temp_update_statements=[]

    	for var in new_variable.keys():
    		if type(new_variable[var]) is str:
    			temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
    		else:
    			temp=new_variable[var]
    		temp_update_statements.append(temp)
                
        for statement in temp_update_statements:
            update_statements.append(statement)
    	for statement in statements:
            update_statements.append(statement)

        #for statement in statements:
        #    #statement.show()
        #    #if type(statement) is not c_ast.Decl:
        #    update_statements.append(statement)
        
    	new_variable={}
    	return update_statements



counter_variableMap={}

counter_variableMap_Conf={}

array_size_variableMap={}

def getPreDefinedFun(statements,degree,dec_map):
	update_statements=[]
	global fail_count
	global error_count
	global assume_count
	global assert_count
	global new_variable
        global counter_variableMap
        global counter_variableMap_Conf
        global array_size_variableMap
        #print '$$$$$$$$$$$$$$$$$@@@@@@@@@@@@'
        #print new_variable
        #print '$$$$$$$$$$$$$$$$$@@@@@@@@@@@@'
	for statement in statements:
		if type(statement) is c_ast.If:
			stmt=getPreDefinedFunIf(statement,degree,dec_map)
			if stmt is not None:
				update_statements.append(stmt)
		elif type(statement) is c_ast.While:
			local_counter_varMap=getCounterVariables(statement.cond,counter_variableMap)

			getConfirmationVariables(statement.stmt.block_items,counter_variableMap,counter_variableMap_Conf)
                        

                        getCounterVariablesConst(statement.cond,array_size_variableMap)
                        
                        getArraySizeVar(local_counter_varMap,counter_variableMap_Conf,array_size_variableMap)
                        

                        degree=degree+1
                        
			new_block_items1=getPreDefinedFun(statement.stmt.block_items,degree,dec_map)
                        
                        degree=degree-1
                        
                        
			for item in local_counter_varMap.keys():
				if item in counter_variableMap.keys():
					del counter_variableMap[item]
				if item in counter_variableMap_Conf.keys():
					del counter_variableMap_Conf[item]
                                if item in array_size_variableMap.keys():
                                        del array_size_variableMap[item]
			#start comment on 16/08/2017
			#if degree==0:
                        #    array_size_variableMap.clear()
                        #    for var in dec_map.keys():
                        #        if type(dec_map[var]) is str:
                        #            temp=c_ast.Decl(name=var, quals=[], storage=[], funcspec=[], type=c_ast.TypeDecl(declname=var, quals=[], type=c_ast.IdentifierType(names=['int'])), init=c_ast.Constant(type='int', value='0'), bitsize=None)
                        #        else:
                        #            temp=dec_map[var]
                        #        update_statements.append(temp)
                        #        del dec_map[var]
                        #        del new_variable[var]
                        #end comment on 16/08/2017
			update_statements.append(c_ast.While(cond=statement.cond, stmt=c_ast.Compound(block_items=new_block_items1)))
		#elif type(statement) is c_ast.Label:
		#	if statement.name=='ERROR':
                #                print 'XXXXXXXXXXXXXXXXXXXXXXXX'
		#		fail_count=fail_count+1
		#		update_statements.append(statement)
		#		update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
		#		new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                #                dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
		#		
		#	else:
		#		update_statements.append(statement)
		elif type(statement) is c_ast.FuncCall:
			parameters=[]
			if statement.args is not None:
				for param in statement.args.exprs:
					if type(param) is c_ast.ID:
						parameters.append(param)
					elif type(param) is c_ast.Constant:
						parameters.append(param)
					elif type(param) is c_ast.BinaryOp:
						parameters.append(param)
					elif type(param) is c_ast.FuncCall:
						parameters.append(param)
					else:
						parameters.append(param)
                                if statement.name.name=='__VERIFIER_assert':
                                    new_statement=None
                                    for parameter in parameters:
                                            if new_statement is None:
                                                    assert_count=assert_count+1
                                                    new_var_name=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE')
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                        
                                                            if len(counter_variableMap_Conf)==degree:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
                                                            elif len(counter_variableMap)==degree:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap.keys(),counter_variableMap)
                                                            else:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
                                                            
                                                
                                                    status,parameter=modificationOfCondition(parameter)
                                                    if status==True:
                                                            parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))
						
                                                    new_statement= c_ast.Assignment(op='=', lvalue=new_var_name, rvalue=parameter)
						#new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                    if len(counter_variableMap_Conf.keys())>0:
                                            
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']=creatArrayDec('_'+str(assert_count)+'_'+'PROVE',array_size_variableMap.keys(),degree)
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']=creatArrayDec('_'+str(assert_count)+'_'+'PROVE',array_size_variableMap.keys(),degree)
                                                        
                                                    else:
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                        
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                        
                                                #print '#############@@@@@@@@'
                                                #print new_variable['_'+str(assert_count)+'_'+'PROVE'].show()
						#print '#############@@@@@@@@'
                                            else:
                                                    assert_count=assert_count+1
                                                    
                                                    new_var_name=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE')
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                            if len(counter_variableMap_Conf)==degree:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
                                                            elif len(counter_variableMap)==degree:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap.keys(),counter_variableMap)
                                                            else:
                                                                new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
                                                            #new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)

                                                    status,stmt=modificationOfCondition(parameter)
                                                    if status==True:
                                                            parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))
                                                    new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=new_var_name, rvalue=parameter), right=new_statement)
                                                    #new_variable['_'+str(assert_count)+'_'+'PROVE']='Array'
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']=creatArrayDec('_'+str(assert_count)+'_'+'PROVE',array_size_variableMap.keys(),degree)
                                                            

                                                        
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']=creatArrayDec('_'+str(assert_count)+'_'+'PROVE',array_size_variableMap.keys(),degree)
                                                    else:
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                        
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                        

                                    update_statements.append(new_statement)
                                elif statement.name.name=='__VERIFIER_assume':
                                    new_statement=None
                                    for parameter in parameters:
                                            if new_statement is None:
                                                    assume_count=assume_count+1
						
                                                    new_var_name=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME')
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                            new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)

                                                    status,parameter=modificationOfCondition(parameter)
                                                    if status==True:
                                                            parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))
						
                                                    new_statement= c_ast.Assignment(op='=', lvalue=new_var_name, rvalue=parameter)
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                        new_variable['_'+str(assume_count)+'_'+'ASSUME']=creatArrayDec('_'+str(assume_count)+'_'+'ASSUME',array_size_variableMap.keys(),degree)
                                                    
                                                        dec_map['_'+str(assume_count)+'_'+'ASSUME']=creatArrayDec('_'+str(assume_count)+'_'+'ASSUME',array_size_variableMap.keys(),degree)
                                                    
                                                    else:
                                                        new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                    
                                                        dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                            else:
                                                    assume_count=assume_count+1
						
                                                    new_var_name=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME')
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                            new_var_name=create_Assert_Array(new_var_name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
						
                                                    status,stmt=modificationOfCondition(parameter)
                                                    if status==True:
                                                            parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))						
						
                                                    new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=new_var_name, rvalue=parameter), right=new_statement)
                                                    if len(counter_variableMap_Conf.keys())>0:
                                                        new_variable['_'+str(assume_count)+'_'+'ASSUME']=creatArrayDec('_'+str(assume_count)+'_'+'ASSUME',array_size_variableMap.keys(),degree)
                                                    
                                                        dec_map['_'+str(assume_count)+'_'+'ASSUME']=creatArrayDec('_'+str(assume_count)+'_'+'ASSUME',array_size_variableMap.keys(),degree)
                                                    
                                                    else:
                                                        new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                    
                                                        dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                    update_statements.append(new_statement)
				else:
                                    update_statements.append(statement)
			else:
				if statement.name.name=='__VERIFIER_error':
                                    fail_count=fail_count+1
                                    #update_statements.append(statement)
                                    update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
                                    new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                    dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                else:
                                    update_statements.append(statement)
		
		else:
			update_statements.append(statement)
	return update_statements
	


#
#Get Counter Variable
#

def getCounterVariables(statement,variableMap):
	variableMap_Local={}
	if type(statement) is c_ast.UnaryOp:
		if type(statement.expr) is c_ast.ID:
			variableMap[statement.expr.name]=statement.expr.name
			variableMap_Local[statement.expr.name]=statement.expr.name
	        else:
                        temp_variableMap=getCounterVariables(statement.expr,variableMap)
                        if temp_variableMap is not None:
                        	for item in temp_variableMap.keys():
                        		variableMap_Local[item]=item
	elif type(statement) is c_ast.ID:
		variableMap[statement.name]=statement.name
		variableMap_Local[statement.name]=statement.name
	#elif type(statement) is c_ast.ArrayRef:
	#	getCounterVariables(statement.expr,variableMap)
	elif type(statement) is c_ast.BinaryOp:
		if type(statement.left) is c_ast.ID:
			variableMap[statement.left.name]=statement.left.name
			variableMap_Local[statement.left.name]=statement.left.name
		else:
			temp_variableMap=getCounterVariables(statement.left,variableMap)
			if temp_variableMap is not None:
				for item in temp_variableMap.keys():
                        		variableMap_Local[item]=item
		if type(statement.right) is c_ast.ID:
			variableMap[statement.right.name]=statement.right.name
			variableMap_Local[statement.right.name]=statement.right.name
		else:
			temp_variableMap=getCounterVariables(statement.right,variableMap)
			if temp_variableMap is not None:
				for item in temp_variableMap.keys():
                        		variableMap_Local[item]=item
        elif type(statement) is c_ast.ArrayRef:
                getAllSubScripts(statement,variableMap,variableMap_Local)
	return variableMap_Local


#
#Get Varible Constant from Condition
#

def getCounterVariablesConst(statement,variableMap):
	if type(statement) is c_ast.UnaryOp:
		if type(statement.expr) is c_ast.ID:
			variableMap[statement.expr.name]=statement.expr.name
	        else:
                        getCounterVariablesConst(statement.expr,variableMap)    
	elif type(statement) is c_ast.ID:
		variableMap[statement.name]=statement.name
        elif type(statement) is c_ast.Constant:
                variableMap[statement.value]=statement.value
	#elif type(statement) is c_ast.ArrayRef:
	#	getCounterVariables(statement.expr,variableMap)
	elif type(statement) is c_ast.BinaryOp:
		if type(statement.left) is c_ast.ID:
			variableMap[statement.left.name]=statement.left.name
		else:
			getCounterVariablesConst(statement.left,variableMap)
		if type(statement.right) is c_ast.ID:
			variableMap[statement.right.name]=statement.right.name
		else:
			getCounterVariablesConst(statement.right,variableMap)









def getAllSubScripts(statement,variableMap,variableMap_Local):
    if type(statement.subscript) is c_ast.ID:
        variableMap[statement.subscript.name]=statement.name
        variableMap_Local[statement.subscript.name]=statement.name
    if type(statement.name) is c_ast.ArrayRef:
        getAllSubScripts(statement.name,variableMap,variableMap_Local)
#
#Get Counter Variable
#

def getCounterVariablesConf(statement,variableMap):
	variableMap_Local={}
	if type(statement) is c_ast.UnaryOp:
		if type(statement.expr) is c_ast.ID:
			variableMap[statement.expr.name]=statement.expr.name
	        else:
                        getCounterVariablesConf(statement.expr,variableMap)    
	elif type(statement) is c_ast.ID:
		variableMap[statement.name]=statement.name
        #elif type(statement) is c_ast.Constant:
        #        variableMap[statement.value]=statement.value
	#elif type(statement) is c_ast.ArrayRef:
	#	getCounterVariables(statement.expr,variableMap)
	elif type(statement) is c_ast.BinaryOp:
		if type(statement.left) is c_ast.ID:
			variableMap[statement.left.name]=statement.left.name
		else:
			getCounterVariablesConf(statement.left,variableMap)
		if type(statement.right) is c_ast.ID:
			variableMap[statement.right.name]=statement.right.name
		else:
			getCounterVariablesConf(statement.right,variableMap)






#
#Confirmation of Counter Variable
#

def getConfirmationVariables(statements,variableMap,variableMap_Conf):
    for statement in statements:
    	if type(statement) is c_ast.Assignment:
        	if type(statement.lvalue) is c_ast.ID:
            		if statement.lvalue.name in variableMap.keys():
            			variableMapExp={}
                		getCounterVariablesConf(statement.rvalue,variableMapExp)
                		if statement.lvalue.name in variableMapExp.keys():
                   			 variableMap_Conf[statement.lvalue.name]=statement.lvalue.name

def getArraySizeVar(local_counter_varMap,counter_variableMap_Conf,array_size_variableMap):
    for var in local_counter_varMap.keys():
        if var in counter_variableMap_Conf.keys() and var in array_size_variableMap.keys():
            #array_size_variableMap[var]=var
            del array_size_variableMap[var]
                




#create_Assert_Array(['x','y'],{'x':'x','y':'y'})
def create_Assert_Array(array_name,items,variableMap):
	if len(items)>0:
		if len(items[1:])>0:
			return c_ast.ArrayRef(name=create_Assert_Array(array_name,items[:-1],variableMap), subscript=c_ast.ID(name=items[-1]))	
		else:
			return c_ast.ArrayRef(name=array_name, subscript=c_ast.ID(name=items[-1]))
	return None
	


#creatArrayDec('a',['x','y']).show()

def creatArrayDec(name,parameterlist,degree):
    str_parameterlist=None
    count=0
    generator = c_generator.CGenerator()
    #for para in parameterlist:
    #    if is_number(para)==True and '.' in para:
    #        para=str(int(para.split(".")[0]))
    arraysize=1000000
    if degree==2:
        arraysize=100000
    elif degree==3:
        arraysize=100000
        
    for x in range(0, degree):
        if str_parameterlist==None:
            
            str_parameterlist='['+str(arraysize)+']'
        else:
            str_parameterlist='['+str(arraysize)+']'+str_parameterlist
        #if count<degree:
        #    if str_parameterlist==None:
        #        str_parameterlist='['+para+']'
        #        #str_parameterlist='['+']'
        #    else:
        #        str_parameterlist='['+para+']'+str_parameterlist
        #count=count+1
    #print '-----------@@@@@@@@@@@@'
    #print parameterlist
    #print count
    #print degree
    #print '-----------@@@@@@@@@@@@'

            #str_parameterlist='['+']'+str_parameterlist
    if str_parameterlist is not None:
        function='int '+name+str_parameterlist
    else:
        function='int '+name
    main_function='void main(){'+function+';}'
    parser = c_parser.CParser()
    ast = parser.parse(main_function)
    return ast.ext[0].body.block_items[0]







#
#Reconstruct Program by Removing assert,assume,error
#

def getPreDefinedFunIf(statement,degree,dec_map):
	new_iftrue=None
	new_iffalse=None
	global fail_count
	global error_count
	global assume_count
	global assert_count
	global new_variable

	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Label:
			#if statement.iftrue.name=='ERROR':
			#	fail_count=fail_count+1
			#	new_block_items1=[]
			#	new_block_items1.append(c_ast.Label(name=statement.iftrue.name, stmt=[]))
			#	new_block_items1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
			#	new_iftrue=c_ast.Compound(block_items=new_block_items1)
			#	new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                        #        dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
			if type(statement.iftrue) is c_ast.FuncCall:
				parameters=[]
				if statement.iftrue.args is not None:
					for param in statement.iftrue.args.exprs:
						if type(param) is c_ast.ID:
							parameters.append(param)
						elif type(param) is c_ast.Constant:
							parameters.append(param)
						elif type(param) is c_ast.BinaryOp:
							parameters.append(param)
						elif type(param) is c_ast.FuncCall:
							parameters.append(param)
						else:
							parameters.append(param)
                                        if statement.iftrue.name.name=='__VERIFIER_assert':
                                            new_statement=None
                                            for parameter in parameters:
                                                    if new_statement is None:
                                                            assert_count=assert_count+1
                                                            status,parameter=modificationOfCondition(parameter)
                                                            if status==True:
                                                                    parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))
                                                            new_statement= c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE'), rvalue=parameter)
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                    else:
                                                            assert_count=assert_count+1
                                                            status,parameter=modificationOfCondition(parameter)
                                                            if status==True:
                                                                    parameter=c_ast.BinaryOp(op='>',left=parameter,right=c_ast.Constant(type='int', value='0'))
                                                            new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE'), rvalue=parameter), right=new_statement)
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                            new_iftrue=new_statement
                                        elif statement.iftrue.name.name=='__VERIFIER_assume':
                                            new_statement=None
                                            for parameter in parameters:
                                                    if new_statement is None:
                                                            assume_count=assume_count+1
                                                            new_statement= c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME'), rvalue=parameter)
                                                            new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                            dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                    else:
                                                            assume_count=assume_count+1
                                                            new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME'), rvalue=parameter), right=new_statement)
                                                            new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                            dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                            new_iftrue=new_statement
                                        elif statement.name.name=='__VERIFIER_error':
                                            fail_count=fail_count+1
                                            new_block_items1=[]
                                            #new_block_items1.append(c_ast.Label(name=statement.iftrue.name, stmt=[]))
                                            new_block_items1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
                                            new_iftrue=c_ast.Compound(block_items=new_block_items1)
                                            new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                            dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                        else:
                                            new_iftrue=statement.iftrue
                                
		elif type(statement.iftrue) is c_ast.Compound:
                    
                        #degree=degree+1
                        
			new_block_items=getPreDefinedFun(statement.iftrue.block_items,degree,dec_map)
                        
                        #degree=degree-1
                        
			new_iftrue=c_ast.Compound(block_items=new_block_items)
		else:
			new_iftrue=statement.iftrue
			
        if type(statement.iffalse) is c_ast.Label:
                    #if statement.iffalse.name=='ERROR':
                    #        fail_count=fail_count+1
                    #        new_block_items1=[]
                    #        #new_block_items1.append(statement.iffalse)
                    #        new_block_items1.append(c_ast.Label(name=statement.iftrue.name, stmt=[]))
                    #        new_block_items1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
                    #        new_iffalse=c_ast.Compound(block_items=new_block_items1)
                    #        new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                    #        dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                    if type(statement.iffalse) is c_ast.FuncCall:
                            parameters=[]
                            if statement.iffalse.args is not None:
                                    for param in statement.iftrue.args.exprs:
                                            if type(param) is c_ast.ID:
                                                    parameters.append(param)
                                            elif type(param) is c_ast.Constant:
                                                    parameters.append(param)
                                            elif type(param) is c_ast.BinaryOp:
                                                    parameters.append(param)
                                    if statement.name.name=='__VERIFIER_assert':
                                            new_statement=None
                                            for parameter in parameters:
                                                    if new_statement is None:
                                                            assert_count=assert_count+1
                                                            new_statement= c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE'), rvalue=parameter)
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                    else:
                                                            assert_count=assert_count+1
                                                            new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assert_count)+'_'+'PROVE'), rvalue=parameter), right=new_statement)
                                                            new_variable['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                                            dec_map['_'+str(assert_count)+'_'+'PROVE']='_'+str(assert_count)+'_'+'PROVE'
                                            new_iffalse=new_statement
                                    elif statement.name.name=='__VERIFIER_assume':
                                            new_statement=None
                                            for parameter in parameters:
                                                    if new_statement is None:
                                                            assume_count=assume_count+1
                                                            new_statement= c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME'), rvalue=parameter)
                                                            new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                            dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                    else:
                                                            assume_count=assume_count+1
                                                            new_statement=c_ast.BinaryOp(op='&&', left=c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(assume_count)+'_'+'ASSUME'), rvalue=parameter), right=new_statement)
                                                            new_variable['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                                            dec_map['_'+str(assume_count)+'_'+'ASSUME']='_'+str(assume_count)+'_'+'ASSUME'
                                            new_iffalse=new_statement
                                    elif statement.name.name=='__VERIFIER_error':
                                            fail_count=fail_count+1
                                            new_block_items1=[]
                                            #new_block_items1.append(c_ast.Label(name=statement.iftrue.name, stmt=[]))
                                            new_block_items1.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='_'+str(fail_count)+'_'+'FAILED'), rvalue=c_ast.Constant(type='int', value='1')))
                                            new_iftrue=c_ast.Compound(block_items=new_block_items1)
                                            new_variable['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                            dec_map['_'+str(fail_count)+'_'+'FAILED']='_'+str(fail_count)+'_'+'FAILED'
                                    else:
                                        new_iffalse=statement.iffalse
        elif type(statement.iffalse) is c_ast.Compound:
                    
                #degree=degree+1
                        
                new_block_items=getPreDefinedFun(statement.iffalse.block_items,degree,dec_map)
                        
                #degree=degree-1
                        
                new_iffalse=c_ast.Compound(block_items=new_block_items)
        else:
                if type(statement.iffalse) is c_ast.If:
                    new_iffalse=getPreDefinedFunIf(statement.iffalse,degree,dec_map)
                else:
                        new_iffalse=statement.iffalse
				
	if new_iftrue is not None and new_iffalse is None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=None)
	elif new_iftrue is not None and new_iffalse is not None:
		return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.Compound:
		return c_ast.If(cond=c_ast.UnaryOp(op='!', expr=statement.cond), iftrue=new_iffalse, iffalse=None)
	elif new_iffalse is not None and type(new_iffalse) is c_ast.If:
		return new_iffalse
	else:
		return None



def construct_main_program(program1, program2, parameters):
    
    update_statements=[]
    
    update_statements
    
    statements1=program1.block_items
    
    statements2=program2.block_items
    
    assert_left=None
    
    assert_right=None
    
    new_expr=[]
    
    new_expr.append(parameters)
        
    update_statements.append(c_ast.FuncCall(name=c_ast.ID(name='__VERIFIER_assume'),args=c_ast.ExprList(exprs=new_expr)))
        
    for x in statements1:
        
        if type(x) is c_ast.Assignment and x.lvalue.name=='p1_RET':
    
            assert_left=x.rvalue
            
        else:
            
            update_statements.append(x)
            
    for x in statements2:
        
        if type(x) is c_ast.Assignment and x.lvalue.name=='p2_RET':
            
            assert_right=x.rvalue
            
        else:
            
            update_statements.append(x)

    new_expr=[]
    
    new_expr.append(c_ast.BinaryOp(op='==',left=assert_left,right=assert_right))
        
    update_statements.append(c_ast.FuncCall(name=c_ast.ID(name='__VERIFIER_assert'),args=c_ast.ExprList(exprs=new_expr)))
    
    update_statements1=[]
    
    update_statements2=[]
    
    for x in update_statements:
        
        if type(x) is c_ast.Decl:
            
            update_statements1.append(x)
            
        else:
            
            update_statements2.append(x)
    
    update_statements = update_statements1+update_statements2
    
    return c_ast.Compound(block_items=update_statements)

    
            







"""


#Function Substitution Modules


"""

counter_variableMap={}
counter_variableMap_Conf={}


def substituteFunBlock(statements,functionvarmap,functionname,externalvarmap):
	update_statements=[]
	global new_variable
        global counter_variableMap
        global counter_variableMap_Conf
	for statement in statements:
		if type(statement) is c_ast.FuncCall:
			membermethod=functionvarmap[statement.name.name]
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
			
		
													
				input_map={}
			
			

				for x in range(0, len(statement.args.exprs)):
					arg=statement.args.exprs
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
					input_map[in_var_map[x]]=arg[x]
				
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),membermethod.getInputvar(),membermethod.getSerialNo())
                            
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)

				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
			        			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=(membermethod.getInputvar()[x].getVariableType(),membermethod.getInputvar()[x].getDimensions())
			        		else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
                                        else:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable[x]=(membermethod.getInputvar()[x].getVariableType(),membermethod.getInputvar()[x].getDimensions())
						else:
                                			new_variable[x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=(membermethod.getLocalvar()[x].getVariableType(),membermethod.getLocalvar()[x].getDimensions())
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
                                        else:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable[x]=(membermethod.getLocalvar()[x].getVariableType(),membermethod.getLocalvar()[x].getDimensions())
						else:
                                			new_variable[x]=membermethod.getLocalvar()[x].getVariableType()
			
			for stmt in new_blocks:
				update_statements.append(stmt)
		elif type(statement) is c_ast.Assignment:
			new_statement,new_block=substituteFun(statement.rvalue,functionvarmap,functionname,externalvarmap)
			if new_block is not None and len(new_block)>0:
				for stmt in new_block:
					update_statements.append(stmt)
			if type(statement.lvalue) is c_ast.ID:
				if 'DUMMY' not in statement.lvalue.name:
					update_statements.append(c_ast.Assignment(op='=',lvalue=statement.lvalue,rvalue=new_statement))
                                else:
                                        if new_block is None:
                                            update_statements.append(c_ast.Assignment(op='=',lvalue=statement.lvalue,rvalue=statement.rvalue))
			else:
				update_statements.append(c_ast.Assignment(op='=',lvalue=statement.lvalue,rvalue=new_statement))
		elif type(statement) is c_ast.While:
                    
                        counter_variableMap_Conf={}
                        counter_variableMap={}
                        local_counter_varMap=getCounterVariables(statement.cond,counter_variableMap)
			getConfirmationVariables(statement.stmt.block_items,counter_variableMap,counter_variableMap_Conf)                        
			statement.cond,new_block=substituteFun(statement.cond,functionvarmap,functionname,externalvarmap)
			if new_block is not None and len(new_block)>0:
				for stmt in new_block:
					update_statements.append(stmt)
			temp_new_block=substituteFunBlock(statement.stmt.block_items,functionvarmap,functionname,externalvarmap)
			if new_block is not None:
				for stmt in new_block:
					temp_new_block.append(stmt)
			update_statements.append(c_ast.While(cond=statement.cond,stmt=c_ast.Compound(block_items=temp_new_block)))	
		elif type(statement) is c_ast.If:
			statement,new_block=substituteFunBlockIf(statement,functionvarmap,functionname,externalvarmap)
			if new_block is not None and len(new_block)>0:
				for stmt in new_block:
					update_statements.append(stmt)
			update_statements.append(statement)
		else:
			update_statements.append(statement)
	return update_statements





def substituteFunBlockIf(statement,functionvarmap,functionname,externalvarmap):
	new_iftrue=None
	new_iffalse=None
	update_statements=None
	if type(statement) is c_ast.If:
		statement.cond,new_block=substituteFun(statement.cond,functionvarmap,functionname,externalvarmap)
		if new_block is not None and len(new_block)>0:
			update_statements=[]
			for stmt in new_block:
				update_statements.append(stmt)
		if type(statement.iftrue) is c_ast.Compound:
			new_iftrue=c_ast.Compound(block_items=substituteFunBlock(statement.iftrue.block_items,functionvarmap,functionname,externalvarmap))
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			new_iffalse=c_ast.Compound(block_items=substituteFunBlock(statement.iffalse.block_items,functionvarmap,functionname,externalvarmap))
		else:
			if type(statement.iffalse) is c_ast.If:
				statement.iffalse,new_block =substituteFunBlockIf(statement.iffalse,functionvarmap,functionname,externalvarmap)
				if new_block is not None and len(new_block)>0:
					if update_statements is None:
						update_statements=[]
					for stmt in new_block:
						update_statements.append(stmt)
				new_iffalse=statement.iffalse
	return c_ast.If(cond=statement.cond, iftrue=new_iftrue, iffalse=new_iffalse),update_statements



def substituteFun(statement,functionvarmap,functionname,externalvarmap):
	new_block=None
	global new_variable
	if type(statement) is c_ast.ID:
                return statement,new_block
        elif type(statement) is c_ast.Constant:
                return statement,new_block
        if type(statement) is c_ast.ArrayRef:
        	return statement,new_block
        elif type(statement) is c_ast.UnaryOp:
                stmt,new_block_t=substituteFun(statement.expr,functionvarmap,functionname,externalvarmap)
                return c_ast.UnaryOp(op=statement.op, expr=stmt),new_block_t
        elif type(statement) is c_ast.FuncCall:
                update_statements=[]
                if statement.name.name not in functionvarmap.keys():
                	return statement,new_block
 		membermethod=functionvarmap[statement.name.name]
		in_var_map=membermethod.getInputvar().keys()
		count=membermethod.getUsedCounter()
		count=count+1
		membermethod.setUsedCounter(count)
		
		membermethod_cur=functionvarmap[functionname]
                
		if membermethod_cur is not None:
			in_var_map_cu=[]
			in_var_map_cu=membermethod_cur.getInputvar().keys()
			all_local_var=[]
			all_local_var_cu=[]
			if in_var_map is not None:
				for x in in_var_map:
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var.append(x)
			if membermethod.getLocalvar() is not None:
				for x in membermethod.getLocalvar().keys():
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var.append(x)
			if in_var_map_cu is not None:
				for x in in_var_map_cu:
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var_cu.append(x)
			if membermethod_cur.getLocalvar() is not None:
				for x in membermethod_cur.getLocalvar().keys():
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var_cu.append(x)
						
			if membermethod.getInputvar() is not None:
				all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
			
	
								
			input_map={}
		
		
			if '__VERIFIER_nondet' not in statement.name.name:
				if statement.args is not None:
					for x in range(0, len(statement.args.exprs)):
                        			arg=statement.args.exprs
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=arg[x]))
						input_map[in_var_map[x]]=arg[x]

				
				
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
                                
                                
                                
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
                                
                                
				for x in membermethod.getInputvar().keys():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=(membermethod.getInputvar()[x].getVariableType(),membermethod.getInputvar()[x].getDimensions())
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
                                        else:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable[x]=(membermethod.getInputvar()[x].getVariableType(),membermethod.getInputvar()[x].getDimensions())
						else:
                                			new_variable[x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=(membermethod.getLocalvar()[x].getVariableType(),membermethod.getLocalvar()[x].getDimensions())
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
                                        else:
                                                if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable[x]=(membermethod.getLocalvar()[x].getVariableType(),membermethod.getLocalvar()[x].getDimensions())
						else:
                                			new_variable[x]=membermethod.getLocalvar()[x].getVariableType()
		
		
				for stmt in new_blocks:
					update_statements.append(stmt)
 		
 				return c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+'RET'),update_statements	
 			else:
 				return statement,new_block
 		else:
 			return statement,new_block
 	elif type(statement) is c_ast.BinaryOp:
 		if type(statement.left) is c_ast.ID and type(statement.right) is c_ast.ID:
 			
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 		if type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.ArrayRef:
 			
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block	
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.BinaryOp:
                                               
                        stmt_right,new_block=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)

 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right),new_block
 			
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.ID:
 			
                        stmt_left,new_block=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)
                        
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right),new_block
 			
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.Constant:
 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 			
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.ID:

 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 			
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.Constant:
 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.Constant:
		 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.ArrayRef:
		 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.ArrayRef:
				 		
		 	return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.ID:
				 		
		 	return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block 		
 		
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.BinaryOp:
		
		        stmt_right,new_block=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)
		                        
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right),new_block
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.BinaryOp:

                        stmt_right,new_block=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)
                        
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right),new_block
 			
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.Constant:

                        stmt_left,new_block=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)
 		
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right),new_block
 			
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.ArrayRef:
		
		        stmt_left,new_block=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)
		 		
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right),new_block
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.BinaryOp:
		
		        stmt_right,new_block=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)
		                        
		 	return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right),new_block
		 			
		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.ArrayRef:
		
		        stmt_left,new_block=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)
		 		
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right),new_block
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.BinaryOp:

                        stmt_left,new_block1=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)

                        stmt_right,new_block2=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)

                        if new_block1 is not None and new_block2 is None:
 		
                                return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right),new_block1

                        elif new_block1 is None and new_block2 is not None:

                                return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right),new_block2
                        else:
                                new_block=[]
                                if new_block1 is not None:
                                	for stmt in new_block1:
                                        	new_block.append(stmt)
                                if new_block2 is not None:
                                	for stmt in new_block2:
                                        	new_block.append(stmt)
                                return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right),new_block
 		
  		elif type(statement.left) is c_ast.FuncCall and type(statement.right) is c_ast.BinaryOp:
 		 	update_statements=[]
		 	
		 	if statement.left.name.name not in functionvarmap.keys():
		 		return statement,new_block
		 	
		 	membermethod=functionvarmap[statement.left.name.name]
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			
			membermethod_cur=functionvarmap[functionname]
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
			
	
								
				input_map={}
			
			
			
				if statement.left.args is not None:
					for x in range(0, len(statement.left.args.exprs)):
						arg=statement.left.args.exprs
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
						input_map[in_var_map[x]]=arg[x]
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),membermethod.getInputvar(),membermethod.getSerialNo())
			
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
				for stmt in new_blocks:
					update_statements.append(stmt)
				
				
				
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()

			
			stmt_right,new_block1=substituteFun(statement.right,functionvarmap,functionname,externalvarmap)
			if new_block1 is not None:
				for stmt in new_block1:
					update_statements.append(stmt)
				
 			return c_ast.BinaryOp(op=statement.op,left=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET'), right=stmt_right),update_statements			
 		
 		
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.FuncCall:
 		 	update_statements=[]
		 	stmt_left,new_block1=substituteFun(statement.left,functionvarmap,functionname,externalvarmap)
		 	if new_block1 is not None:
		 		for stmt in new_block1:
					update_statements.append(stmt)
		 	
		 	if statement.right.name.name not in functionvarmap.keys():
		 		return statement,new_block
		 	
		 	membermethod=functionvarmap[statement.right.name.name]
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			
			membermethod_cur=functionvarmap[functionname]
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
			
		
					
				input_map={}
			
			
			
			
			
				if statement.right.args is not None:
					for x in range(0, len(statement.right.args.exprs)):
						arg=statement.right.args.exprs
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=arg[x]))
						input_map[in_var_map[x]]=arg[x]
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
				for stmt in new_blocks:
					update_statements.append(stmt)
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')),update_statements	
 			
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.FuncCall:
 			update_statements=[]
 			
 			if statement.right.name.name not in functionvarmap.keys():
		 		return statement,new_block
 			
 			membermethod=functionvarmap[statement.right.name.name]
 			
 			
 			if membermethod.getBody() is None:
		 		return statement,new_block
 			
 			
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			
			membermethod_cur=functionvarmap[functionname]
			

			
			
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
			
		
				input_map={}
						
				if statement.right.args is not None:
					for x in range(0, len(statement.right.args.exprs)):
						arg=statement.right.args.exprs
						input_map[in_var_map[x]]=arg[x]
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=arg[x]))
					
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
						
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
				

				
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
				for stmt in new_blocks:
					update_statements.append(stmt)
 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')),update_statements	
 		
  		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.FuncCall:
  			update_statements=[]
  			
  			if statement.right.name.name not in functionvarmap.keys():
		 		return statement,new_block
  			
  			membermethod=functionvarmap[statement.right.name.name]
  			
  			if membermethod.getBody() is None:
		 		return statement,new_block
  			
  			
 			in_var_map=membermethod.getInputvar().keys()
 			count=membermethod.getUsedCounter()
 			count=count+1
 			membermethod.setUsedCounter(count)
 			
 			
 			membermethod_cur=functionvarmap[functionname]
 			if membermethod_cur is not None:
 				in_var_map_cu=[]
 				in_var_map_cu=membermethod_cur.getInputvar().keys()
 				all_local_var=[]
 				all_local_var_cu=[]
 				if in_var_map is not None:
 					for x in in_var_map:
 						if externalvarmap is not None:
 							if x not in externalvarmap.keys():
 								all_local_var.append(x)
 				if membermethod.getLocalvar() is not None:
 					for x in membermethod.getLocalvar().keys():
 						if externalvarmap is not None:
 							if x not in externalvarmap.keys():
 								all_local_var.append(x)
 				if in_var_map_cu is not None:
 					for x in in_var_map_cu:
 						if externalvarmap is not None:
 							if x not in externalvarmap.keys():
 								all_local_var_cu.append(x)
 				if membermethod_cur.getLocalvar() is not None:
 					for x in membermethod_cur.getLocalvar().keys():
 						if externalvarmap is not None:
 							if x not in externalvarmap.keys():
 								all_local_var_cu.append(x)
 						
 				if membermethod.getInputvar() is not None:
 					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
 			
 		
 				input_map={}
 						
 				if statement.right.args is not None:
 					for x in range(0, len(statement.right.args.exprs)):
 						arg=statement.right.args.exprs
 						input_map[in_var_map[x]]=arg[x]
 					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
 				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=arg[x]))
 					
 				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
 						
 				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
 				
 
 				
 				for x in membermethod.getInputvar():
 					if x in all_var_int:
 						if membermethod.getInputvar()[x].getDimensions()>0:
 							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
 						else:
                                 			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
 				
 				for x in membermethod.getLocalvar():
 					if x in all_var_int:
 						if membermethod.getLocalvar()[x].getDimensions()>0:
 							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
 						else:
                                 			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
 				for stmt in new_blocks:
 					update_statements.append(stmt)
  		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')),update_statements	
 		
 		elif type(statement.left) is c_ast.FuncCall and type(statement.right) is c_ast.ID :
			update_statements=[]
			
			if statement.left.name.name not in functionvarmap.keys():
		 		return statement,new_block
			
		 	membermethod=functionvarmap[statement.left.name.name]
		 	
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			
			
			membermethod_cur=functionvarmap[functionname]
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
								
				input_map={}
			
			
				if statement.left.args is not None:
					for x in range(0, len(statement.left.args.exprs)):
						arg=statement.left.args.exprs
						input_map[in_var_map[x]]=arg[x]
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
			
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
			new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
			for x in membermethod.getInputvar():
				if x in all_var_int:
					if membermethod.getInputvar()[x].getDimensions()>0:
						new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
					else:
                                		new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
			for x in membermethod.getLocalvar():
				if x in all_var_int:
					if membermethod.getLocalvar()[x].getDimensions()>0:
						new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
					else:
                                		new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
			for stmt in new_blocks:
				update_statements.append(stmt)
		 		
 			return c_ast.BinaryOp(op=statement.op,left=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET'), right=statement.right),update_statements	

 		elif type(statement.left) is c_ast.FuncCall and type(statement.right) is c_ast.ArrayRef :
			update_statements=[]
			
			if statement.left.name.name not in functionvarmap.keys():
		 		return statement,new_block
			
			
		 	membermethod=functionvarmap[statement.left.name.name]
		 	
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			
			
			membermethod_cur=functionvarmap[functionname]
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
						
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
								
				input_map={}
			
			
				if statement.left.args is not None:
					for x in range(0, len(statement.left.args.exprs)):
						arg=statement.left.args.exprs
						input_map[in_var_map[x]]=arg[x]
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
						#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
			
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
			new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
			for x in membermethod.getInputvar():
				if x in all_var_int:
					if membermethod.getInputvar()[x].getDimensions()>0:
						new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
					else:
                                		new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
			for x in membermethod.getLocalvar():
				if x in all_var_int:
					if membermethod.getLocalvar()[x].getDimensions()>0:
						new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
					else:
                                		new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
			for stmt in new_blocks:
				update_statements.append(stmt)
		 		
 			return c_ast.BinaryOp(op=statement.op,left=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET'), right=statement.right),update_statements	
 		
 		
 		
 		
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.FuncCall:
		 	update_statements=[]
		 	
		 	if statement.right.name.name not in functionvarmap.keys():
		 		return statement,new_block
		 	
		 	membermethod=functionvarmap[statement.right.name.name]
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
					
						
			membermethod_cur=functionvarmap[functionname]
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
									
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
											
				input_map={}
			
			
				for x in range(0, len(statement.right.args.exprs)):
					arg=statement.right.args.exprs
					input_map[in_var_map[x]]=arg[x]
				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
				for stmt in new_blocks:
					update_statements.append(stmt)
		 		
		 	return c_ast.BinaryOp(op=statement.op,left=statement.left, right=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')),update_statements	
		 		
		elif type(statement.left) is c_ast.FuncCall and type(statement.right) is c_ast.Constant :
			update_statements=[]
			
			if statement.left.name.name not in functionvarmap.keys():
		 		return statement,new_block
			
			membermethod=functionvarmap[statement.left.name.name]
			
			if membermethod.getBody() is None:
		 		return statement,new_block
			
			
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
						
			membermethod_cur=functionvarmap[functionname]
			
			
			if membermethod_cur is not None:
				in_var_map_cu=[]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				for x in in_var_map:
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				for x in in_var_map_cu:
					if externalvarmap is not None:
						if x not in externalvarmap.keys():
							all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
									
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
											
				input_map={}
						
			
				if statement.left.args is not None:
					for x in range(0, len(statement.left.args.exprs)):
						arg=statement.left.args.exprs
						input_map[in_var_map[x]]=arg[x]
				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
				#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
				
				
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
				for stmt in new_blocks:
					update_statements.append(stmt)
		
				 		
 			return c_ast.BinaryOp(op=statement.op,left=c_ast.ID(name='t_'+str(count)+'_RET'), right=statement.right),update_statements	
 		
 		elif type(statement.left) is c_ast.FuncCall and type(statement.right) is c_ast.FuncCall:
		 	update_statements=[]
		 	
		 	if statement.left.name.name not in functionvarmap.keys():
		 		return statement,new_block
		 	
		 	membermethod=functionvarmap[statement.left.name.name]
		 	
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 		
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)
			
			membermethod_cur=functionvarmap[functionname]
			
			if membermethod_cur is not None:
				in_var_map_cu=[]
				if membermethod_cur.getInputvar() is not None:
					in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if x not in externalvarmap.keys():
							all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
									
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
											
				input_map={}
						
				if statement.left.args is not None:
					for x in range(0, len(statement.left.args.exprs)):
						arg=statement.left.args.exprs
						input_map[in_var_map[x]]=arg[x]
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
			
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
			
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
					
			
				for stmt in new_blocks:
					update_statements.append(stmt)
		 	
		 		stmt_left=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')
		 	else:
		 		stmt_left=statement.left
		 	
		 	
		 	if statement.right.name.name not in functionvarmap.keys():
		 		return statement,new_block
		 		
		 	membermethod=functionvarmap[statement.right.name.name]
		 	
		 	if membermethod.getBody() is None:
		 		return statement,new_block
		 	
		 	
			in_var_map=membermethod.getInputvar().keys()
			count=membermethod.getUsedCounter()
			count=count+1
			membermethod.setUsedCounter(count)

			if membermethod_cur is not None:
				membermethod_cur=functionvarmap[functionname]
				in_var_map_cu=membermethod_cur.getInputvar().keys()
				all_local_var=[]
				all_local_var_cu=[]
				if in_var_map is not None:
					for x in in_var_map:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if membermethod.getLocalvar() is not None:
					for x in membermethod.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var.append(x)
				if in_var_map_cu is not None:
					for x in in_var_map_cu:
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
				if membermethod_cur.getLocalvar() is not None:
					for x in membermethod_cur.getLocalvar().keys():
						if externalvarmap is not None:
							if x not in externalvarmap.keys():
								all_local_var_cu.append(x)
									
				if membermethod.getInputvar() is not None:
					all_var_int=intersect3(all_local_var,all_local_var_cu,membermethod.getInputvar().keys())
											
				input_map={}
			
			
				if statement.left.args is not None:
					for x in range(0, len(statement.right.args.exprs)):
						arg=statement.right.args.exprs
						input_map[in_var_map[x]]=arg[x]
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+arg[x].name),rvalue=c_ast.ID(name=in_var_map[x])))
					#update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+in_var_map[x]),rvalue=c_ast.ID(name=arg[x].name)))
			
			
			
				new_blocks=reconstructStmtBlock(membermethod.getBody().block_items,count,membermethod.getLocalvar(),input_map,membermethod.getSerialNo(),all_var_int)
			
				new_blocks=substituteFunBlock(new_blocks,functionvarmap,functionname,externalvarmap)
			
			
				for x in membermethod.getInputvar():
					if x in all_var_int:
						if membermethod.getInputvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getInputvar()[x].getVariableType()
				
				for x in membermethod.getLocalvar():
					if x in all_var_int:
						if membermethod.getLocalvar()[x].getDimensions()>0:
							new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]='array'
						else:
                                			new_variable['f'+str(membermethod.getSerialNo())+'_'+str(count)+'_'+x]=membermethod.getLocalvar()[x].getVariableType()
						
		
		
				for stmt in new_blocks:
					update_statements.append(stmt)
		 	
		 		stmt_right=c_ast.ID(name='f'+str(membermethod.getSerialNo())+'_'+str(count)+'_RET')
		 	else:
		 		stmt_right=statement.right
		 	
		 	return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right),update_statements	
	
 		else:
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right),new_block
 	return None


def getIndexVariable(statement,local_map):
    if type(statement) is c_ast.BinaryOp:
        getIndexVariable(statement.left,local_map)
        getIndexVariable(statement.right,local_map)
    elif type(statement) is c_ast.ArrayRef:
        if type(statement.name) is c_ast.ArrayRef:
            getIndexVariable(statement.name,local_map)
        local_map[statement.subscript.name]=statement.subscript.name
    

new_variable_array={}

def reconstructStmtBlock(statements,count,var_map,in_var_map,fun_count,all_var_int):
	update_statements=[]
        global counter_variableMap
        global counter_variableMap_Conf
        global new_variable_array
	for statement in statements:
                if type(statement) is c_ast.Decl:
                    if type(statement.type) is c_ast.ArrayDecl:
                        if statement.name in all_var_int:
                            update_statements.append(c_ast.Decl(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.name, quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=renameArrayName(statement.type), init=statement.init, bitsize=statement.bitsize))
                        else:
                            update_statements.append(statement)
                    elif type(statement.type) is c_ast.PtrDecl:
                        if type(statement.type.type) is c_ast.TypeDecl:
                            update_statements.append(c_ast.TypeDecl('f'+str(fun_count)+'_'+str(count)+'_'+statement.name, quals=statement.type.type.quals, type=statement.type.type.type))
                    else:
                        if statement.name in all_var_int:
                            update_statements.append(c_ast.Decl(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.name, quals=statement.quals, storage=statement.storage, funcspec=statement.funcspec, type=c_ast.TypeDecl(declname='f'+str(fun_count)+'_'+str(count)+'_'+statement.type.declname, quals=statement.type.quals, type=statement.type.type), init=statement.init, bitsize=statement.bitsize))
                        else:
                            update_statements.append(statement)

		elif type(statement) is c_ast.Assignment:
			if type(statement.lvalue) is c_ast.ID:
				if statement.lvalue.name in all_var_int:
					update_statements.append(c_ast.Assignment(op='=', lvalue=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.lvalue.name), rvalue=reconstructStmt(statement.rvalue,count,var_map,in_var_map,fun_count,all_var_int)))
				else:
					if statement.lvalue.name in in_var_map.keys():
                                                r_statement=reconstructStmt(statement.rvalue,count,var_map,in_var_map,fun_count,all_var_int)
                                                l_statement=in_var_map[statement.lvalue]
                                                if '_PROVE' in statement.lvalue.name:
                                                    #local_map={}
                                                    #getIndexVariable(r_statement,local_map)
                                                    #if local_map==counter_variableMap_Conf:
                                                    #new_variable_array[l_statement.name]=creatArrayDec(l_statement.name,counter_variableMap_Conf.keys())
                                                    new_variable_array[l_statement.name]=len(counter_variableMap_Conf.keys())
                                                    l_statement=create_Assert_Array(l_statement.name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
						update_statements.append(c_ast.Assignment(op='=', lvalue=l_statement, rvalue=r_statement))
					else:
                                                r_statement=reconstructStmt(statement.rvalue,count,var_map,in_var_map,fun_count,all_var_int)
                                                l_statement=statement.lvalue
                                                #if '_PROVE' in statement.lvalue.name:
                                                #    new_variable_array[l_statement.name]=len(counter_variableMap_Conf.keys())
                                                #    l_statement=create_Assert_Array(l_statement,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
						update_statements.append(c_ast.Assignment(op='=', lvalue=l_statement, rvalue=r_statement))
			else:
                                r_statement=reconstructStmt(statement.rvalue,count,var_map,in_var_map,fun_count,all_var_int)
                                l_statement=reconstructStmt(statement.lvalue,count,var_map,in_var_map,fun_count,all_var_int)
                                #if '_PROVE' in statement.lvalue.name:
                                #    new_variable_array[l_statement.name]=len(counter_variableMap_Conf.keys())
                                #    l_statement=create_Assert_Array(l_statement.name,counter_variableMap_Conf.keys(),counter_variableMap_Conf)
				update_statements.append(c_ast.Assignment(op='=', lvalue=l_statement, rvalue=r_statement))
		elif type(statement) is c_ast.While:
			update_statements.append(reconstructStmt(c_ast.While(cond=reconstructStmt(statement.cond,count,var_map,in_var_map,fun_count,all_var_int),stmt=c_ast.Compound(block_items=reconstructStmtBlock(statement.stmt.block_items,count,var_map,in_var_map,fun_count,all_var_int))),count,var_map,in_var_map,fun_count,all_var_int ))
		elif type(statement) is c_ast.If:
			update_statements.append(reconstructStmtIf(statement,count,var_map,in_var_map,fun_count,all_var_int))
		else:
			if type(statement) is c_ast.FuncCall:
				update_statements.append(statement)
			else:
                                #if type(statement) is c_ast.Decl:
                                #        var_type=None
                                #        initial_value=None
                                #        for child in statement.children():
                                #                if type(child[1]) is c_ast.TypeDecl:
                                #                	if type(child[1].type) is c_ast.IdentifierType:
                                #                        	var_type=child[1].type.names[0]
                                #                else:
                                #                        initial_value=child[1]
                                #        if initial_value is not None:
                                #        	
                                #        	if statement.name in all_var_int:
                                #        		update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.name), rvalue=reconstructStmt(initial_value,count,var_map,in_var_map,fun_count,all_var_int)))	
                                #        	else:
                                #        		if statement.name in in_var_map.keys():
                                #        			update_statements.append(c_ast.Assignment(op='=',lvalue=in_var_map[statement.name], rvalue=reconstructStmt(initial_value,count,var_map,in_var_map,fun_count,all_var_int)))
                                #        		else:
                                #        			update_statements.append(c_ast.Assignment(op='=',lvalue=c_ast.ID(name=statement.name), rvalue=reconstructStmt(initial_value,count,var_map,in_var_map,fun_count,all_var_int)))
                                        	
                                #else:
                                if type(statement) is not c_ast.Decl:
                                    update_statements.append(statement)
	return update_statements





def reconstructStmtIf(statement,count,var_map,in_var_map,fun_count,all_var_int):
	new_iftrue=None
	new_iffalse=None
	if type(statement) is c_ast.If:
		if type(statement.iftrue) is c_ast.Compound:
			new_iftrue=c_ast.Compound(block_items=reconstructStmtBlock(statement.iftrue.block_items,count,var_map,in_var_map,fun_count,all_var_int))
		else:
			new_iftrue=statement.iftrue
		if type(statement.iffalse) is c_ast.Compound:
			new_iffalse=c_ast.Compound(block_items=reconstructStmtBlock(statement.iffalse.block_items,count,var_map,in_var_map,fun_count,all_var_int))
		else:
			if type(statement.iffalse) is c_ast.If:
				new_iffalse=reconstructStmtIf(statement.iffalse,count,var_map,in_var_map,all_var_int)
	
	return c_ast.If(cond=reconstructStmt(statement.cond,count,var_map,in_var_map,fun_count,all_var_int), iftrue=new_iftrue, iffalse=new_iffalse)






def reconstructStmt(statement,count,var_map,in_var_map,fun_count,all_var_int):
	if type(statement) is c_ast.ID:
		if statement.name in var_map.keys() or statement.name in in_var_map.keys():
			if statement.name in all_var_int:
				return c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.name)
			else:
				return statement
		else:
			return statement
 	elif type(statement) is c_ast.UnaryOp:
 		return c_ast.UnaryOp(op=statement.op,expr=reconstructStmt(statement.expr,count,var_map,in_var_map,fun_count,all_var_int))
 	elif type(statement) is c_ast.Constant:
 		return statement
 	elif type(statement) is c_ast.BinaryOp:
 		if type(statement.left) is c_ast.ID and type(statement.right) is c_ast.ID:
 			stmt_left=None
 			stmt_right=None
 			if statement.left.name in var_map.keys() or statement.left.name in in_var_map.keys():
 				if statement.left.name in all_var_int:
 					stmt_left=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.left.name)
 				else:
 					stmt_left=statement.left
 						
 			else:
 				stmt_left=statement.left
 				
 			if statement.right.name in var_map.keys() or statement.right.name in in_var_map.keys():
				if statement.right.name in all_var_int:
					stmt_right=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.right.name)
				else:
					stmt_right=statement.right
						
			else:
 				stmt_right=statement.right
 			
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right)
                        
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.ArrayRef:
 			stmt_left=None
 			stmt_right=None
 			if statement.left.name in var_map.keys() or statement.left.name in in_var_map.keys():
 				if statement.left.name in all_var_int:
 					stmt_left=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.left.name)
 				else:
 					stmt_left=statement.left
 						
 			else:
 				stmt_left=statement.left
 				
 			stmt_right=renameArrayName1(statement.right,count,var_map,in_var_map,fun_count,all_var_int)
 			
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right)

 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.ID:
 			stmt_left=None
 			stmt_right=None
                        
 			stmt_left=renameArrayName1(statement.left,count,var_map,in_var_map,fun_count,all_var_int)
 				
 			if statement.right.name in var_map.keys() or statement.right.name in in_var_map.keys():
				if statement.right.name in all_var_int:
					stmt_right=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.right.name)
				else:
					stmt_right=statement.right
						
			else:
 				stmt_right=statement.right
 			
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=stmt_right)
 				
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.BinaryOp:
 			stmt_left=None
			if statement.left.name in all_var_int:
				stmt_left=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.left.name)
			else:
				stmt_left=statement.left
					
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 				
 			
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.ID:
 			stmt_right=None
 			
			if statement.right.name in all_var_int:
				stmt_right=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+statement.right.name)
			else:
				stmt_right=statement.right
					
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=stmt_right)
 				
  		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.UnaryOp:
 			stmt_left=None
 			
			if statement.left.name in all_var_int:
				stmt_left=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.left.name)
			else:
				
				stmt_left=statement.left
					
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 				
 			
 		elif type(statement.left) is c_ast.UnaryOp and type(statement.right) is c_ast.ID:
 			stmt_right=None
 			
 		
			if statement.right.name in all_var_int:
				stmt_right=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+statement.right.name)
			else:
				stmt_right=statement.right
					
 			
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=stmt_right)
 					
 		

 		
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.Constant:
 		
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right)
 			
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.ID:
 			stmt_right=None
  
			if statement.right.name in all_var_int:
				stmt_right=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.right.name)
			else:
				stmt_right=statement.right
								
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right)
 				
 			
 		elif type(statement.left) is c_ast.ID and type(statement.right) is c_ast.Constant:
 			stmt_left=None
 			
 		 	if statement.left.name in all_var_int:
				stmt_left=c_ast.ID(name='f'+str(fun_count)+'_'+str(count)+'_'+statement.left.name)
			else:
				stmt_left=statement.left
					
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right)
 			
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.ArrayRef:
 			stmt_right=None
  
			stmt_right=renameArrayName1(statement.right,count,var_map,in_var_map,fun_count,all_var_int)
								
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=stmt_right)
 				
 			
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.Constant:
 			stmt_left=None
 			
 		 	stmt_left=renameArrayName1(statement.left,count,var_map,in_var_map,fun_count,all_var_int)
					
 			return c_ast.BinaryOp(op=statement.op,left=stmt_left, right=statement.right)
                    
                        
 				
 		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.UnaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.UnaryOp and type(statement.right) is c_ast.Constant:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=statement.right)	
                        	
                elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.ArrayRef:
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.Constant:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=statement.right)
  		
  		elif type(statement.left) is c_ast.Constant and type(statement.right) is c_ast.BinaryOp:
  			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
  		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.Constant:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=statement.right)
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.BinaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.UnaryOp and type(statement.right) is c_ast.UnaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.UnaryOp and type(statement.right) is c_ast.BinaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.UnaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.BinaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.BinaryOp and type(statement.right) is c_ast.ArrayRef:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		
 		elif type(statement.left) is c_ast.UnaryOp and type(statement.right) is c_ast.ArrayRef:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		elif type(statement.left) is c_ast.ArrayRef and type(statement.right) is c_ast.UnaryOp:
 			return c_ast.BinaryOp(op=statement.op,left=reconstructStmt(statement.left,count,var_map,in_var_map,fun_count,all_var_int), right=reconstructStmt(statement.right,count,var_map,in_var_map,fun_count,all_var_int))
 		
 		else:
 			return c_ast.BinaryOp(op=statement.op,left=statement.left, right=statement.right)
 	else:
 		return statement
 	return None

def reduceArraySize1(program):
    #print program
    #print '--------------------------'
    status=False
    sub_status=False
    parser = GnuCParser()
    ast = parser.parse(program)
    try:
        for e in ast.ext:
            if type(e) is c_ast.FuncDef: 
                function_body = e.body
                if function_body.block_items is not None:
                    for x in function_body.block_items:
                        if type(x) is c_ast.Decl:
                            stmt = fun_utiles.programPrint(x)
                            if fun_utiles.isSubsVar(x.name)==True:
                                sub_status=True

                            if ('[60]' in stmt) and '_PROVE' not in stmt:
                                status=True
                            elif ('[40]' in stmt) and '_PROVE' not in stmt:
                                status=True
                    e.body.block_items=reduceArraySizeBlock1(function_body.block_items)
                    return ast.ext[0],status,sub_status
        return None,False,False
    except Exception as e:
        #writeLogFile( "j2llogs.logs" ,str(e))
        print str(e)
        print 'XXXXX'
        return None,False,False



def reduceArraySizeBlock1(statements):
    parser = GnuCParser()
    update_statements=[]
    for statement in statements:
        if type(statement) is c_ast.Decl:
            stmt = fun_utiles.programPrint(statement)
            if '[60]' in stmt:
                stmt=stmt.replace('[60]','[10]')
                ast1 = parser.parse(stmt+';')
                update_statements.append(ast1.ext[0])
            elif '[40]' in stmt:
                stmt=stmt.replace('[40]','[10]')
                ast1 = parser.parse(stmt+';')
                update_statements.append(ast1.ext[0])
            else:
                 update_statements.append(statement)
        elif type(statement) is c_ast.While:
            cond=reduceArrayStatement1(statement.cond)
            stmts=reduceArraySizeBlock1(statement.stmt.block_items)
            statement=c_ast.While(cond=cond, stmt=c_ast.Compound(block_items=stmts))
            update_statements.append(statement)
        elif type(statement) is c_ast.If:
            update_statements.append(reduceArraySizeBlockIf1(statement))
        elif type(statement) is c_ast.Assignment:
            update_statements.append(c_ast.Assignment(op=statement.op,lvalue=reduceArrayStatement1(statement.lvalue),rvalue=reduceArrayStatement1(statement.rvalue)))
        else:
            update_statements.append(statement)
    return update_statements


def reduceArraySizeBlockIf1(statement):
    If_stmt=None
    Else_stmt=None
    if type(statement) is c_ast.If:
        if type(statement.iftrue) is c_ast.Compound:
            new_block_temp=reduceArraySizeBlock1(statement.iftrue.block_items)
            If_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            If_stmt=statement.iftrue
    if type(statement.iffalse) is c_ast.Compound:
        if statement.iffalse.block_items is not None:
            new_block_temp=reduceArraySizeBlock1(statement.iffalse.block_items)
            Else_stmt=c_ast.Compound(block_items=new_block_temp)
        else:
            Else_stmt=statement.iffalse
    else:
        if type(statement.iffalse) is c_ast.If:
            Else_stmt=reduceArraySizeBlockIf1(statement.iffalse)
        else:
            Else_stmt=statement.iffalse
    return c_ast.If(cond=reduceArrayStatement1(statement.cond), iftrue=If_stmt, iffalse=Else_stmt)
    
    
def reduceArrayStatement1(statement):
    if type(statement) is c_ast.BinaryOp:
        return c_ast.BinaryOp(op=statement.op, left=reduceArrayStatement1(statement.left), right=reduceArrayStatement1(statement.right))
    elif type(statement) is c_ast.Constant:
        if statement.type=='int' and (statement.value=='40'):
            return c_ast.Constant(type=statement.type,value='10')
        elif statement.type=='int' and (statement.value=='60'):
            return c_ast.Constant(type=statement.type,value='10')
        return statement
    elif type(statement) is c_ast.ArrayRef:
        return c_ast.ArrayRef(name=statement.name,subscript=reduceArrayStatement1(statement.subscript))
    else:
        return statement
