





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
