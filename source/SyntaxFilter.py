from sympy import *
from ply import lex




class typedefclass(object):
 	def __init__(self, flagStruct , typename, typevalue):
        	self.flagStruct = flagStruct
        	self.typename = typename
        	self.typevalue = typevalue
        def isFlagStruct(self):
        	return self.flagStruct
        def setFlagStruct(self,flagStruct):
        	self.flagStruct=flagStruct
	def getTypename(self):
        	return self.typename
        def setTypename(self,typename):
        	self.typename=typename
        def getTypevalue(self):
	        return self.typevalue
	def setTypevalue(self,typevalue):
        	self.typevalue=typevalue



class SLexerError(Exception): pass

class SLexer(object):
        
        

	primitive_types = {
    	'float': 'FLOAT',
    	'int': 'INT',
    	'long': 'LONG',
    	'_bool': '_BOOL',
    	'_complex': '_COMPLEX',
    	'short':'SHORT', 
    	'signed':'SIGNED',
    	'string': 'STRING',
    	'double': 'DOUBLE',
    	'enum':'ENUM',
    	'register':'REGISTER',
    	'volatile':'VOLATILE',
    	'struct':'STRUCT',
    	'union':'UNION',
    	'unsigned':'UNSIGNED',
    	'byte': 'BYTE',
    	'auto':'AUTO',
    	'_int128':'__INT128',
    	'char':'CHAR'
	}

	function_modifiers = [
    	'FINAL',
    	'NATIVE',
    	'STATIC'
	]

	struct_modifers = [
    	'TRANSIENT'
    	'NATIVE'
	]

	class_modifiers = {
    	'abstract': 'ABSTRACT',
    	'instanced': 'INSTANCED',
    	'native': 'NATIVE',
    	'noexport': 'NOEXPORT',
    	'transient': 'TRANSIENT',
    	'template': 'TEMPLATE'
	}

	access_modifiers = {
    	'private': 'PRIVATE',
    	'protected': 'PROTECTED'
	}

	function_parameter_modifiers = {
    	'extern': 'EXTERN',
    	'__extension__': '__EXTENSION__',
    	'inline':'INLINE',
    	'_inline_':'_INLINE_'
	}

	variable_modifiers = {
    	'automated': 'AUTOMATED',
    	'const': 'CONST',
    	'input': 'INPUT',
    	'localized': 'LOCALIZED',
    	'native': 'NATIVE',
    	'private': 'PRIVATE',
    	'protected': 'PROTECTED',
    	'transient': 'TRANSIENT',
	}

	reserved = {
    	'assert': 'ASSERT',
    	'auto': 'AUTO',
    	'_bool': '_BOOL',
    	'begin': 'BEGIN',
    	'bool': 'BOOL',
    	'long': 'LONG',
    	'short':'SHORT', 
    	'_complex': '_COMPLEX',
    	'signed':'SIGNED',
    	'double': 'DOUBLE',
    	'volatile':'VOLATILE',
    	'register':'REGISTER',
    	'unsigned':'UNSIGNED',
    	'union':'UNION',
    	'_int128':'__INT128',
    	'char':'CHAR',
    	'break': 'BREAK',
    	'byte': 'BYTE',
    	'case': 'CASE',
    	'class': 'CLASS',
    	'continue': 'CONTINUE',
    	'default': 'DEFAULT',
    	'do': 'DO',
    	'else': 'ELSE',
    	'end': 'END',
    	'enum': 'ENUM',
    	'extends': 'EXTENDS',
    	'false': 'FALSE',
    	'final': 'FINAL',
    	'float': 'FLOAT',
    	'for': 'FOR',
    	'goto': 'GOTO',
    	'if': 'IF',
    	'import': 'IMPORT',
    	'int': 'INT',
    	'intrinsic': 'INTRINSIC',
    	'invariant': 'INVARIANT',
    	'iterator': 'ITERATOR',
    	'new': 'NEW',
    	'simulated': 'SIMULATED',
    	'static': 'STATIC',
    	'string': 'STRING',
    	'struct': 'STRUCT',
    	'super': 'SUPER',
    	'switch': 'SWITCH',
    	'true': 'TRUE',
    	'while': 'WHILE',
    	# the following are keywords added by ulex
    	'typeof': 'TYPEOF',
    	'sizeof': 'SIZEOF',
    	'typedef': 'TYPEDEF',
    	'offsetof':'OFFSETOF',
    	'void':'VOID',
    	'restrict':'RESTRICT',
    	'__attribute__':'_ATTRIBUTE_',
    	'__asm__':'_ASM_',
    	'__asm':'_ASM',
    	'__typeof__':'_TYPEOF_',
    	'__real__':'__REAL_',
    	'__imag__':'__IMAG__',
    	'__builtin_types_compatible_p':'_BUILTIN_TYPES_COMATIIBLE_P',
    	'__const':'__CONST',
    	'__restrict':'_RESTRICT',
    	'__inline':'_INLINE',
    	'asm':'ASM',
    	'__attribute':'__ATTRIBUTE',
    	'extern': 'EXTERN',
	'__extension__': '__EXTENSION__',
	'inline':'INLINE',
    	'_inline_':'_INLINE_'
	}

	reserved.update(class_modifiers)
	reserved.update(variable_modifiers)

	tokens = [
    	'COMMENT',
    	'UNAME',
    	'INTEGER',
    	'HEX',
    	'SEMICOLON',
    	'LPAREN',
    	'RPAREN',
    	'LSQUARE',
    	'RSQUARE',
    	'LANGLE',
    	'RANGLE',
    	'LCURLY',
    	'RCURLY',
    	'ASSIGN',
    	'COMMA',
    	'PERIOD',
    	'LQUOTE',
    	'RQUOTE',
    	'USTRING',
    	'UFLOAT',
        'UCHAR',
    	'EQUAL',
    	'NEQUAL',
    	'OR',
    	'NOT',
    	'INCREMENT',
    	'DECREMENT',
    	'POWER',
    	'ADD',
    	'MULTIPLY',
    	'AND',
    	'MINUS',
    	'COLON',
    	'AEQUAL',
    	'SUEQUAL',
    	'MUEQUAL',
    	'DEQUAL',
    	'MDEQUAL',
    	'SEQUAL',
    	'MODULUS',
    	'SCONCAT',
    	'SCONCATSPACE',
    	'DIVIDE',
    	'REFERENCE',
    	'DIRECTIVE',
    	'AMPERSAND',
    	'BITWISE_AND',
    	'BITWISE_OR',
    	'LEFT_SHIFT',
    	'RIGHT_SHIFT',
    	'XOR',
    	'BITWISE_NOT',
    	'ID',
    	'LEQUAL',
    	'GEQUAL',
    	'IASSIGN',
    	'DASSIGN',
    	'ARROW',
    	'CONDOP'
    	] + list(reserved.values())

	t_LPAREN = r'\('
	t_RPAREN = r'\)'
	t_LSQUARE = r'\['
	t_RSQUARE = r'\]'
	t_LANGLE = r'\<'
	t_RANGLE = r'\>'
	t_LCURLY = r'\{'
	t_RCURLY = r'\}'
	t_LQUOTE = r'\"'
	t_RQUOTE = r'\"'
	t_ignore = '\r\t '
	t_SEMICOLON = r'\;'
	t_ASSIGN = r'\='
	t_COMMA = r','
	t_PERIOD = '\.'
	t_EQUAL = r'=='
	t_NEQUAL = r'!='
	t_OR = r'\|\|'
	t_NOT = r'!'
	t_INCREMENT = r'\+\+'
	t_DECREMENT = r'\-\-'
	t_POWER = r'\*\*'
	t_ADD = r'\+'
	t_MULTIPLY = r'\*'
	t_AND = r'\&\&'
	t_MINUS = r'-'
	t_COLON = r':'
	t_AEQUAL = r'\+='
	t_SUEQUAL = r'\-='
	t_MUEQUAL = r'\*='
	t_DEQUAL = r'/='
	t_MDEQUAL = r'%='
	t_SEQUAL = r'~='
	t_MODULUS = r'%'
	t_SCONCAT = r'\$'
	t_SCONCATSPACE = r'@'
	t_DIVIDE = r'/'
	t_BITWISE_AND = r'\&'
	t_BITWISE_OR = r'\|'
	t_LEFT_SHIFT = r'<<'
	t_RIGHT_SHIFT = r'>>'
	t_XOR = r'\^'
	t_BITWISE_NOT = r'~'
	t_LEQUAL = r'\<\='
	t_GEQUAL = r'>='
	t_IASSIGN = r'\+='
	t_DASSIGN = r'-='
	t_ARROW = r'->'
	t_CONDOP = r'\?'

	def t_DIRECTIVE(self,t):
    		r'\#(\w+)\s+(.+)'
	t_DIRECTIVE.__doc__ = r'\#(\w+)\s+(.+)'

	def t_REFERENCE(self,t):
    		r'([a-zA-Z0-9_\-]+)\s*\'([a-zA-Z0-9_\-\.]+)\''
    		return t
	t_REFERENCE.__doc__ = r'([a-zA-Z0-9_\-]+)\s*\'([a-zA-Z0-9_\-\.]+)\''

	def t_UNAME(self,t):
    		r'\'([a-zA-Z0-9_\- ]*)\''
    		return t
	t_UNAME.__doc__ = r'\'([a-zA-Z0-9_\- ]*)\''

	def t_USTRING(self,t):
    		r'"((\\{2})*|(.*?[^\\](\\{2})*))"'
    		return t
	t_USTRING.__doc__ = r'"((\\{2})*|(.*?[^\\](\\{2})*))"'

	def t_UFLOAT(self,t):
    		#r'[-+]?\d*?[.]\d+'
    		r'(([-+]?\d+)(\.\d+)(e(\+|-)?(\d+))? | ([-+]?\d+)e(\+|-)?(\d+) | ([-+]?\d+)(\.))([lL]|[fF])?'
    		if t.value[-1]=='f' or t.value[-1]=='F':
                    t.value = float(t.value[:-1])
                    if 'e' in str(t.value) or 'E' in str(t.value):
                        t.value=str(t.value)
                        if 'e' in t.value:
                            expo=Integer(t.value[t.value.index('e')+1:len(t.value)])
                        elif 'E' in t.value:
                            expo=Integer(t.value[t.value.index('E')+1:len(t.value)])
                        else:
                            expo=200
                        if expo>0:
                            t.value = Float(t.value,expo+1)
                        else:
                            t.value = Float(t.value,-1*expo*5)
                elif 'e' in t.value or 'E' in t.value:
                    if 'e' in t.value:
                        expo=Integer(t.value[t.value.index('e')+1:len(t.value)])
                    elif 'E' in t.value:
                        expo=Integer(t.value[t.value.index('E')+1:len(t.value)])
                    else:
                        expo=200
                    if expo>0:
                        t.value = Float(t.value,expo+1)
                    else:
                        t.value = Float(t.value,-1*expo*5)
                else:
                    t.value = Float(t.value)
    		return t
	#t_UFLOAT.__doc__ = r'[-+]?\d*?[.]\d+'
	t_UFLOAT.__doc__ = r'(([-+]?\d*)(\.\d+)(e(\+|-)?(\d+))? | ([-+]?\d+)e(\+|-)?(\d+) | ([-+]?\d+)(\.))([lL]|[fF])?'
	
	def t_HEX(self,t):
    		r'0[xX][0-9a-fA-F]+'
    		t.type = 'INTEGER'
    		t.value = int(t.value, 0)
    		return t
	t_HEX.__doc__ = r'0[xX][0-9a-fA-F]+'

	def t_INTEGER(self,t):
    		r'([-+]?\d+)([U])?'
                if 'U' not in t.value:
                    t.value = int(t.value)
    		return t
	t_INTEGER.__doc__ = r'([-+]?\d+)([U])?'


	def t_UCHAR(self,t):
                t.type = 'UCHAR'
                t.value = t.value
    		return t
	
	simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
        decimal_escape = r"""(\d+)"""
        hex_escape = r"""(x[0-9a-fA-F]+)"""
        escape_sequence = r"""(\\("""+simple_escape+'|'+decimal_escape+'|'+hex_escape+'))'
        cconst_char = r"""([^'\\\n]|"""+escape_sequence+')'
        char_const = "'"+cconst_char+"'"
	t_UCHAR.__doc__ = char_const


	def t_COMMENT(self,t):
    		r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
	t_COMMENT.__doc__ = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'

	def t_ID(self,t):
    		r'[a-zA-Z_][a-zA-Z_0-9]*'
    		t.type = self.reserved.get(t.value.lower(), 'ID')
    		return t
	t_ID.__doc__ = r'[a-zA-Z_][a-zA-Z_0-9]*'

	def t_newline(self,t):
    		r'\n+'
    		t.lexer.lineno += len(t.value)
	t_newline.__doc__ = r'\n+'

	def t_error(self,t):
    		pass

	def __init__(self,text):
	        self.program = []
        	self.text=text
                self.struct_list=[]
                self.type_struct_list=[]

    	def build(self, **kwargs):
        	""" Builds the lexer from the specification. Must be
            	called after the lexer object is created.

            	This method exists separately, because the PLY
            	manual warns against calling lex.lex inside
            	__init__
        	"""
        	self.lexer = lex.lex(object=self, **kwargs)
        def input(self, text):
        	self.lexer.input(text)
    	def token(self):
        	return self.lexer.token()
        def getAllTokens(self):
        	#fd = open(self.filename)
		#text = "".join(fd.readlines())
		self.input(self.text)
        	while True:
			tok = lex.token()
			if not tok: break
			self.program.append(tok)
		return self.program
		
	def getExterns(self,lex):
		nameStack=[]
		while True:
			tok = lex.token()
			if not tok: break
			if tok.type=='SEMICOLON':
				if not nameStack:
					return
			elif tok.type=='LCURLY':
				nameStack.append(tok)
			elif tok.type=='RCURLY':
				nameStack.pop()
				if not nameStack:
					return
		return
		
	def filterSyntax(self):
		#fd = open(self.filename)
		#text = "".join(fd.readlines())
		self.input(self.text)
		self.program=[]
		typedef_list=[]

		while True:
			tok = lex.token()
			if not tok: break
			if tok.type=='SEMICOLON' or tok.type=='LCURLY' or tok.type=='RCURLY':
				self.program.append(tok)
			else:
				if tok.type=='EXTERN' or tok.type=='__EXTENSION__':
					if tok.type=='__EXTENSION__':
						tok = lex.token()
						if tok.type=='TYPEDEF':
							typedef_list.append(self.getTypeDef(lex))
						else:
							self.getExterns(lex)
					else:
						self.getExterns(lex)
				elif tok.type=='TYPEDEF':
                                        term_type=self.getTypeDef(lex)
                                        temp_struct=[]
                                        if term_type is not None and type(term_type.getTypevalue()) is list and type(term_type.getTypename()) is list:
                                            for x in term_type.getTypevalue():
                                                temp_struct.append(x)
                                            if type(term_type.getTypename()) is list:
                                                for x in term_type.getTypename():
                                                    temp_struct.append(x)
                                                str_struct=self.showProgram(temp_struct)
                                                if 'struct' in str_struct or 'union' in str_struct:
                                                    self.type_struct_list.append("typedef "+str_struct+";")
					typedef_list.append(term_type)
				elif tok.type=='STRUCT' or tok.type=='UNION':
                                        list_struct=self.getStructUnionIgn(tok,lex)
                                        str_struct2=self.showProgram(list_struct)
                                        if '{' in str_struct2 and '}' in str_struct2:
                                            self.struct_list.append(str_struct2)
                                        else:
                                            for x_x in list_struct:
                                                self.program.append(x_x)

				else:
					self.program.append(tok)
					
			
		for item1 in typedef_list:
			for item2 in typedef_list:
				if not item1.isFlagStruct():
					key=item1.getTypename().value
					if item1!=item2:
						item3_mod=[]
						for item3 in item2.getTypevalue():
							if item3.type=='ID':
								if item3.value==key:
									for item4 in item1.getTypevalue():
										item3_mod.append(item4)
								else:
									item3_mod.append(item3)
							else:
								item3_mod.append(item3)
						item2.setTypevalue(item3_mod)

		
		#Create a subsitition Map
		type_value_map={}
		for item in typedef_list:
                        
			if not item.isFlagStruct():
				type_value_map[item.getTypename().value]=item.getTypevalue()
			else:
				if item.getTypevalue()[1] is not None and item.getTypevalue()[1].type=='ID':
					type_value_map[item.getTypename()[-1].value]=item.getTypevalue()
                                elif item.isFlagStruct()==True and item.getTypevalue()[1].type=='LCURLY' and item.getTypename() is not None:
                                        temp_stmt=[]
                                        temp_stmt.append(item.getTypevalue()[0])
                                        temp_stmt.append(item.getTypename()[0])
                                        type_value_map[item.getTypename()[-1].value]=temp_stmt
					
		program_mod=[]
		for item in self.program:
			if item.type=='ID' and item.value in type_value_map.keys():
				for item1 in type_value_map[item.value]:
					program_mod.append(item1)
			else:
				program_mod.append(item)
		
		self.program=program_mod
                
		return self.showProgram(self.program),self.struct_list,self.type_struct_list
	
	
	def getTypeDef(self,lex):
		nameStack=[]
		list_token=[]
		isStruct=False
		struct_token=[]
		tok = lex.token()
		if not tok: None
		list_token.append(tok)
		if tok.type=='STRUCT' or tok.type=='UNION':
			isStruct=True
			struct_token=self.getStructUnion(lex)
		while True:
			tok = lex.token()
			if not tok: break
			list_token.append(tok)
			if tok.type=='SEMICOLON':
				if not nameStack:
					if isStruct==True:
						typedefobj=typedefclass(isStruct, list_token[1:-1],[list_token[0]]+struct_token)
						return typedefobj
					else:
						typedefobj=typedefclass(False,list_token[-2],list_token[:-2])
						return typedefobj
			elif tok.type=='LCURLY':
				nameStack.append(tok)
			elif tok.type=='RCURLY':
				nameStack.pop()
		if isStruct==True:
			typedefobj=typedefclass(isStruct,list_token[1:-1],[list_token[0]]+struct_token)
			return typedefobj
		else:
			typedefobj=typedefclass(isStruct,list_token[-2],list_token[:-2])
		return typedefobj
	

	def showProgram(self,list_token):
		program_str=None
		for tok in list_token:
			if tok.type=='LCURLY' or tok.type=='RCURLY':
				if program_str is None:
					program_str=' '+str(tok.value)+'\n'
				else:
					program_str+=' '+str(tok.value)+'\n'
			elif tok.type=='SEMICOLON':
				if program_str is None:
					program_str=str(tok.value)+'\n'
				else:
					program_str+=str(tok.value)+'\n'
			else:
				if tok.type=='LPAREN' or tok.type=='RPAREN':
					if program_str is None:
						program_str=str(tok.value)
					else:
						program_str+=str(tok.value)
				else:
					if program_str is None:
						program_str=' '+str(tok.value)
					else:
						program_str+=' '+str(tok.value)

		return program_str



	def getStructUnion(self,lex):
		nameStack=[]
		list_token=[]
		while True:
			tok = lex.token()
			if not tok: break
			list_token.append(tok)
			if tok.type=='LCURLY':
				nameStack.append(tok)
			elif tok.type=='RCURLY':
				nameStack.pop()
			if not nameStack: return list_token
		return list_token

	def getStructUnionIgn(self,pass_tok,lex):
		nameStack=[]
		list_token=[]
		list_token.append(pass_tok)
		while True:
			tok = lex.token()
			if not tok: break
			list_token.append(tok)
			if tok.type=='LCURLY':
				nameStack.append(tok)
				#list_token.append(tok)
			elif tok.type=='RCURLY':
				nameStack.pop()
				#list_token.append(tok)
			elif tok.type=='SEMICOLON':
				if not nameStack: 
					#list_token.append(tok)
					return list_token
				#else: 
					#list_token.append(tok)
		return list_token
	
	def createCommonEquation(self,variable_const_map,counter):
		self.input(self.text)
		final_expression=''
		while True:
			tok = lex.token()
			if not tok: break
			if tok.type=='ID':
				if tok.value not in variable_const_map.keys() and tok.value is not 'T' and tok.value is not 'n':
					counter=counter+1
					final_expression+='C'+str(counter)
				else:
					final_expression+=str(tok.value)
			else:
				final_expression+=str(tok.value)
		return final_expression

	def wolframalphaConstruct(self):
		self.input(self.text)
		Opstatus=False
		final_expression=''
		extra=''
		while True:
			tok = lex.token()
			if not tok: break
			if (tok.type=='ID' or tok.type=='INTEGER') and Opstatus==False:
				Opstatus=True
				final_expression+=str(tok.value)
			elif (tok.type=='ID' or tok.type=='INTEGER') and Opstatus==True:
				Opstatus=True
				final_expression+='*'+extra
				final_expression+=str(tok.value)
				extra=''
			elif tok.type=='ADD':
				Opstatus=False
				final_expression+=extra+str(tok.value)
				extra=''
			elif tok.type=='DIVIDE':
				Opstatus=False
				final_expression+=extra+str(tok.value)
				extra=''
			elif tok.type=='POWER':
				Opstatus=False
				final_expression+=extra+str(tok.value)
				extra=''
			elif tok.type=='MINUS':
				Opstatus=False
				final_expression+=extra+str(tok.value)
				extra=''
			elif tok.type=='MULTIPLY':
				Opstatus=False
				final_expression+=str(tok.value)
				extra=''
			else:
				if Opstatus==True:
					extra+=str(tok.value)
				else:
					final_expression+=str(tok.value)
		return final_expression+extra
	