
import sys
import os


currentdirectory = os.path.dirname(os.path.realpath(__file__))


sys.path.append(currentdirectory+"/packages/mpmath/")
sys.path.append(currentdirectory+"/packages/sympy/")

from sympy import *
from sympy.core.relational import Relational


import utiles_translation
import FOL_translation
import fun_utiles
import copy
from itertools import permutations


ConstraintCount=0



#rec_equ="X(0)=A;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,ite(X(_n1)<B,X(_n1)+2,X(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+F"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;M(0)=j;M(_n1+1)=X(_n1)+M(_n1);X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"
#rec_equ="X(0)=A;X(_n1+1)=ite(B>0,X(_n1)+1,ite(C>0,X(_n1)+2,X(_n1)))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1==1,1,(_n1+1)*X(_n1))"
#rec_equ="X(0)=0;X(_n1+1)=ite(_n1==1,1,(1+X(_n1)))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1==1,1,(_n1+1)*X(_n1));Y(0)=1;Y(_n1+1)=ite(_n1==1,1,(_n1+1)*Y(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B)"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B);Y(0)=1;Y(_n1+1)=ite(C>0,Y(_n1)+A,Y(_n1)+B)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1)+5,X(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"
#rec_equ="X(0)=2;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1)+5,X(_n1)-5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-5)"
#rec_equ="X(0)=10;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-15)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+15)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+15,X(_n1)-5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-15,X(_n1)+5)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1)+5,X(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<50,X(_n1)+1,ite(_n1<70,X(_n1)+2,ite(_n1<90,X(_n1)+3,X(_n1))))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<A,X(_n1)+1,ite(_n1<B,X(_n1)+2,ite(_n1<C,X(_n1)+3,X(_n1))))"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,X(_n1)+2)"

#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<A,X(_n1)+1,X(_n1)+2)"





#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(B>0,X(_n1)+Y(_n1),ite(C>0,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(B>0,X(_n1)+1,ite(C>0,X(_n1)+Y(_n1),X(_n1)))"


#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=X(_n1)+1;Y(_n1+1)=X(_n1)+Y(_n1)+1"


#rec_equ="X(0)=A;X(_n1+1)=X(_n1)+1"


#var = "_n1"

def solve_recurrence(rec_equ,var):
    
    rec_list = rec_equ.split(';')
    
    list_equations=[]
    
    list_solutions = []
    
    for rec_eq in rec_list:
        
        expression =[]
        left_side = rec_eq[0 : rec_eq.find('=')]
        right_side = rec_eq[rec_eq.find('=')+1:len(rec_eq)]

        utiles_translation.resetGlobal()
        statement_temp = utiles_translation.createASTStmt(left_side)
        left_side_update = utiles_translation.expressionCreator_C(statement_temp)
        if left_side_update is not None:
            left_side_update=eval(left_side_update)
        
        utiles_translation.resetGlobal()
        statement_temp = utiles_translation.createASTStmt(right_side)
        right_side_update = utiles_translation.expressionCreator_C(statement_temp)
        if right_side_update is not None:
            right_side_update=eval(right_side_update)
        
        if utiles_translation.expr_find(left_side_update,eval("['"+var+"']"))==True:
            
            expression.append('i1')
            expression.append('0')
            expression.append(var)
            expression.append(left_side_update)
            expression.append(right_side_update)

        else:
            
            expression.append('i0')
            expression.append('0')
            expression.append(left_side_update)
            expression.append(right_side_update)

        list_equations.append(expression)
    
    
    results = rec_solver(list_equations)
    
    
    list_equations=[]
    
    closed_formed=[]
    
    for result in results:
        if result[0]=='i0' or result[0]=='i1':
            list_equations.append(result)
        else:
            if result[0]=='i2':
                closed_formed.append(result)
    if len(list_equations)>1:
        results,equations_map,basecase_map = mutual_rec_solver(list_equations,var)
        
        
        for result in results:
            closed_formed.append(result)
            
    
    #var_map={}
    #for x in list_equations:
    #    print FOL_translation.wff2z3_update(x)
    #print var_map
    #print '-----------------'
    
    
    results, axoims = solve_conditional_rec(equations_map, basecase_map, list_equations, var)
    
    if results is not None:
    
        for result in results:
            closed_formed.append(result)


    print 'NOt ABLE TO SOLVE FOLLOWING'
    if len(list_equations)>0:
        for x in list_equations:
            if x[0]=='i1':
                print FOL_translation.wff2string1(x)
    else:
        print 'No Equations Left'
    
    print ''
    print 'CLOSED FORM SOLUTION'
    if len(closed_formed)>0:    
        for result in closed_formed:
            
            print FOL_translation.wff2string1(result)
    else:
        print 'No Solution'
    
    print ''
    print 'ADDITIONAL AXOIMS'
    if axoims is not None:
        if len(axoims)>0:    
            for axoim in axoims:
                print FOL_translation.wff2string1(axoim)
        else:
            print 'No Additional Axoims'
    else:
        print 'No Additional Axoims'
            
    
    #for equation in list_equations:
    #    print equation
        
    #Conditional 
    #print solve_rec(list_equations[1],list_equations[0])
        

"""
Mutual Recurrences Solving Module
#Add by Pritom Rajkhowa

"""

def mutual_rec_solver(list_equations,var):
    equation_map={}
    base_map={}
    fun_map={}
    coeff_map={}
    main_solutions=[]
    
    for axiom in list_equations:
        if axiom[0]=='i1':
             lefthandstmt=FOL_translation.expr2string1(axiom[3])
	     lefthandstmt=lefthandstmt.strip()
             equation_map[str(simplify(lefthandstmt))]=axiom
             
             new_expr=copy.deepcopy(axiom[3])
             
             new_expr = fun_utiles.expr_replace(new_expr,eval("['+',"+"['"+axiom[2]+"'],['1']]"),eval("['"+axiom[2]+"']"))
             
             fun_map[str(simplify(lefthandstmt))]=new_expr
             
	if axiom[0]=='i0':
	     lefthandstmt=FOL_translation.expr2string1(axiom[2])
	     lefthandstmt=lefthandstmt.strip()
	     base_map[str(simplify(lefthandstmt))]=axiom
    
    
    
    for x in equation_map.keys():
        #print x
        #print FOL_translation.expr2string1(equation_map[x][4])
        
        equ_map = {}
        
        coeff_expr = simplify(FOL_translation.expr2string1(equation_map[x][4]))
        
        for y in fun_map.keys():
            
            term = simplify(FOL_translation.expr2string1(fun_map[y]))
            
            equ_map[str(term)] = coeff_expr.coeff(term)
            
            coeff_expr = coeff_expr - term*equ_map[str(term)]
            
            #print coeff_expr
            
        equ_map[None] = coeff_expr
        
        coeff_map[x] = equ_map
            
    new_coeff_map = copy.deepcopy(coeff_map)
    
    group_map={}
    
    
    for x in new_coeff_map.keys():
        
        if x is not None:
        
            group_list=None
                
            for y in new_coeff_map.keys():
                if x!=y:
                    if y in coeff_map.keys() and x in coeff_map.keys():
                    
                        ret = isMutualRecurGroup(coeff_map[y],coeff_map[x])
                        
                        if ret is not None:
                            if group_list is None:
                                group_list=[]
                                group_list.append(x)
                                group_list.append(y)
                                del coeff_map[y]
                            else:
                                group_list.append(y)
                                del coeff_map[y]
            if group_list is not None and x in group_list and x in coeff_map.keys():
                del coeff_map[x]
                group_map[x]=group_list
        
    for x in group_map.keys():
        group_list = group_map[x]
        if group_list is not None and len(group_list)>0:
            
            new_coeff_map2 = update_cofficent(group_list, new_coeff_map, var)
            
            solutions = solve_mutual_rec(group_list, new_coeff_map2, equation_map, base_map, var)
            
            if solutions is not None:
                
                for solution in solutions:
                    
                    main_solutions.append(solution)
                    
                    stmt1 = FOL_translation.expr2string1(solution[3])
                    
                    term1=str(simplify(stmt1).subs(simplify(str(var)),simplify(str(var)+"+1")))
                    
                    term2=str(simplify(stmt1).subs(simplify(str(var)),0))
                    
                    if term1 in equation_map.keys():
                    
                        if equation_map[term1] in list_equations:
                            
                            list_equations.remove(equation_map[term1])
                        
                        del equation_map[term1]
                        
                    if term2 in base_map.keys():
                        
                        if base_map[term2] in list_equations:
                            
                            list_equations.remove(base_map[term2])

                        del base_map[term2]
                    for x in equation_map:
                        e = equation_map[x]
                        for y in solutions:
                            e[4] = fun_utiles.expr_replace(e[4],y[3],y[4])
                    for x in base_map:
                        e = base_map[x]
                        for y in solutions:
                            e[3] = fun_utiles.expr_replace(e[3],y[3],y[4])
    
    
    
    return main_solutions,equation_map,base_map

                 
    





def solve_mutual_rec(group_list, new_coeff_map, equation_map, base_map, var):

    list_of_values=[]
    
    solutions=[]
    
    for x in group_list:
        list_of_value=[]
                
        factor,non_coeff = iscofficentEqual(new_coeff_map[x], var)
                
        if non_coeff is None:
            return None
            
        utiles_translation.resetGlobal()
        
        if factor is None:
            
            return None
        
        statement_temp = utiles_translation.createASTStmt(factor)
        list_of_value.append(utiles_translation.expressionCreator_C(statement_temp))
        
        utiles_translation.resetGlobal()
        statement_temp = utiles_translation.createASTStmt(non_coeff)
        list_of_value.append(utiles_translation.expressionCreator_C(statement_temp))
        
        term1 = simplify(x).subs(simplify(str(var)+"+1"),0)
        term2 = str(base_map[str(term1)][3])
        list_of_value.append(term2)
        term3 = copy.deepcopy(equation_map[x][3])
        term3 = fun_utiles.expr_replace(term3,eval("['+',"+"['"+var+"'],['1']]"),eval("['"+var+"']"))
        list_of_value.append(term3)
        list_of_values.append(list_of_value)
        
    count=0
    const_expr=''
    const_expr_end=''
    const_coeff=''
    const_coeff_end=''
    const_value=None
    
    
    for list_of_value in list_of_values:
        
        const_value=list_of_value[0]

        if count<len(list_of_values)-1:
            const_expr+="['+',"+list_of_value[2]+","
            const_expr_end+="]"
            const_coeff+="['+',"+str(list_of_value[1])+","
            const_coeff_end+="]"
        else:
            const_expr+=str(list_of_value[2])
            const_coeff+=str(list_of_value[1])
            
        count=count+1
        
    for list_of_value in list_of_values:
                
        express_main="['i2', '0', '"+var+"',"+str(list_of_value[3])+",['+',"+"['+',"+"['*',['*',['power',['"+str(len(list_of_values))+"'],['"+var+"']],"+"['power',"+const_value+",['"+var+"']]],"+const_expr+const_expr_end+"]"+","+"['+',"+const_coeff+const_coeff_end+",['/'"+",['*',"+const_value+",['-',['1'],['*',['power',['"+str(len(list_of_values))+"'],['"+var+"']],['power',"+const_value+",['"+var+"']]]]],"+"['-',['1'],['*',['"+str(len(list_of_values))+"'],"+const_value+"]]]]],"+str(list_of_value[1])+"]]"

        solutions.append(eval(express_main))
        
    return solutions





def iscofficentEqual(new_coeff,var):
    status=True
    list=new_coeff.keys()
    temp_map={}
    non_coeff=None
    for x in new_coeff.keys():
        if x is not None:
            temp_map[str(new_coeff[x])]=str(new_coeff[x])
        else:
            if var not in str(new_coeff[x]):
                non_coeff=str(new_coeff[x])
    if len(temp_map)==1:
        return temp_map.keys()[0],non_coeff
        
    else:
        return None,non_coeff
    


        

def update_cofficent(group_list, new_coeff, variable):
    
    key_map={}
    
    new_coeff2 = copy.deepcopy(new_coeff)
    
    for x in group_list:
        
        term1=simplify(x).subs(simplify(str(variable)+"+1"),variable)
        
        key_map[str(term1)] = str(x)
        
    for x in new_coeff.keys():
        if x is not None and x not in key_map.values():
            del new_coeff2[str(x)]
        if x in new_coeff2.keys():
            for y in new_coeff[x]:
                if y is not None and y not in key_map.keys():
                    del new_coeff2[x][y]
                
    return new_coeff2



def solve_conditional_rec(equations_map, basecase_map, list_equations, var):
    
        tuple_lists=[]
        
        solution_list=None
        
        additional_axoims=None
        
        for x in equations_map.keys():
            
            tuple_list=[]
            
            tuple_list.append(x)
            
            map_con_expression={}
            
            map_fun = {}
            
            map_var = {}
            
            condition_map_constrt(equations_map[x][4],map_con_expression)
            
            tuple_list.append(equations_map[x])#1
            
            tuple_list.append(map_fun)#2
            
            tuple_list.append(map_var)#3
            
            fun_utiles.getAllVarFun(equations_map[x][4],map_fun,map_var)
            
            map_fun = {}
            
            map_var = {}
            
            fun_utiles.getAllVarFun(equations_map[x][3],map_fun,map_var)
            
            tuple_list.append(map_fun)#4
            
            tuple_list.append(map_var)#5
            
            tuple_list.append(map_con_expression)#6
            
            tuple_lists.append(tuple_list)
 
        temp_tuple_lists=copy.deepcopy(tuple_lists)
        
        group_lists=[]
        
        for x in tuple_lists:
            
            if x in temp_tuple_lists:
                
                group_list=[]
                
                group_list.append(x)
                
                for y in temp_tuple_lists:
                    if x!=y and x[2]==y[2]:
                        
                        group_list.append(y)
                        
                        temp_tuple_lists.remove(y)
                        
                if len(group_list)>0:
                    
                    group_lists.append(group_list)
    
        for group_list in group_lists:   
            
            soln,axoims = rec_solve_conditional(group_list, equations_map, basecase_map, list_equations, var) 
            
            if axoims is not None:
                
                if additional_axoims is None:
                    
                    additional_axoims = axoims
                    
                else:
                    
                    additional_axoims += axoims

                
                
            
            if  soln is not None:
                
                if solution_list is None:
                    
                    solution_list = soln
                    
                else:
                    
                    solution_list+=soln
                
        return solution_list,additional_axoims



def rec_solve_conditional(group_list, equations_map,basecase_map, list_equations, var):
    
    solution_list=[]
    
    additional_axoims=None
    
    if len(group_list)==1:
        
        solution_type=None
        
        for x in group_list:

            for y in x[6]:
                
                z = x[6][y]
                                
                if z[0] is not None:
                    
                    
                    if fun_utiles.isFunctionPresent(z[0])==True:
                        
                        if solution_type==None:
                            
                           solution_type='Function'
                           
                        elif solution_type=='Counter' or solution_type=='Constant' or solution_type=='Base Case':
                            
                            solution_type='Function'
                            
                        else:
                            solution_type='Function'
                            
                        z.append(solution_type)
                        
                    elif fun_utiles.isVariablePresent(z[0])==True and fun_utiles.isFunctionPresent(z[0])!=True:
                        
                        if solution_type==None:
                            
                            if z[0][0]=='==' and fun_utiles.isFunctionPresent(x[6][y][1])==None and fun_utiles.isVariablePresent(x[6][y][1])==None :
                                
                                solution_type='Base Case'
                                
                            elif (z[0][0]=='==' or z[0][0]=='!=') and z[0][1][0]=='%' and z[0][1][1][0]==var and fun_utiles.is_number(z[0][1][2][0])==True:
                                
                                
                                solution_type='Periodic'
                                
                            else:
                                
                                solution_type='Counter'
                                
                        elif solution_type!='Function':
                            
                            solution_type='Counter'
                            
                        z.append(solution_type)
                        
                        if solution_type=='Periodic':
                            
                            z.append(z[0][1][2][0])
                            
                            z.append(z[0][0])
                    else:
                        
                        if solution_type==None:
                            
                            solution_type='Constant'
                            
                        elif solution_type!='Function' and solution_type!='Counter' and solution_type!='Base Case':
                            
                            solution_type='Constant'
                            
                        z.append(solution_type)                        
                else:
                    z.append(None)
                
            if  solution_type=='Constant':
                
                soln = solveConstantType(x, equations_map, basecase_map, list_equations)
                
                if soln is not None:
                    
                    solution_list.append(soln)
                    
            elif  solution_type=='Base Case':
            
                soln = solveBaseCaseType(x, equations_map, basecase_map, list_equations)
                
                if soln is not None:
                    
                    solution_list.append(soln)

            elif  solution_type=='Periodic':
                
                soln = solvePeriodicType(x, equations_map, basecase_map, list_equations)
                
                if soln is not None:
                    
                    solution_list.append(soln)


            elif  solution_type=='Counter':
                
                soln, axoims = solveCounterType(x, equations_map, basecase_map, list_equations)
                
                
                if axoims is not None:
                    
                    if additional_axoims is None:
                        
                        additional_axoims=axoims
                        
                    else:
                        
                        additional_axoims=axoims+additional_axoims
                
                #soln=None
                
                if soln is not None:
                    
                    solution_list.append(soln)
                
            elif  solution_type=='Function':
                
                soln, axoims = solveFunctionType(x, equations_map, basecase_map, list_equations)
                                
                if axoims is not None:
                    
                    if additional_axoims is None:
                        
                        additional_axoims=axoims
                        
                    else:
                        
                        additional_axoims=axoims+additional_axoims
                
                        
                if soln is not None:
                    
                    solution_list.append(soln)
            
    
    return solution_list,additional_axoims
                



def constructInfoSystem(e, equations_map, basecase_map, list_equations):
    
    global ConstraintCount
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    e_solution=None
    
    e_end=''
    
    close_form=None
    
    
    for x in e[6]:
        
        list=[]
        
        new_e=eval("['"+e[1][0]+"','"+e[1][1]+"','"+e[1][2]+"',"+str(e[1][3])+","+str(e[6][x][1])+"]")
        
        ConstraintCount = ConstraintCount+1
        
        e_new_base=copy.deepcopy(e_base)
        
        e_new_base[-1]=eval("['_CV"+str(ConstraintCount)+"']")
        
        
        sol = solve_rec(new_e,e_new_base)
        
                
        if sol is not None:
            
            list.append(e[6][x][2])
                    
            if e[6][x][0] is not None:
                
                e[6][x][0] = fun_utiles.expr_replace(e[6][x][0],sol[-2],sol[-1])
                
                e_new = copy.deepcopy(e[6][x][0])
        
                #e_new = fun_utiles.expr_replace(e_new,sol[-2],sol[-1])
                
            else:
                
                e_new=None
                
            list.append(sol)
            
            list.append(e_new)
            
                        
            if e_new is not None:
                
                
                constraint_list=[]
                
                equation_list=[]
                
                e_new1 = copy.deepcopy(sol[-1])
                                
                e_new1_in = copy.deepcopy(sol[-1])
                
                e_new1_in = fun_utiles.expr_replace(e_new1_in,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['1']]"))
                
                                
                
                if e_new1==e_new1_in:
                    
                    list.append('constant')
                
                else:
                
                    constraint_in =  eval("['s0',['<=',"+str(e_new1_in)+","+str(e_new1)+"]]")
                    
                
                    equation_list.append(constraint_in)
                    
                    constraint_list.append(FOL_translation.wff2z3_update(constraint_in))
                
                
                    var_map={}
    
                    FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                    vfacts=[]
                
                    for vfact in var_map:
                        vfacts.append(var_map[vfact])

                    status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')

                    if 'Counter Example' in status:
                    
                        list.append('increasing')
                    
                    else:
                    
                        constraint_list=[]
                        
                        equation_list=[]
                
                        constraint_de =  eval("['s0',['>=',"+str(e_new1_in)+","+str(e_new1)+"]]")
                        
                    
                        equation_list.append(constraint_de)
                        
                        constraint_list.append(FOL_translation.wff2z3_update(constraint_de))
                
                        var_map={}
    
                        FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                        vfacts=[]
                
                        for vfact in var_map:
                            
                            vfacts.append(var_map[vfact])

                        status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                                            
                        if 'Counter Example' in status:
                        
                            list.append('decreasing')

        
                
                equation_list=[]
                
                constraint_list=[]
                
                #e_new1 = fun_utiles.expr_replace(e_new1,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['_CS"+str(ConstraintCount)+"']]"))
                
                
                e_new = fun_utiles.expr_replace(e_new,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['1']]"))
                                
                
                e_new2 = copy.deepcopy(e_new)
                
                e_new2 = fun_utiles.expr_complement(e_new2)
                
                e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+e[1][2]+"']"),eval("['_CE"+str(ConstraintCount)+"']"))

                
                equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(ConstraintCount)+"'],['"+e[1][2]+"']],"+"['<',['"+e[1][2]+"'],['_CE"+str(ConstraintCount)+"']]"+"],"+str(e_new)+"]]")
            
                equation2 = eval("['s0',"+str(e_new2)+"]")
                
                constraint1 = eval("['a',['<=',['0'],['_CE"+str(ConstraintCount)+"']]]")
                
                constraint11 = eval("['a',['<=',['0'],['_CS"+str(ConstraintCount)+"']]]")
                
                constraint2 = eval("['a',['<',['_CS"+str(ConstraintCount)+"'],['_CE"+str(ConstraintCount)+"']]]")
                
                
                list.append(ConstraintCount)
                
                list.append(equation1)
                list.append(equation2)
                list.append(constraint1)
                list.append(constraint11)
                list.append(constraint2)
                
                #print FOL_translation.wff2z3_update(equation1)
                constraint_list.append(FOL_translation.wff2z3_update(equation1))
                equation_list.append(equation1) 
                
                #print FOL_translation.wff2z3_update(equation2)
                constraint_list.append(FOL_translation.wff2z3_update(equation2))
                equation_list.append(equation2)
                
                #print FOL_translation.wff2z3_update(constraint1)
                constraint_list.append(FOL_translation.wff2z3_update(constraint1))
                equation_list.append(constraint1)
                
                #print FOL_translation.wff2z3_update(constraint2)
                constraint_list.append(FOL_translation.wff2z3_update(constraint2))
                equation_list.append(constraint2)
                
                
                var_map={}
    
                FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                vfacts=[]
                
                for vfact in var_map:
                    vfacts.append(var_map[vfact])

                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                
                
                if 'Successfully Proved' in status:
                    
                    list.append('Always True')
                    
                else:
                
                    e_new3 = copy.deepcopy(e_new)
        
                    #e_new3 = fun_utiles.expr_replace(e_new3,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['_CS"+str(ConstraintCount+1)+"']]"))
                    #e_new3 = fun_utiles.expr_replace(e_new3,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['_CS"+str(ConstraintCount+1)+"']]"))
                
                    e_new4 = copy.deepcopy(e_new3)
                
                    e_new4 = fun_utiles.expr_complement(e_new4)
                
                    e_new4 = fun_utiles.expr_replace(e_new2,eval("['"+e[1][2]+"']"),eval("['_CE"+str(ConstraintCount+1)+"']"))

                
                    equation3 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(ConstraintCount+1)+"'],['"+e[1][2]+"']],"+"['<',['"+e[1][2]+"'],['_CE"+str(ConstraintCount+1)+"']]"+"],"+str(e_new1)+"]]")
            
                    equation4 = eval("['s0',"+str(e_new4)+"]")
                
                    constraint3 = eval("['a',['==',['_CE"+str(ConstraintCount)+"'],['_CS"+str(ConstraintCount+1)+"']]]")
                
                    constraint4 = eval("['a',['<',['_CS"+str(ConstraintCount+1)+"'],['_CE"+str(ConstraintCount+1)+"']]]")
                
                    constraint_list.append(FOL_translation.wff2z3_update(equation3))
                    equation_list.append(equation3) 
                
                    constraint_list.append(FOL_translation.wff2z3_update(equation4))
                    equation_list.append(equation4)
                
                    constraint_list.append(FOL_translation.wff2z3_update(constraint3))
                    equation_list.append(constraint3)
                
                    constraint_list.append(FOL_translation.wff2z3_update(constraint4))
                    equation_list.append(constraint4)
                
                    var_map={}
    
                    FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                    vfacts=[]
                
                    for vfact in var_map:
                        vfacts.append(var_map[vfact])

                    status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                
                    if 'Successfully Proved' in status:
                        list.append('No Repeat')
            
            if e_new is not None:
                
                constraint_list=[]
            
                e_cond = copy.deepcopy(e_new)
            
                e_cond = fun_utiles.expr_replace(e_cond,eval("['"+e[1][2]+"']"),eval("['0']"))
                
                e_cond = fun_utiles.expr_replace(e_cond,e_base[-2],e_base[-1])
                
                e_cond = eval("['s0',"+str(e_cond)+"]")
                
                constraint_list.append(FOL_translation.wff2z3_update(e_cond))
                
                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                                
                if 'Counter Example' in status:
                    
                    list.append('Initial')
                                                                                
                elif 'Successfully Proved' in status:
                    
                    list.append('Never Initial')
                    
                else:
                    
                    list.append(e_cond)

            else:
                
                list.append(None)
                list.append(str(ConstraintCount))
            
            e[6][x].append(list)
            
                
        else:
            
            return None

    return e



def solveCounterType(e, equations_map, basecase_map, list_equations):

    new_e = constructInfoSystem(e, equations_map, basecase_map, list_equations)
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    additional_axoims=None

    
    if  new_e is not None:
        
        constraint_list=[]
        
        equation_list=[]
        
        for x in e[6]:
                        
            if len(e[6][x][-1])>5 :
                
                
                constraint_list.append(FOL_translation.wff2z3_update(e[6][x][-1][5]))
                
                equation_list.append(e[6][x][-1][5])
                
                constraint_list.append(FOL_translation.wff2z3_update(e[6][x][-1][6]))
                
                equation_list.append(e[6][x][-1][6])
                
                constraint_list.append(FOL_translation.wff2z3_update(e[6][x][-1][7]))
                
                equation_list.append(e[6][x][-1][7])
                
                constraint_list.append(FOL_translation.wff2z3_update(e[6][x][-1][8]))
                
                equation_list.append(e[6][x][-1][8])
                
                constraint_list.append(FOL_translation.wff2z3_update(e[6][x][-1][9]))
                
                equation_list.append(e[6][x][-1][9])
                
        var_map={}
        
        FOL_translation.getEqVariFunDetails(equation_list,var_map)
        
        vfacts=[]
        
        for vfact in var_map:
            vfacts.append(var_map[vfact])
                            
        status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
        
        if 'Counter Example' in status:
            
            map_counter_CE={}
            
            map_counter_CS={}
            
            map_counter_others={}
            
            values = status[status.index('[')+1:len(status)-1-status[::-1].index(']')].split(',')
            
            
            for x in values:
                if '_f =' not in x and '->' not in x and '[' not in x and ']' not in x:
                    y = x.split('=')
                    key = y[0].replace('\n','')
                    key = key.strip()
                    value = y[1].replace('\n','')
                    value = value.strip()
                    if '_CE' in key and fun_utiles.is_number(value):
                        map_counter_CE[key]= value
                    elif '_CS' in key and  fun_utiles.is_number(value):
                        map_counter_CS[key] = value
                    else:
                        map_counter_others[key] = value
                        
            if len(map_counter_others)==0:
                
                list_values = map_counter_CE.values()
            
                list_values = sorted(list_values)
        
            
                list_sort = []
            
                soln_start=None
            
                soln_end=None
            
                prv_value=None
            
                else_value=None
            
                constraints=None
            
            
                if len(list_values)==len(e[6])-1:
                
                    for x in list_values:
                    
                        for key,value in map_counter_CE.iteritems():
                        
                            if value==x:
                            
                                list_sort.append(key)
                            
                    for y in list_sort:
                    
                        for x in e[6]:
                        
                            if e[6][x][-1][0] is not None:
                            
                                if '_CE'+str(e[6][x][-1][4])==y:
                                
                                
                                    if constraints is None:
                                        
                                        constraint_list.append('_CS'+str(e[6][x][-1][4])+"==0")
                                    
                                        constraints = str(e[6][x][-1][4])
                                        
                                    else:
                                    
                                        constraint_list.append('_CS'+str(e[6][x][-1][4])+"==_CE"+constraints)
                                    
                                        constraints = str(e[6][x][-1][4])

                                                                    
                                
                                    if soln_start is None:
                                    
                                    
                                        cond = copy.deepcopy(e[6][x][-1][2])
                                    
                                        cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x][-1][1][2]+"']"),eval("['-',['"+e[6][x][-1][1][2]+"'],['1']]"))
                                    
                                        stmt = copy.deepcopy(e[6][x][-1][1][4])
                                    
                                        stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x][-1][4])+"']"),e_base[3])
                                    
                                        prv_value = copy.deepcopy(stmt)
                                    
                                        prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x][-1][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x][-1][4])+"'],['1']]"))
                                    
                                        #soln_start="['"+e[6][x][-1][1][0]+"','"+e[6][x][-1][1][1]+"','"+e[6][x][-1][1][2]+"',"+str(e[6][x][-1][1][3])+",['ite',['==',['"+e[6][x][-1][1][2]+"'],['0']]"+","+str(e_base[3])+",['ite',"+str(cond)+","+str(stmt)
                                        soln_start="['"+e[6][x][-1][1][0]+"','"+e[6][x][-1][1][1]+"','"+e[6][x][-1][1][2]+"',"+str(e[6][x][-1][1][3])+",['ite',"+str(cond)+","+str(stmt)
                                        #soln_end="]]"
                                        soln_end="]"
                                    

                                    
                                    
                                    
                                    else:
                                    
                                        if prv_value is not None:
                                        
                                            cond = copy.deepcopy(e[6][x][-1][2])
                                        
                                            cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x][-1][1][2]+"']"),eval("['-',['"+e[6][x][-1][1][2]+"'],['1']]"))
                                        
                                            stmt = copy.deepcopy(e[6][x][-1][1][4])
                                        
                                        
                                            stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x][-1][4])+"']"),prv_value)
                                        
                                        
                                            prv_value = copy.deepcopy(stmt)
                                    
                                            prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x][-1][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x][-1][4])+"'],['1']]"))
                                    
                                            soln_start+=",['ite',"+str(cond)+","+str(stmt)
                                    
                                            soln_end+="]"

                                        else:
                                        
                                            return None,None

                        
                            else:
                            
                                else_value = e[6][x][-1][1][4]
                                
                    if prv_value is not None:
                        else_value = fun_utiles.expr_replace(else_value,eval("['"+'_CV'+str(len(list_sort)+1)+"']"),prv_value)
                    
                        #print str(soln_start)+","+str(else_value)+soln_end+"]"
                    
                        soln = eval(str(soln_start)+","+str(else_value)+soln_end+"]")
                    
                    
                    
                        if soln is not None:
                            if equations_map[e[0]] in list_equations:
                                list_equations.remove(equations_map[e[0]])
            
                            if basecase_map[equation_base] in list_equations:
                                list_equations.remove(basecase_map[equation_base])

                
                            del basecase_map[equation_base]
        
                            del equations_map[e[0]]
        
                            for x in equations_map:
                                e = equations_map[x]
                                e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                            for x in basecase_map:
                                e = basecase_map[x]
                                e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                        
                            status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                        
                        
                            if 'Counter Example' in status:
            
                                map_counter_CE={}
            
                                map_counter_CS={}
            
                                values = status[status.index('[')+1:len(status)-1-status[::-1].index(']')].split(',')
            
                                for x in values:
                                
                                    y = x.split('=')
                                
                                    key = y[0].replace('\n','')
                                
                                    key = key.strip()
                                
                                    value = y[1].replace('\n','')
                                
                                    value = value.strip()
                                
                                    if '_CE' in key and fun_utiles.is_number(value):
                                    
                                        map_counter_CE[key]= value
                                    
                                    elif '_CS' in key and  fun_utiles.is_number(value):
                                    
                                        map_counter_CS[key]= value

                        
                        
                            for x in map_counter_CE:
                                soln[4] = fun_utiles.expr_replace(soln[4],eval("['"+x+"']"),eval("['"+map_counter_CE[x]+"']"))

                            return soln,None
                    
                        else:
                        
                            return None,None
                    
                    else:
                        return None,None
            else:
                
                none_cond = constructNoneCondition(e)
                
                soln=None
                
                local_count=1
                
                list_con_expression = new_e[6].keys()
                                
                perm= permutations(list_con_expression,len(list_con_expression))
                
                for x in list(perm):
                    
                    count = 0
                    
                    soln_first=None
                    
                    soln_start=None
            
                    soln_end=None
            
                    prv_value=None
                    
                    prv_count=None
                    
                    local_count=local_count+1
                    
                
                    for i in range(0,len(x)):
                        
                        
                        
                        if soln_start is None:
                            
                            
                            if e[6][x[i]][0] is not None:
                                
                                cond = copy.deepcopy(e[6][x[i]][0])
                                
                            else:
                                
                                cond = copy.deepcopy(none_cond)
                                

                            cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+e[6][x[i]][3][1][2]+"'],['1']]"))
                            
                            
                            soln_first = "['i2','0','"+e[6][x[i]][3][1][2]+"',"+str(e[6][x[i]][3][1][3])
                            
                                    
                            stmt = copy.deepcopy(e[6][x[i]][3][1][4])
                                                    
                            
                            if additional_axoims is None:
                                
                                additional_axoims = []
                            
                            
                            if e[6][x[i]][0] is None:
                                
                                #print "['and',['<=',['0'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"
                                
                                constraint1 = eval("['s1',['implies',"+"['and',['<=',['0'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"+","+str(cond)+"]]")
                                
                                constraint2 = fun_utiles.expr_complement(copy.deepcopy(cond))
                                
                                constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['"+'_CE'+str(e[6][x[i]][-1][-1])+"']"))
                                
                                constraint2 = eval("['s0',"+str(constraint2)+"]")
                            
                                constraint3 = eval("['a',['<=',['0'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")
                                
                                
                                constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                                constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                                constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                
                                
                                
                                additional_axoims.append(constraint1)
                                
                                additional_axoims.append(constraint2)
                                
                                additional_axoims.append(constraint3)
                                

                                
                                stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),e_base[3])
                                
                                stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                
                                prv_value = copy.deepcopy(stmt)
                                
                                prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][-1][-1])+"'],['1']]"))
                                
                                prv_count = e[6][x[i]][-1][-1]
                                
                            
                            else:
                                
                                
                                constraint1 = copy.deepcopy(e[6][x[i]][3][5])
                                
                                constraint2 = copy.deepcopy(e[6][x[i]][3][6])
                                
                                constraint3 = copy.deepcopy(e[6][x[i]][3][7])
                                
                                constraint4 = copy.deepcopy(e[6][x[i]][3][9])
                                
                                
                                
                                constraint1 = fun_utiles.expr_replace(constraint1,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                                constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                                constraint3 = fun_utiles.expr_replace(constraint3,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                                constraint4 = fun_utiles.expr_replace(constraint4,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                                
                                constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                                constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                                constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                                constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                                constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                                constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                       
                       
                                                                    
                                additional_axoims.append(constraint1)
                                
                                additional_axoims.append(constraint2)
                                
                                additional_axoims.append(constraint3)

                                additional_axoims.append(constraint4)
                                
                                

                                    
                                                            
                                stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),e_base[3])
                                
                                stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                                
                                prv_value = copy.deepcopy(stmt)
                                
                                prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][3][4])+"'],['1']]"))
                                
                                prv_count = e[6][x[i]][3][4]
                                
                            
                            soln_start="['ite',"+str(cond)+","+str(stmt)
                            
                            soln_end="]"
                            
                        else:
                            
                            if prv_value is not None:
                                
                                if e[6][x[i]][0] is not None:
                                
                                    cond = copy.deepcopy(e[6][x[i]][0])
                                
                                else:
                                
                                    cond = copy.deepcopy(none_cond)
                                    
                                    
                                cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+e[6][x[i]][3][1][2]+"'],['1']]"))
                                    
                                stmt = copy.deepcopy(e[6][x[i]][3][1][4])
                            
                                if e[6][x[i]][0] is None:
                                    
                                    
                                    constraint1 = eval("['s1',['implies',"+"['and',['<=',['_CE"+str(prv_count)+"'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"+","+str(cond)+"]]")
                                
                                    constraint2 = fun_utiles.expr_complement(copy.deepcopy(cond))
                                    
                                                                   
                                    constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['"+'_CE'+str(e[6][x[i]][-1][-1])+"']"))
                                    
                                     
                                    constraint2 = eval("['s0',"+str(constraint2)+"]")
                                
                                    constraint3 = eval("['a',['<=',['0'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")

                                    constraint4 = eval("['a',['<=',['"+str(prv_count)+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")
                                    
                                    
                                    
                                    constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                                    constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                                    constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                       
                                    constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                       
                                    constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    
                                    additional_axoims.append(constraint1)
                                
                                    additional_axoims.append(constraint2)
                                
                                    additional_axoims.append(constraint3)

                                    additional_axoims.append(constraint4)
                                    
                                    


                                    
                                    
                                    stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),prv_value)
                                    
                                
                                    prv_value = copy.deepcopy(stmt)
                                    
                                    
                                    stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                                    prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(len(x))+"'],['1']]"))
                                    
                                    prv_count = e[6][x[i]][-1][-1]
                            
                                else:
                                    
                        
                                    constraint1 = copy.deepcopy(e[6][x[i]][3][5])
                                
                                    constraint2 = copy.deepcopy(e[6][x[i]][3][6])
                                
                                    constraint3 = copy.deepcopy(e[6][x[i]][3][7])
                                
                                    constraint4 = copy.deepcopy(e[6][x[i]][3][9])

                                    

                                    constraint1 = fun_utiles.expr_replace(constraint1,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                                    constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                                    constraint3 = fun_utiles.expr_replace(constraint3,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                                    constraint4 = fun_utiles.expr_replace(constraint4,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                                                    
                    
                                    
                                    
                                    
                                    
                                    constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                          
                                    constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))
                                  
                                    constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                                    constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                                    constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                    
                                    constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    
                                    
                                    
                                    additional_axoims.append(constraint1)
                                
                                    additional_axoims.append(constraint2)
                                
                                    additional_axoims.append(constraint3)

                                    additional_axoims.append(constraint4)
                                    

                                    
                                                            
                                    stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),prv_value)
                                    
                                    prv_value = copy.deepcopy(stmt)
                                    
                                    stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                                    prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][3][4])+"'],['1']]"))
                                
                                    prv_count = e[6][x[i]][3][4]
                            
                                if i==len(x)-1:
                                    
                                    soln_start+=","+str(stmt)

                                else:
                                    
                                    soln_start+=",['ite',"+str(cond)+","+str(stmt)
                            
                                    soln_end+="]"

                    if soln is None:
                        
                        soln = soln_start+soln_end
                        
                    else:
                        soln="['or',"+soln+","+soln_start+soln_end+"]"
                
                soln = soln_first+","+soln+"]"
                
                soln = eval(soln)
                
                if equations_map[e[0]] in list_equations:
                    
                    list_equations.remove(equations_map[e[0]])
            
                if basecase_map[equation_base] in list_equations:
                                
                    list_equations.remove(basecase_map[equation_base])

                
                del basecase_map[equation_base]
        
                del equations_map[e[0]]
        
                for x in equations_map:
                    e = equations_map[x]
                    e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                for x in basecase_map:
                    e = basecase_map[x]
                    e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])
                                                
                return soln,additional_axoims
    else:
        return None,None




def constructNoneCondition(e):
    
    condition=None
    list_seq=None
    
    if len(e[6])>1:
        
        for x in e[6]:
            if e[6][x][0] is not None:
                
                if condition is None:
                    list_seq =[]
                    condition = str(e[6][x][0])
                    list_seq.append(e[6][x][3][4])
            
                else:
            
                    condition = "['and',"+condition+","+str(e[6][x][0])+"]"
    else:
        for x in e[6]:
            if e[6][x][0] is not None:
                list_seq =[]
                list_seq.append(e[6][x][3][4])
                return e[6][x][0],list_seq

    condition= eval("['!',"+condition+"]")
    
    if condition is not None:
        
        return condition,list_seq
    
    else:
        
        return None,None
        
        
        
def solveFunctionMontonic(new_e, e, equations_map, basecase_map, list_equations):
    

    #new_e = constructInfoSystem(e, equations_map, basecase_map, list_equations)
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    additional_axoims=None
    
    type_in = None
    
    type_in_in=None
        
    if  new_e is not None:
        
        none_cond=None
                
        soln=None
                
        local_count=1
                
        list_con_expression = new_e[6].keys()
        
        for x in new_e[6]:
            
            #print new_e[6][x][2]
            
            #print new_e[6][x][3][1][4]
            
            #print new_e[6][x][3][3]
            
            #print '~~~~~~~~~~~~~~~~~~~~~~~'
            #print new_e[6][x][3]
            #print '-----------------------'
            #print new_e[6][x][3][3]
            #print '~~~~~~~~~~~~~~~~~~~~~~~'

            
            
            if type_in is None:
                            
                if new_e[6][x][3][3] is None:
                    
                    type_in_in = getTypeEquation(new_e[6][x][3][1])
                                                            
                    if type_in_in is not None:
                        
                        if type_in is None:
                            
                            type_in = type_in_in
                        
                        elif type_in_in == 'Constant':
                            
                            type_in = type_in
                            
                        elif type_in!='undefined' and  type_in != type_in_in:
                            
                            type_in='undefined'
                
                else:
                    if type_in!='undefined':
                        
                        type_in = new_e[6][x][3][3]
                    
                
            else:
                
                if new_e[6][x][3][3] is None:
                    
                    type_in_in = getTypeEquation(new_e[6][x][3][1])
                                                            
                    if type_in_in is not None:
                        
                        if type_in is None:
                            
                            type_in = type_in_in
                        
                        elif type_in_in == 'Constant':
                            
                            type_in = type_in
                            
                        elif type_in!='undefined' and  type_in != type_in_in:
                            
                            type_in='undefined'
                else:
                    if type_in!='undefined':
                        
                        type_in = new_e[6][x][3][3]

            
        list_seq=None
        
        #print '################3'
        
        #print type_in
        
        #print type_in_in
        
        #print '################3'
        
        if type_in =='undefined':
            
            if type_in=='undefined' and type_in_in=='constant':
                
                if len(new_e[6])==2:
                    
                    soln,additional_axoims = getFunction2Constant(new_e, e, equations_map, basecase_map, list_equations)
                    
                    if soln is not None:
                        
                        return soln,additional_axoims
                    
                    else:
                        
                        return None,None
                    
            elif type_in=='undefined' and (type_in_in=='increasing' or type_in_in=='decreasing') :
                
                if len(new_e[6])==2:
                
                    #soln,additional_axoims = getFunctionCycle(new_e, e, equations_map, basecase_map, list_equations)
                    soln,additional_axoims = getFunction2ConstantRev(new_e, e, equations_map, basecase_map, list_equations)
                    
                    if soln is not None:
                        
                        return soln,additional_axoims
                    
                    
                    return None,None
            else:
                
                return None,None
                
        elif (type_in=='increasing' or type_in=='decreasing') and type_in_in=='constant':
            
            
            if len(new_e[6])==2:
                    
                soln,additional_axoims = getFunction2Constant(new_e, e, equations_map, basecase_map, list_equations)
                    
                if soln is not None:
                        
                    return soln,additional_axoims
                    
                else:
                        
                    return None,None

        
        
        elif (type_in=='increasing' and type_in_in=='decreasing') or (type_in=='decreasing' and type_in_in=='increasing'):
                
            if len(new_e[6])==2:
                
                soln,additional_axoims = getFunctionCycle(new_e, e, equations_map, basecase_map, list_equations)
                                    
                if soln is not None:
                        
                    return soln,additional_axoims
                    
                return None,None

            else:
                
                return None,None
        
        elif type_in_in!='Constant':
        
            none_cond,list_seq = constructNoneCondition(new_e)
            
        
        soln=None
                
        local_count=1
                
        list_con_expression = new_e[6].keys()
        
        if none_cond is None:
            
            list_con_expression.remove(None)
                                
        
        print none_cond
        
        print list_con_expression
        
        perm= permutations(list_con_expression,len(list_con_expression))
        
        for x in list(perm):
                    
            count = 0
                    
            soln_first=None
                    
            soln_start=None
            
            soln_end=None
            
            prv_value=None
                    
            prv_count=None
                    
            local_count=local_count+1
            

                
            for i in range(0,len(x)):
                
                        
                if soln_start is None:
                                                
                            
                    if e[6][x[i]][0] is not None:
                                
                        cond = copy.deepcopy(e[6][x[i]][0])
                                
                    else:
                                
                        cond = copy.deepcopy(none_cond)
                                

                    cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+e[6][x[i]][3][1][2]+"'],['1']]"))
                            
                            
                    soln_first = "['i2','0','"+e[6][x[i]][3][1][2]+"',"+str(e[6][x[i]][3][1][3])
                            
                                    
                    stmt = copy.deepcopy(e[6][x[i]][3][1][4])
                                                    
                            
                    if additional_axoims is None:
                                
                        additional_axoims = []
                            
                            
                    if e[6][x[i]][0] is None:
                                
                        #print "['and',['<=',['0'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"
                                
                        cond = fun_utiles.expr_replace(cond,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),e_base[3])
                        
                        if list_seq is not None:
                            
                           for z in  list_seq:
                               
                                cond = fun_utiles.expr_replace(cond ,eval("['"+'_CV'+str(z)+"']"),e_base[3])
                        
                        
                        constraint1 = eval("['s1',['implies',"+"['and',['<=',['0'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"+","+str(cond)+"]]")
                                
                        constraint2 = fun_utiles.expr_complement(copy.deepcopy(cond))
                                
                        constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['"+'_CE'+str(e[6][x[i]][-1][-1])+"']"))
                                
                        constraint2 = eval("['s0',"+str(constraint2)+"]")
                            
                        constraint3 = eval("['a',['<=',['0'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")
                                
                                
                        constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                        constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                        constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                
                                
                                
                        additional_axoims.append(constraint1)
                                
                        additional_axoims.append(constraint2)
                                
                        additional_axoims.append(constraint3)
                                
                        
                                
                        stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),e_base[3])
                        
                                                    
                        stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                
                        prv_value = copy.deepcopy(stmt)
                                
                        prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][-1][-1])+"'],['1']]"))
                                
                        prv_count = e[6][x[i]][-1][-1]
                                
                            
                    else:
                                
                                
                        
                        cond = fun_utiles.expr_replace(cond,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),e_base[3])
                        
                        if list_seq is not None:
                            
                           for z in  list_seq:
                               
                                cond = fun_utiles.expr_replace(cond,eval("['"+'_CV'+str(z)+"']"),e_base[3])

                                
                        cond = fun_utiles.expr_replace(cond,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))


                        
                        constraint1 = copy.deepcopy(e[6][x[i]][3][5])
                                
                        constraint2 = copy.deepcopy(e[6][x[i]][3][6])
                                
                        constraint3 = copy.deepcopy(e[6][x[i]][3][7])
                                
                        constraint4 = copy.deepcopy(e[6][x[i]][3][9])
                                
                                
                                
                        constraint1 = fun_utiles.expr_replace(constraint1,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                        constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                        constraint3 = fun_utiles.expr_replace(constraint3,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                        constraint4 = fun_utiles.expr_replace(constraint4,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['0']"))
                                
                                
                        constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                        constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                        constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                        constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                        constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                        constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                       
                        if list_seq is not None:
                            
                            for z in  list_seq:
                               
                                constraint1[-1] = fun_utiles.expr_replace(constraint1[-1] ,eval("['"+'_CV'+str(z)+"']"),e_base[3])
                                
                                constraint2[-1] = fun_utiles.expr_replace(constraint2[-1] ,eval("['"+'_CV'+str(z)+"']"),e_base[3])

                       
                       
                       
                                                                    
                        additional_axoims.append(constraint1)
                                
                        additional_axoims.append(constraint2)
                                
                        additional_axoims.append(constraint3)

                        additional_axoims.append(constraint4)
                                
                                                            
                        stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),e_base[3])
                                
                        stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                                
                        prv_value = copy.deepcopy(stmt)
                                
                        prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][3][4])+"'],['1']]"))
                                
                        prv_count = e[6][x[i]][3][4]
                                
                            
                    soln_start="['ite',"+str(cond)+","+str(stmt)
                            
                    soln_end="]"
                            
                else:
                            
                    if prv_value is not None:
                                
                        if e[6][x[i]][0] is not None:
                                
                            cond = copy.deepcopy(e[6][x[i]][0])
                                
                        else:
                                
                            cond = copy.deepcopy(none_cond)
                                    
                                    
                        cond = fun_utiles.expr_replace(cond,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+e[6][x[i]][3][1][2]+"'],['1']]"))
                        
                        
                                    
                        stmt = copy.deepcopy(e[6][x[i]][3][1][4])
                            
                        if e[6][x[i]][0] is None:
                            
                            
                            
                            cond = fun_utiles.expr_replace(cond,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),prv_value)
                            
                            
                            if list_seq is not None:
                            
                                for z in  list_seq:
                               
                                    cond = fun_utiles.expr_replace(cond ,eval("['"+'_CV'+str(z)+"']"),prv_value)

                                    
                                    
                            cond = fun_utiles.expr_replace(cond,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))
                                                           
                                                                                               
                            constraint1 = eval("['s1',['implies',"+"['and',['<=',['_CE"+str(prv_count)+"'],['"+e[6][x[i]][3][1][2]+"']],['<',['"+e[6][x[i]][3][1][2]+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]"+","+str(cond)+"]]")
                                
                            constraint2 = fun_utiles.expr_complement(copy.deepcopy(cond))
                                    
                                                                   
                            constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['"+'_CE'+str(e[6][x[i]][-1][-1])+"']"))
                                    
                                     
                            constraint2 = eval("['s0',"+str(constraint2)+"]")
                                
                            constraint3 = eval("['a',['<=',['0'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")

                            constraint4 = eval("['a',['<=',['"+str(prv_count)+"'],['_CE"+str(e[6][x[i]][-1][-1])+"']]]")
                                    
                                    
                                    
                            constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                            constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                            constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                                                                      
                            constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                       
                            constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][-1][-1])+"']"),eval("['_CE"+str(e[6][x[i]][-1][-1])+"_"+str(local_count)+"']"))
                       
                            constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    
                            additional_axoims.append(constraint1)
                                
                            additional_axoims.append(constraint2)
                                
                            additional_axoims.append(constraint3)

                            additional_axoims.append(constraint4)
                                    
                                    


                                    
                                    
                            stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][-1][-1])+"']"),prv_value)
                                    
                                
                            prv_value = copy.deepcopy(stmt)
                                    
                                    
                            stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                            prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(len(x))+"'],['1']]"))
                                    
                            prv_count = e[6][x[i]][-1][-1]
                            
                        else:
                            
                            
                            cond = fun_utiles.expr_replace(cond,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),prv_value)
                            
                            if list_seq is not None:
                            
                                for z in  list_seq:
                               
                                    cond = fun_utiles.expr_replace(cond ,eval("['"+'_CV'+str(z)+"']"),prv_value)
                                    
                                    
                            cond = fun_utiles.expr_replace(cond,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    
                        
                            constraint1 = copy.deepcopy(e[6][x[i]][3][5])
                                
                            constraint2 = copy.deepcopy(e[6][x[i]][3][6])
                                
                            constraint3 = copy.deepcopy(e[6][x[i]][3][7])
                                
                            constraint4 = copy.deepcopy(e[6][x[i]][3][9])

                                    

                            constraint1 = fun_utiles.expr_replace(constraint1,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                            constraint2 = fun_utiles.expr_replace(constraint2,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                            constraint3 = fun_utiles.expr_replace(constraint3,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                
                            constraint4 = fun_utiles.expr_replace(constraint4,eval("['"+'_CS'+str(e[6][x[i]][3][4])+"']"),eval("['"+'_CE'+str(prv_count)+"']"))
                                                                    
                    
                                    
                                    
                                    
                                    
                            constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                          
                            constraint1 = fun_utiles.expr_replace(constraint1,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))
                                  
                            constraint2 = fun_utiles.expr_replace(constraint2,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                                                      
                            constraint3 = fun_utiles.expr_replace(constraint3,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                       
                            constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(e[6][x[i]][3][4])+"']"),eval("['_CE"+str(e[6][x[i]][3][4])+"_"+str(local_count)+"']"))
                                    
                            constraint4 = fun_utiles.expr_replace(constraint4,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                    
                            if list_seq is not None:
                            
                                for z in  list_seq:
                               
                                    constraint1[-1] = fun_utiles.expr_replace(constraint1[-1] ,eval("['"+'_CV'+str(z)+"']"),prv_value)
                                
                                    constraint2[-1] = fun_utiles.expr_replace(constraint2[-1] ,eval("['"+'_CV'+str(z)+"']"),prv_value)

                                    
                                    
                            additional_axoims.append(constraint1)
                                
                            additional_axoims.append(constraint2)
                                
                            additional_axoims.append(constraint3)

                            additional_axoims.append(constraint4)
                                    

                                                            
                            stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x[i]][3][4])+"']"),prv_value)
                                    
                            prv_value = copy.deepcopy(stmt)
                                    
                            stmt = fun_utiles.expr_replace(stmt,eval("['_CE"+str(prv_count)+"']"),eval("['_CE"+str(prv_count)+"_"+str(local_count)+"']"))

                                
                            prv_value = fun_utiles.expr_replace(prv_value,eval("['"+e[6][x[i]][3][1][2]+"']"),eval("['-',['"+'_CE'+str(e[6][x[i]][3][4])+"'],['1']]"))
                                
                            prv_count = e[6][x[i]][3][4]
                            
                        if i==len(x)-1:
                                    
                            soln_start+=","+str(stmt)

                        else:
                                    
                            soln_start+=",['ite',"+str(cond)+","+str(stmt)
                            
                            soln_end+="]"

            if soln is None:
                        
                soln = soln_start+soln_end
                        
            else:
                    
                soln="['or',"+soln+","+soln_start+soln_end+"]"
                
        soln = soln_first+","+soln+"]"
                
        soln = eval(soln)
                
        if equations_map[e[0]] in list_equations:
                    
            list_equations.remove(equations_map[e[0]])
            
        if basecase_map[equation_base] in list_equations:
                                
            list_equations.remove(basecase_map[equation_base])

                
        del basecase_map[equation_base]
        
        del equations_map[e[0]]
        
        for x in equations_map:
            e = equations_map[x]
            e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
        for x in basecase_map:
            e = basecase_map[x]
            e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])
                                                

        return soln,additional_axoims





def getFunctionCycle(new_e, e, equations_map, basecase_map, list_equations):

    soln=None
    
    additional_axoms=None
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    equation1 = None
    
    equation2 = None
    
    equation_left1 = None
    
    equation_left2 = None
    
    CE_count=None

    
    for x in new_e[6]:
        
        if new_e[6][x][0] is not None:
            
            if equation1 is None:
                
                equation1 = new_e[6][x][1]
                
                equation_left1 = new_e[6][x][3][1][-2]
                
            CE_count='_CE'+str(new_e[6][x][3][4])
                
            new_e[6][x][3][1][-1] = fun_utiles.expr_replace(new_e[6][x][3][1][-1],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
                        
            elseValue= copy.deepcopy(new_e[6][x][3][1][-1])
            
            elseValue = fun_utiles.expr_replace(elseValue,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['"+'_CE'+str(new_e[6][x][3][4])+"']"))
            
            new_e[6][x][3][5] = fun_utiles.expr_replace(new_e[6][x][3][5],eval("['"+'_CS'+str(new_e[6][x][3][4])+"']"),eval("['0']"))
            
            new_e[6][x][3][5] = fun_utiles.expr_replace(new_e[6][x][3][5],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            new_e[6][x][3][6] = fun_utiles.expr_replace(new_e[6][x][3][6],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])

                
            cond = fun_utiles.expr_replace(new_e[6][x][0],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])

            if soln is None:
                
                equation_list = []
                
                constraint_list =[]
                
                temp_cond = eval("['a',"+str(cond)+"]")
                
                equation_list.append(temp_cond)
                
                constraint_list.append(FOL_translation.wff2z3_update(temp_cond))
                
                var_map={}
                
                FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                vfacts=[]
                
                for vfact in var_map:
                    vfacts.append(var_map[vfact])

                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')

                if 'Counter Example' in status:
       
                    if equations_map[e[0]] in list_equations:
                    
                        list_equations.remove(equations_map[e[0]])
            
                    if basecase_map[equation_base] in list_equations:
                    
                        list_equations.remove(basecase_map[equation_base])

                    del basecase_map[equation_base]
                
                    del equations_map[e[0]]
        
                    for x in equations_map:
                        e = equations_map[x]
                        e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                    for x in basecase_map:
                        e = basecase_map[x]
                        e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                    
                    return new_e[6][x][3][1], None
                
                else:
                    
                    additional_axoms=[]
                
                    additional_axoms.append(new_e[6][x][3][5])
                
                    additional_axoms.append(new_e[6][x][3][6])
                
                    additional_axoms.append(new_e[6][x][3][7])

            
                    soln="['"+new_e[6][x][3][1][0]+"','"+new_e[6][x][3][1][1]+"','"+new_e[6][x][3][1][2]+"',"+str(new_e[6][x][3][1][3])+",['ite',"+str(cond)+","+str(new_e[6][x][3][1][-1])+",Black]]"
        else:
            
            if equation2 is None:
                
                equation2 = new_e[6][x][1]
                
                equation_left2 = new_e[6][x][3][1][-2]

        
    if equation1 is not None and equation2 is not None:
                
        equation_left1= simplify(FOL_translation.expr2string1(equation_left1))
        
        coeff_expr1 = simplify(FOL_translation.expr2string1(equation1))
                
        term1 = simplify(equation_left1)
                    
        coeff_const1 = coeff_expr1.coeff(term1)
                    
        if str(coeff_const1)=='1':
                
            result1 = coeff_expr1 - coeff_const1*simplify(equation_left1)
            
            
        equation_left2= simplify(FOL_translation.expr2string1(equation_left2))
        
        coeff_expr2 = simplify(FOL_translation.expr2string1(equation2))
                
        term2 = simplify(equation_left2)
                    
        coeff_const2 = coeff_expr1.coeff(term2)
                    
        if str(coeff_const2)=='1':
                
            result2 = coeff_expr2 - coeff_const2*simplify(equation_left2)
            
            
        factor=result1/result2
        

        
        if factor.is_positive==False and CE_count is not None:
            
            factor=-1*factor
            
            if factor==1:
                                
                
                if result2.is_positive==False:
                    print "1"
                    print result1
                    print result2
                    soln = soln.replace('Black',"['ite',['==',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['0']]"+",['"+str(factor+1)+"']],['0']],['-',"+str(elseValue)+",['"+str(result1)+"']],"+str(elseValue)+"]")
                    soln = eval(soln)
                    
                else:
                    print "2"
                    print result1
                    print result2
                    soln = soln.replace('Black',"['ite',['==',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['0']]"+",['"+str(factor+1)+"']],['0']],['+',"+str(elseValue)+",['"+str(result2)+"']],"+str(elseValue)+"]")
                    soln = eval(soln)

                
                
            elif factor<1:
                

                factor=-1*(result2/result1)
                
                
                if result2.is_positive==False:
                    
                    
                    soln = soln.replace('Black',"['ite',['==',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['0']]"+",['"+str(factor+1)+"']],['0']],['-',"+str(elseValue)+",['"+str(-1*result2)+"']],['+',['-',"+str(elseValue)+",['"+str(-1*result2)+"']],"+"['*',"+"['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']]"+",['"+str(factor+1)+"']]"+",['"+str(result1)+"']]"+"]"+"]")
                    soln = eval(soln)
                    
                    
                else:
                    

                    soln = soln.replace('Black',"['ite',['==',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['0']]"+",['"+str(factor+1)+"']],['0']],['+',"+str(elseValue)+",['"+str(result2)+"']],['-',['+',"+str(elseValue)+",['"+str(result2)+"']],"+"['*',"+"['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']]"+",['"+str(factor+1)+"']]"+",['"+str(-1*result1)+"']]"+"]"+"]")
                    soln = eval(soln)

                
            else:
                
                if result2.is_positive==False:

                    soln = soln.replace('Black',"['ite',['!=',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']],['0']],['-',"+str(elseValue)+","+"['*',"+"['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']]"+",['"+str(-1*result2)+"']]"+"],"+str(elseValue)+"]")
                    soln = eval(soln)
                    
                else:
                    
                    soln = soln.replace('Black',"['ite',['!=',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']],['0']],['+',"+str(elseValue)+","+"['*',"+"['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']]"+",['"+str(result2)+"']]"+"],"+str(elseValue)+"]")
                    soln = eval(soln)
            
            
            if soln is not None:
                

                
                if equations_map[e[0]] in list_equations:
                    
                    list_equations.remove(equations_map[e[0]])
            
                if basecase_map[equation_base] in list_equations:
                                
                    list_equations.remove(basecase_map[equation_base])

                
                del basecase_map[equation_base]
        
                del equations_map[e[0]]
        
                for x in equations_map:
                    e = equations_map[x]
                    e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                for x in basecase_map:
                    e = basecase_map[x]
                    e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                return soln,additional_axoms
            
    
    return None,None











def getFunction2Constant(new_e, e, equations_map, basecase_map, list_equations):
    
    soln=None
    
    additional_axoms=None
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]

    for x in new_e[6]:
        
        if new_e[6][x][0] is not None:
            
            
            cond = fun_utiles.expr_replace(new_e[6][x][0],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            cond = fun_utiles.expr_replace(cond,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['-',['"+new_e[6][x][3][1][2]+"'],['1']]"))
            
            
            new_e[6][x][3][1][-1] = fun_utiles.expr_replace(new_e[6][x][3][1][-1],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            elseValue= copy.deepcopy(new_e[6][x][3][1][-1])
            
            elseValue = fun_utiles.expr_replace(elseValue,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['"+'_CE'+str(new_e[6][x][3][4])+"']"))
            
            
            new_e[6][x][3][5] = fun_utiles.expr_replace(new_e[6][x][3][5],eval("['"+'_CS'+str(new_e[6][x][3][4])+"']"),eval("['0']"))
            
            new_e[6][x][3][5] = fun_utiles.expr_replace(new_e[6][x][3][5],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            new_e[6][x][3][6] = fun_utiles.expr_replace(new_e[6][x][3][6],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])


            
            if soln is None:
                
                equation_list = []
                
                constraint_list =[]
                
                temp_cond = eval("['a',"+str(cond)+"]")
                
                equation_list.append(temp_cond)
                
                constraint_list.append(FOL_translation.wff2z3_update(temp_cond))
                
                var_map={}
                
                FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                vfacts=[]
                
                for vfact in var_map:
                    vfacts.append(var_map[vfact])

                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')

                if 'Counter Example' in status:
                    
                    if equations_map[e[0]] in list_equations:
                    
                        list_equations.remove(equations_map[e[0]])
            
                    if basecase_map[equation_base] in list_equations:
                    
                        list_equations.remove(basecase_map[equation_base])

                    del basecase_map[equation_base]
                
                    del equations_map[e[0]]
        
                    for x in equations_map:
                        
                        e = equations_map[x]
                        
                        e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                    for x in basecase_map:
                        
                        e = basecase_map[x]
                        
                        e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                    
                    return new_e[6][x][3][1], None
                
                else:
                
                    soln=eval("['"+new_e[6][x][3][1][0]+"','"+new_e[6][x][3][1][1]+"','"+new_e[6][x][3][1][2]+"',"+str(new_e[6][x][3][1][3])+",['ite',"+str(cond)+","+str(new_e[6][x][3][1][-1])+","+str(elseValue)+"]]")
                
                    additional_axoms=[]
                
                    additional_axoms.append(new_e[6][x][3][5])
                
                    additional_axoms.append(new_e[6][x][3][6])
                
                    additional_axoms.append(new_e[6][x][3][7])
                
                    if equations_map[e[0]] in list_equations:
                    
                        list_equations.remove(equations_map[e[0]])
            
                    if basecase_map[equation_base] in list_equations:
                    
                        list_equations.remove(basecase_map[equation_base])

                    del basecase_map[equation_base]
                
                    del equations_map[e[0]]
        
                    for x in equations_map:
                        e = equations_map[x]
                        e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                    for x in basecase_map:
                        e = basecase_map[x]
                        e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])
                                            
                    return soln,additional_axoms
            
    return soln,additional_axoms
                






def getFunction2ConstantRev(new_e, e, equations_map, basecase_map, list_equations):
    
    soln=None
    
    additional_axoms=None
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    value_else=None
    
    counter_else=None
    
    if new_e[6][None][0] is None:
        
        counter_else = new_e[6][None][3][-1]
        
        value_else = new_e[6][None][3][1][-1]
        

    for x in new_e[6]:
        
        if new_e[6][x][0] is not None:
            
            
            cond_else = copy.deepcopy(new_e[6][x][0])
            
            value_else = fun_utiles.expr_replace(value_else,eval("['"+'_CV'+str(counter_else)+"']"),e_base[3])
            
            cond_else = fun_utiles.expr_replace(cond_else,eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),value_else)
            
            cond_else = fun_utiles.expr_replace(cond_else,eval("['"+'_CV'+str(counter_else)+"']"),e_base[3])
            
            cond = fun_utiles.expr_replace(new_e[6][x][0],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            
            if soln is None:
                
                equation_list = []
                
                constraint_list =[]
                
                temp_cond = eval("['a',"+str(cond)+"]")
                
                equation_list.append(temp_cond)
                
                constraint_list.append(FOL_translation.wff2z3_update(temp_cond))
                
                var_map={}
                
                FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                vfacts=[]
                
                for vfact in var_map:
                    vfacts.append(var_map[vfact])

                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                

                if 'Counter Example' in status:
                    
                    if equations_map[e[0]] in list_equations:
                    
                        list_equations.remove(equations_map[e[0]])
            
                    if basecase_map[equation_base] in list_equations:
                    
                        list_equations.remove(basecase_map[equation_base])

                    del basecase_map[equation_base]
                
                    del equations_map[e[0]]
        
                    for x in equations_map:
                        
                        e = equations_map[x]
                        
                        e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                    for x in basecase_map:
                        
                        e = basecase_map[x]
                        
                        e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                    new_e[6][x][3][1][-1] = fun_utiles.expr_replace(new_e[6][x][3][1][-1],eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
                    
                    return new_e[6][x][3][1], None
                
                else:
                    
                    value = copy.deepcopy(value_else)
                    
                    value = fun_utiles.expr_replace(value,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['"+'_CE'+str(new_e[6][x][3][4])+"']"))
                    
                    
                    soln=eval("['"+new_e[6][x][3][1][0]+"','"+new_e[6][x][3][1][1]+"','"+new_e[6][x][3][1][2]+"',"+str(new_e[6][x][3][1][3])+",['ite',"+str(cond_else)+","+str(value_else)+","+str(value)+"]]")
                                       
                    
                    constraint1 = eval("['s1',['implies',['and',['<=',['0'],['"+new_e[6][x][3][1][2]+"']],['<',['"+new_e[6][x][3][1][2]+"'],['"+'_CE'+str(new_e[6][x][3][4])+"']]],"+str(cond_else)+"]]")
                    
                    
                    constraint2 = eval("['s0',"+str(fun_utiles.expr_replace(fun_utiles.expr_complement(copy.deepcopy(cond_else)),eval("['"+new_e[6][x][3][1][2]+"']"),eval("['"+'_CE'+str(new_e[6][x][3][4])+"']")))+"]")
                    
                    constraint3 =eval("['a',['<=',['0'],['"+'_CE'+str(new_e[6][x][3][4])+"']]]")
                    
                    
                    additional_axoms=[]
                
                    additional_axoms.append(constraint1)
                
                    additional_axoms.append(constraint2)
                
                    additional_axoms.append(constraint3)

                    
                    if equations_map[e[0]] in list_equations:
                    
                        list_equations.remove(equations_map[e[0]])
            
                    if basecase_map[equation_base] in list_equations:
                    
                        list_equations.remove(basecase_map[equation_base])

                    del basecase_map[equation_base]
                
                    del equations_map[e[0]]
        
                    for x in equations_map:
                        e = equations_map[x]
                        e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                    for x in basecase_map:
                        e = basecase_map[x]
                        e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])
                        
                                            
                    return soln,additional_axoms
            
    return soln,additional_axoms










def getTypeEquation(e):
    
    
    equation_list=[]
    
    constraint_list=[]

    e_new1 = copy.deepcopy(e[4])
                                
    e_new1_in = copy.deepcopy(e[4])
    
    e_new1_in = fun_utiles.expr_replace(e_new1_in,eval("['"+e[2]+"']"),eval("['-',['"+e[2]+"'],['1']]"))
    
    if e_new1==e_new1_in:
        
        return 'constant'
    
    else:

        constraint_in =  eval("['s0',['<=',"+str(e_new1_in)+","+str(e_new1)+"]]")
        
        equation_list.append(constraint_in)
        
        
        constraint_list.append(FOL_translation.wff2z3_update(constraint_in))

                
        var_map={}
    
        FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
        vfacts=[]
                
        for vfact in var_map:
            vfacts.append(var_map[vfact])

        status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
        

        if 'Counter Example' in status:
                    
            return 'increasing'
            
        else:

            equation_list=[]
            
            constraint_list=[]
                
            constraint_de =  eval("['s0',['>=',"+str(e_new1_in)+","+str(e_new1)+"]]")
            
                    
            equation_list.append(constraint_de)
            
            constraint_list.append(FOL_translation.wff2z3_update(constraint_de))
                
            var_map={}
    
            FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
            vfacts=[]
                
            for vfact in var_map:
                            
                vfacts.append(var_map[vfact])

            status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                    
            if 'Counter Example' in status:
                        
                return 'decreasing'
            
            else:
                return 'Undefined'






def solveFunctionType(e, equations_map, basecase_map, list_equations):

    new_e = constructInfoSystem(e, equations_map, basecase_map, list_equations)
            
    
    if  new_e is not None:
    
        soln = solveForAlways(e, equations_map, basecase_map, list_equations)
    
        if soln is not  None:
        
            return soln,None
        
        else:
            
            soln,axioms = solveFunctionMontonic(new_e, e,equations_map, basecase_map, list_equations)
                        
            if soln is not None:
            
                return soln,axioms
            
            else:
                
                return None,None

            
    else:
        
        return None,None




def solveForAlways(e, equations_map, basecase_map, list_equations):
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
        
    for x in e[6]:
        

        if e[6][x][-1][-1]=='Initial' and e[6][x][-1][-2]=='Always True':
            
            
            e[6][x][-1][1][-1] = fun_utiles.expr_replace(e[6][x][-1][1][-1],eval("['_CS"+str(ConstraintCount)+"']"),e_base[-1])

            
            if equations_map[e[0]] in list_equations:
                list_equations.remove(equations_map[e[0]])
            
            if basecase_map[equation_base] in list_equations:
                list_equations.remove(basecase_map[equation_base])

                
            del basecase_map[equation_base]
        
            del equations_map[e[0]]
        
            for x in equations_map:
                e = equations_map[x]
                e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
            for x in basecase_map:
                e = basecase_map[x]
                e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

            return e[6][x][-1][1]




    
    
def solveBaseCaseType(e, equations_map, basecase_map, list_equations):
    
    base_list=[]
    
    soln=None
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    if e_base is not None:
        list=[]
        list.append(eval("['0']"))
        list.append(e_base[3])
        base_list.append(list)

    for x in e[6]:
        if e[6][x][2]=='Base Case':
            list=[]
            list.append(e[6][x][0][2])
            list.append(e[6][x][1])
            base_list.append(list)
        elif e[6][x][2]==None:
            new_e=eval("['"+e[1][0]+"','"+e[1][1]+"','"+e[1][2]+"',"+str(e[1][3])+","+str(e[6][x][1])+"]")
    
    soln = solve_rec_m(new_e, base_list)
    
    if soln is not None:
        
        if equations_map[e[0]] in list_equations:
            list_equations.remove(equations_map[e[0]])
            
        if basecase_map[equation_base] in list_equations:
            list_equations.remove(basecase_map[equation_base])

                
        del basecase_map[equation_base]
        
        del equations_map[e[0]]
        
        for x in equations_map:
            e = equations_map[x]
            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
        for x in basecase_map:
            e = basecase_map[x]
            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
            
    return soln

    
    


def solveConstantType(e, equations_map, basecase_map, list_equations):
        
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    e_solution=None
    
    e_end=''
    
    close_form=None
    
    for x in e[6]:
        
        new_e=eval("['"+e[1][0]+"','"+e[1][1]+"','"+e[1][2]+"',"+str(e[1][3])+","+str(e[6][x][1])+"]")
        
        sol = solve_rec(new_e,e_base)
        
        if sol is not None:
            
            close_form=sol[3]
            
            if x is not None:
                
                if e_solution is None:
                    
                    e_solution ="['ite',"+str(e[6][x][0])+","+str(sol[4])
                    
                else:
                    
                    e_solution +=",['ite',"+str(e[6][x][0])+","+str(sol[4])
                    
                e_end+=']'
                
            else:
                
                e_end = ","+str(sol[4])+e_end
        else:
            
            return None
        
    if close_form is not None:
                
        soln = eval("['i2','"+e[1][1]+"','"+e[1][2]+"',"+str(close_form)+","+e_solution+e_end+']')
        
        if equations_map[e[0]] in list_equations:
            list_equations.remove(equations_map[e[0]])
            
        if basecase_map[equation_base] in list_equations:
            list_equations.remove(basecase_map[equation_base])

                
        del basecase_map[equation_base]
        
        del equations_map[e[0]]
        
        for x in equations_map:
            e = equations_map[x]
            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
        for x in basecase_map:
            e = basecase_map[x]
            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])

        return  soln
        
    else:
        
        return None




def solvePeriodicType(e, equations_map, basecase_map, list_equations):
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    equation_left = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),simplify(str(e[1][2]))))
    
    e_base = basecase_map[equation_base]
    
    new_expr=copy.deepcopy(e[1][3])
    
    new_expr = fun_utiles.expr_replace(new_expr,eval("['+',"+"['"+e[1][2]+"'],['1']]"),eval("['"+e[1][2]+"']"))
    
    term_list=[]
    
    for x in e[6]:
        if e[6][x][2]=='Periodic':
            
            list=[]
            
            list.append(e[6][x][4])
            
            list.append(e[6][x][3])

            coeff_expr = simplify(FOL_translation.expr2string1(e[6][x][1]))
    
            term = simplify(equation_left)
            
            coeff_const = coeff_expr.coeff(term)
            
            if str(coeff_const)=='1':
                
                result = coeff_expr - coeff_const*simplify(equation_left)
                
                list.append(result)
                
                term_list.append(list)
                
        elif e[6][x][2]==None:
            
            list=[]
            
            coeff_expr = simplify(FOL_translation.expr2string1(e[6][x][1]))
    
            term = simplify(equation_left)
            
            coeff_const = coeff_expr.coeff(term)
            
            if str(coeff_const)=='1':
                
                result = coeff_expr - coeff_const*simplify(equation_left)
                
                list.append(result)
                
                term_list.append(list)

    if len(term_list)==2:
        if term_list[0][0]=='==':
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[0][1]))
            initer_update = utiles_translation.expressionCreator_C(statement_temp)
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[0][2]))
            stmt_update1 = utiles_translation.expressionCreator_C(statement_temp)
            
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[1][0]))
            stmt_update2 = utiles_translation.expressionCreator_C(statement_temp)
            
            stmt_update="['+',['+',"+str(e_base[3])+",['*',"+str(stmt_update1)+",['-',['"+var+"'],['/',['"+var+"'],"+str(initer_update)+"]]]],"+"['*',['/',['"+var+"'],"+str(initer_update)+"],"+str(stmt_update2)+"]]"
            
            
            soln = eval("['i2','"+e[1][1]+"','"+e[1][2]+"',"+str(new_expr)+","+stmt_update+']')
        
            if equations_map[e[0]] in list_equations:
                list_equations.remove(equations_map[e[0]])
            
            if basecase_map[equation_base] in list_equations:
                list_equations.remove(basecase_map[equation_base])

                
            del basecase_map[equation_base]
        
            del equations_map[e[0]]
        
            for x in equations_map:
                e = equations_map[x]
                e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
            for x in basecase_map:
                e = basecase_map[x]
                e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])

            return  soln
            
        else:
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[0][1]))
            initer_update = utiles_translation.expressionCreator_C(statement_temp)
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[0][2]))
            stmt_update1 = utiles_translation.expressionCreator_C(statement_temp)
            
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[1][0]))
            stmt_update2 = utiles_translation.expressionCreator_C(statement_temp)
            
            stmt_update="['+',['+',"+str(e_base[3])+",['*',"+str(stmt_update2)+",['-',['"+var+"'],['/',['"+var+"'],"+str(initer_update)+"]]]],"+"['*',['/',['"+var+"'],"+str(initer_update)+"],"+str(stmt_update1)+"]]"
            
            soln = eval("['i2','"+e[1][1]+"','"+e[1][2]+"',"+str(new_expr)+","+stmt_update+']')
        
            if equations_map[e[0]] in list_equations:
                list_equations.remove(equations_map[e[0]])
            
            if basecase_map[equation_base] in list_equations:
                list_equations.remove(basecase_map[equation_base])

                
            del basecase_map[equation_base]
        
            del equations_map[e[0]]
        
            for x in equations_map:
                e = equations_map[x]
                e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
            for x in basecase_map:
                e = basecase_map[x]
                e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])

            return  soln
    
    return None



#def classificationOfEq(e)



def condition_map_constrt(e1,map_con_expression):
    if e1[0]=='ite':
        arg_list=FOL_translation.expr_args(e1)
        list_expr=[]
        list_expr.append(arg_list[0])
        list_expr.append(arg_list[1])
        map_con_expression[FOL_translation.expr2string1(arg_list[0])]=list_expr
        if arg_list[2][0]=='ite':
            condition_map_constrt(arg_list[2],map_con_expression)
        else:
            list_expr=[]
            list_expr.append(None)
            list_expr.append(arg_list[2])
            map_con_expression[None]=list_expr
        





"""

Is eligible for mutual recurrences

"""

def isMutualRecurGroup(e_m1,e_m2):
    for x in e_m1.keys():
        if x is not None:
            if x not in e_m2.keys() or e_m1[x]!=e_m2[x]:
                return None
    return e_m2



"""
Recurrences Solving Module
#Add by Pritom Rajkhowa
#June 8

Test cases

Test Case 1

#e1=['i1', 2, '_n1', ['a3', ['+', ['_n1'], ['1']]], ['+', ['a3', ['_n1']], ['1']]]
#e2=['i0', 0, ['a3', ['0']], ['0']]

Test Case 2

#e1=['i1', 2, '_n1', ['a3', ['+', ['_n1'], ['1']]], ['*', ['a3', ['_n1']], ['+', ['_n1'], ['1']]]]
#e2=['i0', 0, ['a3', ['0']], ['1']]

Test Case 3

#e1=['i1', 2, '_n1', ['t3', ['+', ['_n1'], ['1']]], ['+', ['t3', ['_n1']], ['2']]]
#e2=['i0', 0, ['a3', ['0']], ['1']]

Test Case 4

#e1=['i1', 2, '_n1', ['a3', ['+', ['_n1'], ['1']]], ['*', ['a3', ['_n1']], ['2']]]
#e2=['i0', 0, ['a3', ['0']], ['1']]

"""
def solve_rec(e1,e2):
        global fun_call_map
	lefthandstmt=None
	righthandstmt=None
	righthandstmt_d=None
	lefthandstmt_base=None
	righthandstmt_base=None
	righthandstmt_base_d=None
	variable=None
	closed_form_soln=None
	if e1[0]=='i1':
		lefthandstmt=FOL_translation.expr2string1(e1[3])
		righthandstmt=FOL_translation.expr2string1(e1[4])
		lefthandstmt=lefthandstmt.strip()
		righthandstmt=righthandstmt.strip()
		variable=e1[2]
		if lefthandstmt.find('_PROVE')>0:
			return None
		elif lefthandstmt.find('_ASSUME')>0:
        		return None
		if 'ite' not in righthandstmt and '>' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '|' not in righthandstmt and '&' not in righthandstmt: 
		    	lefthandstmt=simplify(lefthandstmt)
		    	righthandstmt=simplify(righthandstmt)
		    	variable=simplify(variable)
		else:
			if '|' not in righthandstmt and '&' not in righthandstmt and '<<' not in righthandstmt and '>>' not in righthandstmt:
                            righthandstmt=FOL_translation.expr2stringSimplify(e1[4])
			righthandstmt=righthandstmt.strip()
			if 'ite' not in righthandstmt and '>' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '|' not in righthandstmt and '&' not in righthandstmt: 
				lefthandstmt=simplify(lefthandstmt)
				righthandstmt=simplify(righthandstmt)
		    		variable=simplify(variable)
			else:
				lefthandstmt=None
				righthandstmt=None
				variable=None
	if e2[0]=='i0':
		lefthandstmt_base=FOL_translation.expr2string1(e2[2])
		righthandstmt_base=FOL_translation.expr2string1(e2[3])
		variable_list=[]
		fun_utiles.expr2varlist(e2[3],variable_list)
		lefthandstmt_base=lefthandstmt_base.strip()
		righthandstmt_base=righthandstmt_base.strip()
		if 'ite' in righthandstmt_base or '|' in righthandstmt_base or '&' in righthandstmt_base or '<<' in righthandstmt_base or '>>' in righthandstmt_base: 
			return None
		lefthandstmt_base=simplify(lefthandstmt_base)
		righthandstmt_base=simplify(righthandstmt_base)

	if variable is not None and lefthandstmt is not None and righthandstmt is not None and lefthandstmt_base is not None and righthandstmt_base is not None:
		righthandstmt_d=righthandstmt
		righthandstmt_base_d=righthandstmt_base
		term1=lefthandstmt.subs(simplify(str(variable)+"+1"),0)
		term2=lefthandstmt.subs(simplify(str(variable)+"+1"),simplify(variable))
		if term1==lefthandstmt_base and  str(term2) in str(righthandstmt):
			righthandstmt=simplify(righthandstmt).subs({simplify(term2):simplify('T(n)'),simplify(variable):simplify('n')})
			result=None
			#Try to solve recurrences
			try:
				#result=recurreSolver_wolframalpha(righthandstmt,righthandstmt_base,variable_list)
				result=recurreSolver_sympy(righthandstmt,righthandstmt_base)
				#if result is None:
					#result=recurreSolver_sympy(righthandstmt,righthandstmt_base)
					#result=recurreSolver_wolframalpha(righthandstmt,righthandstmt_base,variable_list)
			except ValueError:
				result=None
			if result is not None:
				result=fun_utiles.substituteValue(fun_utiles.simplify_sympy(result),simplify('n'),simplify(variable))
				#writeLogFile( "j2llogs.logs" , "\nOriginal Axoims \n"+str(lefthandstmt)+"="+str(righthandstmt_d)+","+str(lefthandstmt_base)+"="+str(righthandstmt_base_d)+"\n Closed Form Solution\n"+str(result)+"\n" )
				if "**" in str(result):
					result=translatepowerToFun(str(result))
                                        
				expression=str(str(term2)+"="+str(result))
                                utiles_translation.resetGlobal()
                                statement_temp = utiles_translation.createASTStmt(expression)
                                
                                closed_form_soln = utiles_translation.construct_expressionC(e1[1],e1[2],expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.lvalue))),expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.rvalue))))
				#tree = p.parse_expression(expression)
				#closed_form_soln=construct_expression(tree,e1[1],e1[2])
                                
			
	#return None
	return closed_form_soln
    
"""
Recurrences Solving Module by 
#Add by Pritom Rajkhowa

"""
    
def solve_rec_m(e1,list):
        global fun_call_map
	lefthandstmt=None
	righthandstmt=None
	righthandstmt_d=None
	lefthandstmt_base=None
	righthandstmt_base=None
	righthandstmt_base_d=None
	variable=None
	closed_form_soln=None
        bascase_map={}
	if e1[0]=='i1':
		lefthandstmt=FOL_translation.expr2string1(e1[3])
		righthandstmt=FOL_translation.expr2string1(e1[4])
		lefthandstmt=lefthandstmt.strip()
		righthandstmt=righthandstmt.strip()
		variable=e1[2]
		if lefthandstmt.find('_PROVE')>0:
			return None
		elif lefthandstmt.find('_ASSUME')>0:
        		return None
		if 'ite' not in righthandstmt and '>' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '|' not in righthandstmt and '&' not in righthandstmt: 
		    	lefthandstmt=simplify(lefthandstmt)
		    	righthandstmt=simplify(righthandstmt)
		    	variable=simplify(variable)
		else:
			if '|' not in righthandstmt and '&' not in righthandstmt and '<<' not in righthandstmt and '>>' not in righthandstmt:
                            righthandstmt=FOL_translation.expr2stringSimplify(e1[4])
			righthandstmt=righthandstmt.strip()
			if 'ite' not in righthandstmt and '>' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '<' not in righthandstmt and '==' not in righthandstmt and '|' not in righthandstmt and '&' not in righthandstmt: 
				lefthandstmt=simplify(lefthandstmt)
				righthandstmt=simplify(righthandstmt)
		    		variable=simplify(variable)
			else:
				lefthandstmt=None
				righthandstmt=None
				variable=None
	if list is not None:
            for e2 in list: 
                bascase_map[simplify("T("+FOL_translation.expr2string1(e2[0])+")")]=simplify(FOL_translation.expr2string1(e2[1]))
                
	if variable is not None and lefthandstmt is not None and righthandstmt is not None and len(bascase_map)>0:
		righthandstmt_d=righthandstmt
		#righthandstmt_base_d=righthandstmt_base
		term1=lefthandstmt.subs(simplify(str(variable)+"+1"),0)
		term2=lefthandstmt.subs(simplify(str(variable)+"+1"),simplify(variable))
		if len(bascase_map)>0 and  str(term2) in str(righthandstmt):
			righthandstmt=simplify(righthandstmt).subs({simplify(term2):simplify('T(n)'),simplify(variable):simplify('n')})
			result=None
			#Try to solve recurrences
			try:
				#result=recurreSolver_wolframalpha(righthandstmt,righthandstmt_base,variable_list)
				result=recurreSolver_sympy_m(righthandstmt,bascase_map)
				#if result is None:
					#result=recurreSolver_sympy(righthandstmt,righthandstmt_base)
					#result=recurreSolver_wolframalpha(righthandstmt,righthandstmt_base,variable_list)
			except ValueError:
				result=None
			if result is not None:
				result=fun_utiles.substituteValue(fun_utiles.simplify_sympy(result),simplify('n'),simplify(variable))
				#writeLogFile( "j2llogs.logs" , "\nOriginal Axoims \n"+str(lefthandstmt)+"="+str(righthandstmt_d)+","+str(lefthandstmt_base)+"="+str(righthandstmt_base_d)+"\n Closed Form Solution\n"+str(result)+"\n" )
				if "**" in str(result):
					result=translatepowerToFun(str(result))
                                        
				expression=str(str(term2)+"="+str(result))
                                utiles_translation.resetGlobal()
                                statement_temp = utiles_translation.createASTStmt(expression)
                                
                                closed_form_soln = utiles_translation.construct_expressionC(e1[1],e1[2],expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.lvalue))),expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.rvalue))))
				#tree = p.parse_expression(expression)
				#closed_form_soln=construct_expression(tree,e1[1],e1[2])
                                
			
	#return None
	return closed_form_soln


"""
 
#Solving Recurrences using sympy
 
"""
def recurreSolver_sympy(righthandstmt,righthandstmt_base):
	expression="T(n+1)-("+str(righthandstmt)+")"
	#print expression
	f=simplify(expression)
	#Register n as Symbol
	n=Symbol('n')
	#Register T as Function
	T=Function('T')
	result=None
	#Converting String to Sympy Expression
	terminationList={sympify("T(0)"):righthandstmt_base}
	#Try to solve recurrences
	try:
		result=rsolve(f, T(n), terminationList)
		flag=False
            	flag=fun_utiles.isConstInResult( str(result) )
		if flag==False and result is not None and 'RisingFactorial' not in str(result) and 'binomial' not in str(result) and 'gamma' not in str(result) and 'rgamma' not in str(result) and 'gammaprod' not in str(result) and 'loggamma' not in str(result) and 'beta' not in str(result) and 'superfac' not in str(result) and 'barnesg' not in str(result):
			result=simplify(result)
			#writeLogFile( "j2llogs.logs" ,"\nEquation Pass to sympy\n"+str(expression)+"=0"+"------"+"Base Case--T(0)="+str(righthandstmt_base)+"\n" )
			#writeLogFile( "j2llogs.logs" ,"\nClosed form solution return by sympy \n"+str(result)+"\n" )
		else:
                    result=None
                    #writeLogFile( "j2llogs.logs" , "\nFailed to find close form solution\n" )
	except ValueError:
		result=None
		#writeLogFile( "j2llogs.logs" , "\nFailed to find close form solution\n" )

	return result




def recurreSolver_sympy_m(righthandstmt,base_map):
	expression="T(n+1)-("+str(righthandstmt)+")"
	#print expression
	f=simplify(expression)
	#Register n as Symbol
	n=Symbol('n')
	#Register T as Function
	T=Function('T')
	result=None
	#Converting String to Sympy Expression
	#terminationList={sympify("T(0)"):righthandstmt_base}
	#Try to solve recurrences
	try:
		result=rsolve(f, T(n), base_map)
		flag=False
            	flag=fun_utiles.isConstInResult( str(result) )
		if flag==False and result is not None and 'RisingFactorial' not in str(result) and 'binomial' not in str(result) and 'gamma' not in str(result) and 'rgamma' not in str(result) and 'gammaprod' not in str(result) and 'loggamma' not in str(result) and 'beta' not in str(result) and 'superfac' not in str(result) and 'barnesg' not in str(result):
			result=simplify(result)
			#writeLogFile( "j2llogs.logs" ,"\nEquation Pass to sympy\n"+str(expression)+"=0"+"------"+"Base Case--T(0)="+str(righthandstmt_base)+"\n" )
			#writeLogFile( "j2llogs.logs" ,"\nClosed form solution return by sympy \n"+str(result)+"\n" )
		else:
                    result=None
                    #writeLogFile( "j2llogs.logs" , "\nFailed to find close form solution\n" )
	except ValueError:
		result=None
		#writeLogFile( "j2llogs.logs" , "\nFailed to find close form solution\n" )

	return result


# expr_replace(e,e1,e2): replace all subterm e1 in e by e2


def expr_replace_power(e): #e,e1,e2:. expr
    args=FOL_translation.expr_args(e)
    op=FOL_translation.expr_op(e)
    if len(args)>0:
        if op=='power' or 'power_' in op :
            return eval("['**']")+list(expr_replace_power(x) for x in FOL_translation.expr_args(e))
        else:
            return e[:1]+list(expr_replace_power(x) for x in FOL_translation.expr_args(e))
    else:
        return e



"""
#Code Add by Pritom Rajkhowa
#Following Code will Translate Java Program to a Array of Statements 
"""
"""
Recurrence Solver After Translation
"""
def rec_solver(a):
    constant_fun_map={}
    equation_map={}
    base_map={}
    for axiom in a:
        if axiom[0]=='i1':
             lefthandstmt=FOL_translation.expr2string1(axiom[3])
	     lefthandstmt=lefthandstmt.strip()
             equation_map[str(simplify(lefthandstmt))]=axiom
	if axiom[0]=='i0':
	     lefthandstmt=FOL_translation.expr2string1(axiom[2])
	     lefthandstmt=lefthandstmt.strip()
	     base_map[str(simplify(lefthandstmt))]=axiom
             
    while True:
        solution_map={} 
	for equation in equation_map:
            e1=equation_map[equation]
	    equation_base=str(simplify(equation).subs(simplify(str(e1[2])+"+1"),0))
	    if equation_base in base_map.keys():
                e2=base_map[equation_base]
                result=solve_rec(e1,e2)
                if result is not None:
                    a.remove(base_map[equation_base])
                    del base_map[equation_base]
                    solution_map[equation]=result
	for equation in solution_map:
            a.remove(equation_map[equation])
	    del equation_map[equation]
	    e=solution_map[equation]
	    e1=copy.deepcopy(e)
	    variable=e[2]
	    a=fun_utiles.solnsubstitution(a,e[3],e[4])
	if len(equation_map)==0 or len(solution_map)==0:
            break
    return a



#solve_recurrence(rec_equ,var)
