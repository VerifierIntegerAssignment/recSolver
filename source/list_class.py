"""
#Axiom Class
#Plain Python object to store Information about a Axiom
"""
class axiomclass(object):
 	def __init__(self, frame_axioms , output_equations , other_axioms, inputvariable, vfact, constraints, const_var_map, asserts, assumes,variables):
        	self.frame_axioms = frame_axioms
        	self.output_equations = output_equations
        	self.other_axioms = other_axioms
        	self.inputvariable = inputvariable
        	self.vfact = vfact
        	self.constraints = constraints
        	self.const_var_map = const_var_map
        	self.asserts = asserts
        	self.assumes = assumes
                self.variables = variables
                
        def getFrame_axioms(self):
        	return self.frame_axioms
        def getOutput_equations(self):
        	return self.output_equations
        def getOther_axioms(self):
        	return self.other_axioms
        def getInputvariable(self):
        	return self.inputvariable
        def getVfact(self):
        	return self.vfact
        def getConstraints(self):
        	return self.constraints
        def getConst_var_map(self):
        	return self.const_var_map
        def getAsserts(self):
    	        return self.asserts
    	def setAsserts(self,asserts):
		self.asserts=asserts
    	def getAssumes(self):
        	return self.assumes
    	def getVariables(self):
        	return self.variables
        def setFrame_axioms(self,frame_axioms):
        	self.frame_axioms=frame_axioms
        def setOutput_equations(self,output_equations):
        	self.output_equations=output_equations
        def setOther_axioms(self,other_axioms):
        	self.other_axioms=other_axioms
        def setInputvariable(self,inputvariable):
        	self.inputvariable=inputvariable
        def setVfact(self,vfact):
        	self.vfact=vfact
        def setConstraints(self,constraints):
        	self.constraints=constraints
        def setConst_var_map(self,const_var_map):
        	self.const_var_map=const_var_map
        def setAsserts(self,asserts):
    	        self.asserts=asserts
    	def setAssumes(self,assumes):
        	self.assumes=assumes
    	def setVariables(self,variables):
        	self.variables=variables

"""
#Sort Class
#Plain Python object to store Information about a Java  Class 
"""
class sortclass(object):
 	def __init__(self, sortname , varmap):
        	self.sortname = sortname
        	self.varmap = varmap
        def getSortname(self):
        	return self.sortname
        def getVarmap(self):
        	return self.varmap
        
        
"""

#Member Method Class
#Plain Python object to store Information about Member Method of a Java Class 
"""
class membermethodclass(object):
 	def __init__(self, methodname, returnType , inputvar, localvar, body, usedCounter, serialNo,tempoary, analysis_module, fun_decl):
        	self.methodname = methodname
        	self.inputvar = inputvar
        	self.returnType = returnType
        	self.localvar = localvar
        	self.body = body
        	self.usedCounter = usedCounter
        	self.serialNo = serialNo
        	self.tempoary = tempoary
                self.analysis_module = analysis_module
                self.fun_decl = fun_decl
        def getMethodname(self):
        	return self.methodname
        def getreturnType(self):
        	return self.returnType
        def getInputvar(self):
        	return self.inputvar
        def getLocalvar(self):
        	return self.localvar
        def getBody(self):
		return self.body
	def getUsedCounter(self):
		return self.usedCounter
	def getSerialNo(self):
		return self.serialNo
	def getTempoary(self):
		return self.tempoary
	def getFun_decl(self):
		return self.fun_decl
	def getAnalysis_module(self):
		return self.analysis_module
	def setInputvar(self, inputvar):
	        self.inputvar=inputvar
	def setLocalvar(self, localvar):
	        self.localvar=localvar
	def setBody(self, body):
		self.body=body
	def setUsedCounter(self, usedCounter):
		self.usedCounter=usedCounter
	def setSerialNo(self, serialNo):
		self.serialNo=serialNo
	def setTempoary(self,tempoary):
		self.tempoary=tempoary
	def setAnalysis_module(self,analysis_module):
		self.analysis_module=analysis_module
	def setFun_decl(self,fun_decl):
		self.fun_decl=fun_decl
"""

#Variable Class 

#Plain Python Object to store information about variable

"""
class variableclass(object):
	def __init__(self, variablename, variableType, modifiers, dimensions, initialvalue, structType):
        	self.variablename = variablename
        	self.variableType = variableType
        	self.modifiers = modifiers
        	self.dimensions = dimensions
        	self.initialvalue = initialvalue
        	self.structType = structType
	def getVariablename(self):
		return self.variablename
	def getVariableType(self):
		return self.variableType
	def getModifiers(self):
		return self.modifiers
	def getDimensions(self):
		return self.dimensions
	def getInitialvalue(self):
		return self.initialvalue
        def setInitialvalue(self,initialvalue):
		self.initialvalue=initialvalue
	def getStructType(self):
		return self.structType
	def setStructType(self,initialvalue):
		self.structType=structType


"""

#Expression Class
#Plain Python object to store Information about Java Expression 
"""
class expressionclass(object):
 	def __init__(self, expression, serialNo, isPrime, degree):
        	self.expression = expression
        	self.serialNo = serialNo
        	self.isPrime = isPrime
        	self.degree = degree
        def getExpression(self):
        	return self.expression
        def getSerialNo(self):
        	return self.serialNo
        def getIsPrime(self):
        	return self.isPrime
        def getDegree(self):
        	return self.degree
        def setExpression(self, expression):
		self.expression=expression
	def setSerialNo(self, serialNo):
		self.serialNo=serialNo
	def setIsPrime(self, isPrime):
		self.isPrime=isPrime
	def setDegree(self, degree):
		self.degree=degree


"""

#Block Class
#Plain Python object to store Information about Block of Java Expression 
"""
class blockclass(object):
 	def __init__(self, expression, predicate, serialNo ,isPrime ,degree):
        	self.expression = expression
        	self.predicate = predicate
        	self.serialNo = serialNo
        	self.isPrime = isPrime
        	self.degree = degree
        def getExpression(self):
        	return self.expression
        def getPredicate(self):
        	return self.predicate
        def getSerialNo(self):
        	return self.serialNo
        def getIsPrime(self):
        	return self.isPrime
        def getDegree(self):
        	return self.degree
        def setExpression(self, expression):
		self.expression=expression
	def setPredicate(self, predicate):
		self.predicate=predicate
	def setSerialNo(self, serialNo):
		self.serialNo=serialNo
	def setIsPrime(self, isPrime):
		self.isPrime=isPrime
       	def setDegree(self, degree):
		self.degree=degree


"""

#Block Class
#Plain Python object to store Information about if else Java Loop 
"""
class Ifclass(object):
 	def __init__(self, predicate, expressionif, expressionelse, serialNo ,isPrime ,degree):
        	self.predicate = predicate
        	self.expressionif = expressionif
        	self.expressionelse = expressionelse
        	self.serialNo = serialNo
        	self.isPrime = isPrime
        	self.degree = degree
        def getExpressionif(self):
        	return self.expressionif
        def getExpressionelse(self):
        	return self.expressionelse
        def getPredicate(self):
        	return self.predicate
        def getSerialNo(self):
        	return self.serialNo
        def getIsPrime(self):
        	return self.isPrime
        def getDegree(self):
        	return self.degree
        def setExpressionif(self, expressionif):
		self.expressionif=expressionif
	def setExpressionelse(self, expressionelse):
		self.expressionelse=expressionelse
	def setPredicate(self, predicate):
		self.predicate=predicate
	def setSerialNo(self, serialNo):
		self.serialNo=serialNo
	def setIsPrime(self, isPrime):
		self.isPrime=isPrime
       	def setDegree(self, degree):
		self.degree=degree


"""

#Struct Class
#Plain Python object to store Information about Struct (C Expression) 
"""
class structclass(object):
 	def __init__(self, name, isTypeDef, variablemap , defName, isPointer):
        	self.name = name
        	self.isTypeDef = isTypeDef
        	self.variablemap = variablemap
        	self.defName = defName
        	self.isPointer = isPointer
        def getName(self):
        	return self.name
        def getIsTypeDef(self):
        	return self.isTypeDef
        def getVariablemap(self):
        	return self.variablemap
        def getDefName(self):
        	return self.defName
        def getIsPointer(self):
        	return self.isPointer
        def setName(self, name):
		self.name=name
	def setIsTypeDef(self, isTypeDef):
		self.isTypeDef=isTypeDef
	def setVariablemap(self, variablemap):
		self.variablemap=variablemap
	def setDefName(self, defName):
		self.defName=defName
       	def setIsPointer(self, isPointer):
		self.isPointer=isPointer
