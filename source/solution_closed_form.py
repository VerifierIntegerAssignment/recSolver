
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


#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=X(_n1)+1;Y(_n1+1)=X(_n1)+Y(_n1)"
#rec_equ="X(0)=A;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,ite(X(_n1)<B,X(_n1)+2,X(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+F"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"
#rec_equ="X(0)=A;Y(0)=B;Z(0)=C;M(0)=j;M(_n1+1)=X(_n1)+M(_n1);X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"
#rec_equ="X(0)=A;X(_n1+1)=ite(B>0,X(_n1)+1,ite(C>0,X(_n1)+2,X(_n1)))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1==1,1,(_n1+1)*X(_n1))"
#rec_equ="X(0)=0;X(_n1+1)=ite(_n1==1,1,1+X(_n1))"
#rec_equ="X(0)=0;X(_n1+1)=ite(_n1==1,1,(1+X(_n1)));Y(0)=1;Y(_n1+1)=ite(_n1==1,1,(_n1+1)*Y(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1==1,1,(_n1+1)*X(_n1));Y(0)=1;Y(_n1+1)=ite(_n1==1,1,(_n1+1)*Y(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B)"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1%5!=0,X(_n1)+A,X(_n1)+B)"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B);Y(0)=1;Y(_n1+1)=ite(C>0,Y(_n1)+A,Y(_n1)+B)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1)+5,X(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1)-5,X(_n1))"
#rec_equ="X(0)=2;X(_n1+1)=ite(X(_n1)%2==0,X(_n1)-5,X(_n1))"



#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)-5)"

#rec_equ="X(0)=2;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1)+5,X(_n1)-5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-5)"
#rec_equ="X(0)=10;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-15)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+15)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+15,X(_n1)-5)"
#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-15,X(_n1)+5)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1),X(_n1)+5)"
#rec_equ="X(0)=0;X(_n1+1)=ite(X(_n1)>0,X(_n1),X(_n1)+5)"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<50,X(_n1)+1,ite(_n1<70,X(_n1)+2,ite(_n1<90,X(_n1)+3,X(_n1))))"
#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<A,X(_n1)+1,ite(_n1<B,X(_n1)+2,ite(_n1<C,X(_n1)+3,X(_n1))))"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,X(_n1)+2)"

#rec_equ="X(0)=1;X(_n1+1)=ite(_n1<A,X(_n1)+1,X(_n1)+2)"



#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,ite(X(_n1)<B,X(_n1)-2,X(_n1)+2))"

#rec_equ="X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,ite(X(_n1)<B,X(_n1)+2,X(_n1)+3))"



#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(B>0,X(_n1)+Y(_n1),ite(C>0,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(B>0,X(_n1)+1,ite(C>0,X(_n1)+Y(_n1),X(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(B>0,X(_n1)+Y(_n1),ite(C>0,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(B>0,Y(_n1)+1,ite(C>0,X(_n1)+Y(_n1),Y(_n1)))"

#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(0<50,X(_n1)+Y(_n1),ite(0<70,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(0<90,X(_n1)+1,ite(C>0,X(_n1)+Y(_n1),X(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(_n1<50,X(_n1)+Y(_n1),ite(_n1<70,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(_n1<50,Y(_n1)+1,ite(_n1<70,X(_n1)+Y(_n1),Y(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(_n1<C,X(_n1)+Y(_n1),ite(_n1<D,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(_n1<C,Y(_n1)+1,ite(_n1<D,X(_n1)+Y(_n1),Y(_n1)))"
#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(_n1<C,X(_n1)+Y(_n1),X(_n1)+2);Y(_n1+1)=ite(_n1<C,Y(_n1)+1,X(_n1)+Y(_n1))"
#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(X(_n1)+Y(_n1)<C,X(_n1)+Y(_n1),X(_n1)+2);Y(_n1+1)=ite(X(_n1)+Y(_n1)<C,Y(_n1)+1,X(_n1)+Y(_n1))"


#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=ite(X(_n1)+Y(_n1)<C,X(_n1)+Y(_n1),X(_n1)-1);Y(_n1+1)=ite(X(_n1)+Y(_n1)<C,Y(_n1)-1,X(_n1)+Y(_n1))"






#rec_equ="X(0)=A;Y(0)=B;X(_n1+1)=X(_n1)+1;Y(_n1+1)=X(_n1)+Y(_n1)+1"


#rec_equ="X(0)=A;X(_n1+1)=X(_n1)+1"

#rec_equ="x2(0)=0;x2(n+1)=x2(n)+1;y(0)=0;y(n+1)=ite(x(n)<A,y(n)+1,y(n)-1);u2(0)=1;v2(0)=1;w2(0)=1;u2(n+1)=u(n)+v(n)+w(n);v(n+1)=u(n)+v(n)+w(n);w(n+1)=u(n)+v(n)+w(n)"

#rec_equ="x2(0)=0;x2(_n1+1)=x2(_n1)+1;y2(0)=0;y2(_n1+1)=ite(x2(_n1)<50,y2(_n1)+1,y2(_n1)-1);z2(0)=0;z2(_n1+1)=ite(z2(_n1)<60,z2(_n1)+4,z2(_n1)-2);u2(0)=1;v2(0)=1;w2(0)=1;u2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);v2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);w2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1)"

#rec_equ="x2(0)=0;x2(_n1+1)=x2(_n1)+1;y2(0)=0;y2(_n1+1)=ite(x2(_n1)<50,y2(_n1)+1,y2(_n1)-1);u2(0)=1;v2(0)=1;w2(0)=1;u2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);v2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);w2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1)"



#rec_equ="u2(0)=1;v2(0)=1;w2(0)=1;u2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);v2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1);w2(_n1+1)=u2(_n1)+v2(_n1)+w2(_n1)"

#rec_equ="z2(0)=0;z2(_n1+1)=ite(z2(_n1)<60,z2(_n1)+4,z2(_n1)-2)"

#rec_equ="z2(0)=0;z2(_n1+1)=ite(z2(_n1)<60,z2(_n1)+4,z2(_n1)-4)"


#var = "_n1"

def solve_recurrence(rec_equ,var):
    
    rec_list = rec_equ.split(';')
    
    list_equations=[]
    
    list_solutions = []
    
    axoims=None
    
    
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
    
    
    results,soln_map = rec_solver_group(list_equations)
    
    for x in soln_map:
        
        results.append(soln_map[x])
    
    
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
    #print list_equations
    #print '-----------------'
    if len(list_equations)>0:
        
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
    print 'ADDITIONAL AXIOMS'
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
        
        #res_expr ="['ite',['==',['"+var+"'],['0']],"+str(list_of_value[1])+","+"['+',"+"['+',"+"['*',['*',['power',['"+str(len(list_of_values))+"'],['"+var+"']],"+"['power',"+const_value+",['"+var+"']]],"+const_expr+const_expr_end+"]"+","+"['*',"+const_coeff+const_coeff_end+",['/'"+",['*',"+const_value+",['-',['1'],['*',['power',['"+str(len(list_of_values))+"'],['"+var+"']],['power',"+const_value+",['"+var+"']]]]],"+"['-',['1'],['*',['"+str(len(list_of_values))+"'],"+const_value+"]]]]],"+str(list_of_value[1])+"]"+"]"
        
        res_expr ="['ite',['==',['"+var+"'],['0']],"+str(list_of_value[2])+","+"['+',"+"['+',"+"['*',['*',['**',['"+str(len(list_of_values))+"'],['"+var+"']],"+"['**',"+const_value+",['"+var+"']]],"+const_expr+const_expr_end+"]"+","+"['*',"+const_coeff+const_coeff_end+",['/'"+",['*',"+const_value+",['-',['1'],['*',['**',['"+str(len(list_of_values))+"'],['"+var+"']],['**',"+const_value+",['"+var+"']]]]],"+"['-',['1'],['*',['"+str(len(list_of_values))+"'],"+const_value+"]]]]],"+str(list_of_value[1])+"]"+"]"
        
        express_main="['i2', '0', '"+var+"',"+str(list_of_value[3])+","+res_expr+"]"
        
        solutions.append(eval(express_main))
        
    return solutions





def iscofficentEqual(new_coeff,var):
    status=True
    list1=new_coeff.keys()
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
                    
                    print '$$$$$$$$$$$$$$$$$$$$$$$$'
                    print z[0]
                    print '$$$$$$$$$$$$$$$$$$$$$$$$'
                    
                    if fun_utiles.isFunctionPresent(z[0])==True:
                        
                        if solution_type==None:
                            
                           solution_type='Function'
                           
                        elif solution_type=='Counter' or solution_type=='Constant' or solution_type=='Base Case':
                            
                            solution_type='Function'
                            
                        else:
                            solution_type='Function'
                            
                        z.append(solution_type)
                        
                    elif fun_utiles.isVariablePresent(z[0])==True and fun_utiles.isFunctionPresent(z[0])!=True:
                        
                        print '%%%%%%%%Ram Ram%%%%%%%%%%%%%%%'
                        print (z[0][0]=='==' or z[0][0]=='!=') 
                        print z[0][1][0]=='%' 
                        print z[0][1][1][0]==var 
                        print fun_utiles.is_number(z[0][1][2][0])==True
                        print '%%%%%%%%Ram Ram%%%%%%%%%%%%%%%'
                        
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
                        print '+++++++++++++++++++++'
                        print solution_type
                        print '+++++++++++++++++++++'
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
    else:
        
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
                
            soln = solveGroupConstantType(group_list, equations_map, basecase_map, list_equations)
            
            if soln is not None:
                    
                if solution_list is not None:
                    
                    solution_list+=soln
                    
                else:
                    
                    solution_list=soln
                    
        elif solution_type=='Counter':
            
            soln,add_axm = solveGroupCounterType(group_list, equations_map, basecase_map, list_equations)
                        
            if soln is not None:
                    
                if solution_list is not None:
                    
                    solution_list+=soln
                    
                else:
                    
                    solution_list=soln
                    
            if add_axm is not None:
                
                if  additional_axoims is not None:
                    
                    additional_axoims+=add_axm
                    
                else:
                    
                    additional_axoims =add_axm
                    
        elif solution_type=='Function':
            
            soln,add_axm = solveGroupFunctionType(group_list, equations_map, basecase_map, list_equations)
                        
            if soln is not None:
                    
                if solution_list is not None:
                    
                    solution_list+=soln
                    
                else:
                    
                    solution_list=soln
                    
            if add_axm is not None:
                
                if  additional_axoims is not None:
                    
                    additional_axoims+=add_axm
                    
                else:
                    
                    additional_axoims =add_axm
            
            print solution_type

    
    return solution_list,additional_axoims
                



def constructInfoSystem(e, equations_map, basecase_map, list_equations):
    
    global ConstraintCount
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    e_base = basecase_map[equation_base]
    
    e_solution=None
    
    e_end=''
    
    close_form=None
    
    
    for x in e[6]:
        
        list1=[]
        
        new_e=eval("['"+e[1][0]+"','"+e[1][1]+"','"+e[1][2]+"',"+str(e[1][3])+","+str(e[6][x][1])+"]")
        
        ConstraintCount = ConstraintCount+1
        
        e_new_base=copy.deepcopy(e_base)
        
        e_new_base[-1]=eval("['_CV"+str(ConstraintCount)+"']")
        
        
        sol = solve_rec(new_e,e_new_base)
        
                
        if sol is not None:
            
            list1.append(e[6][x][2])
                    
            if e[6][x][0] is not None:
                
                e[6][x][0] = fun_utiles.expr_replace(e[6][x][0],sol[-2],sol[-1])
                
                e_new = copy.deepcopy(e[6][x][0])
        
                #e_new = fun_utiles.expr_replace(e_new,sol[-2],sol[-1])
                
            else:
                
                e_new=None
                
            list1.append(sol)
            
            list1.append(e_new)
            
                        
            if e_new is not None:
                
                
                constraint_list=[]
                
                equation_list=[]
                
                e_new1 = copy.deepcopy(sol[-1])
                                
                e_new1_in = copy.deepcopy(sol[-1])
                
                e_new1_in = fun_utiles.expr_replace(e_new1_in,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['1']]"))
                
                                
                
                if e_new1==e_new1_in:
                    
                    list1.append('constant')
                
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
                    
                        list1.append('increasing')
                    
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
                        
                            list1.append('decreasing')

        
                
                equation_list=[]
                
                constraint_list=[]
                
                #e_new1 = fun_utiles.expr_replace(e_new1,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['_CS"+str(ConstraintCount)+"']]"))
                
                
                #e_new = fun_utiles.expr_replace(e_new,eval("['"+e[1][2]+"']"),eval("['-',['"+e[1][2]+"'],['1']]"))
                                
                
                e_new2 = copy.deepcopy(e_new)
                
                e_new2 = fun_utiles.expr_complement(e_new2)
                
                e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+e[1][2]+"']"),eval("['_CE"+str(ConstraintCount)+"']"))

                
                equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(ConstraintCount)+"'],['"+e[1][2]+"']],"+"['<',['"+e[1][2]+"'],['_CE"+str(ConstraintCount)+"']]"+"],"+str(e_new)+"]]")
            
                
                equation2 = eval("['s0',"+str(e_new2)+"]")
                
                constraint1 = eval("['a',['<=',['0'],['_CE"+str(ConstraintCount)+"']]]")
                
                constraint11 = eval("['a',['<=',['0'],['_CS"+str(ConstraintCount)+"']]]")
                
                constraint2 = eval("['a',['<',['_CS"+str(ConstraintCount)+"'],['_CE"+str(ConstraintCount)+"']]]")
                
                
                list1.append(ConstraintCount)
                
                list1.append(equation1)
                list1.append(equation2)
                list1.append(constraint1)
                list1.append(constraint11)
                list1.append(constraint2)
                
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
                    
                    list1.append('Always True')
                    
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
                        list1.append('No Repeat')
            
            if e_new is not None:
                
                constraint_list=[]
            
                e_cond = copy.deepcopy(e_new)
            
                e_cond = fun_utiles.expr_replace(e_cond,eval("['"+e[1][2]+"']"),eval("['0']"))
                
                e_cond = fun_utiles.expr_replace(e_cond,e_base[-2],e_base[-1])
                
                e_cond = eval("['s0',"+str(e_cond)+"]")
                
                constraint_list.append(FOL_translation.wff2z3_update(e_cond))
                
                status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                                
                if 'Counter Example' in status:
                    
                    list1.append('Initial')
                                                                                
                elif 'Successfully Proved' in status:
                    
                    list1.append('Never Initial')
                    
                else:
                    
                    list1.append(e_cond)

            else:
                
                list1.append(None)
                list1.append(str(ConstraintCount))
            
            e[6][x].append(list1)
            
                
        else:
            
            return None

    return e





def isGroupConditions(group_list):
    
    cond_map=None
    
    for x in group_list:

        if cond_map is None:
            
            cond_map = x[6].keys()
            
        else:
            
            temp_cond_map = x[6].keys()
            
            if cond_map!=temp_cond_map:
                
                return False
            
    return True



def isGroupMonotonic(condition_map):
    
    type=None
    
    for x in condition_map:
                        
        for y in condition_map[x]:
            
            if type is None:
                                
                if y[-1] is not None:
                    
                    type=y[-1]
                
            elif type != y[-1]:
                
                type=None
                
    return type





def constructInfoSystemGroup(group_list, equations_map, basecase_map, list_equations):
    
    global ConstraintCount
    
    local_count=0
    
    condition_map={}
    
    condition_map_exp={}
    
    for x in group_list:
        
        
        for y in x[-1]:
                        
            local_count+=1
            
            list1=[]
            
            list1.append(x[0])
            
            list1.append(x[1][2])
            
            list1.append(x[1][-2])
            
            list1.append(x[-1][y])
            
            list1.append(local_count)
            
            if y in condition_map.keys():
                
                main_list = condition_map[y]
                
                temp_list = main_list[0]
                
                list1.append(temp_list[-1])
                
                main_list = condition_map[y]
                
                main_list.append(list1)
                
                condition_map[y] = main_list
                
            else:
                
                ConstraintCount+=1
                
                list1.append(ConstraintCount)
                
                main_list=[]
                
                main_list.append(list1)
                
                condition_map[y] = main_list
                
                
    for x in condition_map:
    
            #condition_map_exp[]        
        a_list=[]
        
        for y in condition_map[x]:
                        
            equation_base = str(simplify(y[0]).subs(simplify(str(y[1])+"+1"),0))
    
            e_base = basecase_map[equation_base]
            
            y.append(e_base)
            
            e_new_base=copy.deepcopy(e_base)
        
            e_new_base[-1]=eval("['_CV"+str(y[4])+"']")
                        
            new_e=eval("['i1','"+str(0)+"','"+y[1]+"',"+str(y[2])+","+str(y[3][1])+"]")
            
            a_list.append(new_e)
            
            a_list.append(e_new_base)
            
            
             
        a_list,soln = rec_solver_group(a_list)
        
        
        if len(a_list)>0:
            
            return None,None
        
        else:
            
            for y in condition_map[x]:
                
                #condition_map_exp[x]=
                
                if  y[0] in soln:
                    
                    y.append(soln[y[0]])
                    
                    if y[3][0] is not None:
                                            
                        e_new2 = copy.deepcopy(y[3][0])
                
                        e_new2 = fun_utiles.expr_complement(e_new2)

                    
                        equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(y[-3])+"'],['"+y[1]+"']],"+"['<',['"+y[1]+"'],['_CE"+str(y[-3])+"']]"+"],"+str(y[3][0])+"]]")
            
                        e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+y[1]+"']"),eval("['_CE"+str(y[-3])+"']"))
                        
                        equation2 = eval("['s0',"+str(e_new2)+"]")
                
                        constraint1 = eval("['a',['<=',['0'],['_CE"+str(y[-3])+"']]]")
                
                        constraint2 = eval("['a',['<=',['0'],['_CS"+str(y[-3])+"']]]")
                
                        constraint3 = eval("['a',['<',['_CS"+str(y[-3])+"'],['_CE"+str(y[-3])+"']]]")
                    
                        list1 =[]
                    
                        list1.append(equation1)
                        list1.append(equation2)
                        list1.append(constraint1)
                        list1.append(constraint2)
                        list1.append(constraint3)
                        
                        y.append(list1)
                        
                    else:
                        
                        y.append(None)
                        
                    #print y[7][-1]
                    e_new_in = copy.deepcopy(y[7][-1])
                    
                    e_new_in = fun_utiles.expr_replace(e_new_in,eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                    
                    if e_new_in==y[7][-1]:
                        
                        y.append('Constant')
                        
                    else:
                        
                        equation_list=[]
                        
                        constraint_list=[]
                        
                        constraint_in =  eval("['s0',['<=',"+str(y[7][-1])+","+str(e_new_in)+"]]")
                    
                        equation_list.append(constraint_in)
                    
                        constraint_list.append(FOL_translation.wff2z3_update(constraint_in))
                
                
                        var_map={}
    
                        FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                        vfacts=[]
                
                        for vfact in var_map:
                            vfacts.append(var_map[vfact])

                        status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                        
                        if 'Counter Example' in status:
                    
                            y.append('increasing')
                            
                        elif 'Successfully Proved' in status:
                    
                            y.append('Always True')
                            
                            
                        else:

                            equation_list=[]
                        
                            constraint_list=[]
                        
                            constraint_in =  eval("['s0',['>=',"+str(y[7][-1])+","+str(e_new_in)+"]]")
                    
                            equation_list.append(constraint_in)
                    
                            constraint_list.append(FOL_translation.wff2z3_update(constraint_in))
                
                
                            var_map={}
    
                            FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                            vfacts=[]
                
                            for vfact in var_map:
                                vfacts.append(var_map[vfact])

                            status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                            
                            if 'Counter Example' in status:
                    
                                y.append('increasing')
                            
                            elif 'Successfully Proved' in status:
                    
                                y.append('Always True')
                                
                            else:

                                y.append(None)
                                

    #for x in condition_map:
        
    #    print x #key condition
        
    #    for y in condition_map[x]:
            
    #        print y[0]  #key condition
    #        print y[1]  #Inductive varible
    #        print y[2]  #Left Expression
    #        print y[3]  #List condition expression, Right Expression, Function Type
    #        print y[4]  #Local Count
    #        print y[5]  #Global Count
    #        print y[6]  #Base Case
    #        print y[7]  #Solution
    #        print y[8]  #Constraint List
    #        print y[9]  #Type 
    #for x in condition_map:
    #    print x
    #    print 
    return condition_map





def constructInfoSystemGroupFunction(group_list, equations_map, basecase_map, list_equations):
    
    global ConstraintCount
    
    local_count=0
    
    condition_map={}
    
    condition_map_exp={}
    
    for x in group_list:
                
        for y in x[-1]:
                        
            local_count+=1
            
            list1=[]
            
            list1.append(x[0])
            
            list1.append(x[1][2])
            
            list1.append(x[1][-2])
            
            list1.append(x[-1][y])
            
            list1.append(local_count)
            
            if y in condition_map.keys():
                
                main_list = condition_map[y]
                
                temp_list = main_list[0]
                
                list1.append(temp_list[-1])
                
                main_list = condition_map[y]
                
                main_list.append(list1)
                
                condition_map[y] = main_list
                
            else:
                
                ConstraintCount+=1
                
                list1.append(ConstraintCount)
                
                main_list=[]
                
                main_list.append(list1)
                
                condition_map[y] = main_list
                
                
    for x in condition_map:
    
            #condition_map_exp[]        
        a_list=[]
        
        for y in condition_map[x]:
                        
            equation_base = str(simplify(y[0]).subs(simplify(str(y[1])+"+1"),0))
    
            e_base = basecase_map[equation_base]
            
            y.append(e_base)
            
            e_new_base=copy.deepcopy(e_base)
        
            e_new_base[-1]=eval("['_CV"+str(y[4])+"']")
                        
            new_e=eval("['i1','"+str(0)+"','"+y[1]+"',"+str(y[2])+","+str(y[3][1])+"]")
            
            a_list.append(new_e)
            
            a_list.append(e_new_base)
            
            
             
        a_list,soln = rec_solver_group(a_list)
        
        
        if len(a_list)>0:
            
            return None
        
        else:
            
            for y in condition_map[x]:
                
                #condition_map_exp[x]=
                
                if  y[0] in soln:
                    
                    y.append(soln[y[0]])
                    
                    if y[3][0] is not None:
                        
                        for key in soln:
                                                    
                            y[3][0] = fun_utiles.expr_replace(y[3][0],soln[key][-2],soln[key][-1])
                        
                                            
                        e_new2 = copy.deepcopy(y[3][0])
                
                        e_new2 = fun_utiles.expr_complement(e_new2)

                    
                        equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(y[-3])+"'],['"+y[1]+"']],"+"['<',['"+y[1]+"'],['_CE"+str(y[-3])+"']]"+"],"+str(y[3][0])+"]]")
            
                        e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+y[1]+"']"),eval("['_CE"+str(y[-3])+"']"))
                        
                        equation2 = eval("['s0',"+str(e_new2)+"]")
                
                        constraint1 = eval("['a',['<=',['0'],['_CE"+str(y[-3])+"']]]")
                
                        constraint2 = eval("['a',['<=',['0'],['_CS"+str(y[-3])+"']]]")
                
                        constraint3 = eval("['a',['<',['_CS"+str(y[-3])+"'],['_CE"+str(y[-3])+"']]]")
                    
                        list1 =[]
                    
                        list1.append(equation1)
                        list1.append(equation2)
                        list1.append(constraint1)
                        list1.append(constraint2)
                        list1.append(constraint3)
                        
                        y.append(list1)
                        
                    else:
                        
                        y.append(None)
                        
                    #print y[7][-1]
                    e_new_in = copy.deepcopy(y[7][-1])
                    
                    e_new_in = fun_utiles.expr_replace(e_new_in,eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                    
                    if e_new_in==y[7][-1]:
                        
                        y.append('Constant')
                        
                    else:
                        
                        equation_list=[]
                        
                        constraint_list=[]
                        
                        constraint_in =  eval("['s0',['<=',"+str(y[7][-1])+","+str(e_new_in)+"]]")
                    
                        equation_list.append(constraint_in)
                                            
                        constraint_list.append(FOL_translation.wff2z3_update(constraint_in))
                
                
                        var_map={}
    
                        FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                        vfacts=[]
                
                        for vfact in var_map:
                            vfacts.append(var_map[vfact])

                        status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                        
                        if 'Counter Example' in status:
                    
                            y.append('increasing')
                                                        
                            
                        else:

                            equation_list=[]
                        
                            constraint_list=[]
                        
                            constraint_in =  eval("['s0',['>=',"+str(y[7][-1])+","+str(e_new_in)+"]]")
                    
                            equation_list.append(constraint_in)
                    
                            constraint_list.append(FOL_translation.wff2z3_update(constraint_in))
                
                
                            var_map={}
    
                            FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                            vfacts=[]
                
                            for vfact in var_map:
                                vfacts.append(var_map[vfact])

                            status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                            
                            if 'Counter Example' in status:
                    
                                y.append('increasing')
                                                            
                            else:
                                
                                return None

                                y.append(None)
                                

    #for x in condition_map:
        
    #    print x #key condition
        
    #    for y in condition_map[x]:
            
    #        print y[0]  #key condition
    #        print y[1]  #Inductive varible
    #        print y[2]  #Left Expression
    #        print y[3]  #List condition expression, Right Expression, Function Type
    #        print y[4]  #Local Count
    #        print y[5]  #Global Count
    #        print y[6]  #Base Case
    #        print y[7]  #Solution
    #        print y[8]  #Constraint List
    #        print y[9]  #Type 
    #for x in condition_map:
    #    print x
    #    print 
    return condition_map
            
            
            
            

                    
                    
        


def solveGroupCounterType(group_list, equations_map, basecase_map, list_equations):
    
    
    
    condition_map=None
    
    status = isGroupConditions(group_list)
    
    soln_cons_map={}
    
    soln_none_map={}
    
    soln_main_map={}
    
    soln_main_end_map={}
    
    soln_main_final_map={}
    
    main_soln_map={}
    
    soln_map={}
    
    additional_axoms = [] 
    
    final_soln_list= []
    
    if status is True:
        
        condition_map = constructInfoSystemGroup(group_list, equations_map, basecase_map, list_equations)
        
    
    if condition_map is not None:
        
        constraint_list = []
    
        equation_list = []

        for x in condition_map:
            
            e_list = condition_map[x][1][8]
            
            if e_list is not None:
                for y in e_list:
                
                    constraint_list.append(FOL_translation.wff2z3_update(y))
                
                    equation_list.append(y)
                
                
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
                                
                if len(list_values)==len(condition_map)-1:
                
                    for x in list_values:
                    
                        for key,value in map_counter_CE.iteritems():
                        
                            if value==x:
                            
                                list_sort.append(key)
                                
                    
                    for y in list_sort:
                        
                        for x in condition_map:
                        
                            for e in condition_map[x]:
                                
                                if '_CE'+str(e[5])==y:
                                    
                                    
                                    if e[0] in soln_cons_map:
                                        
                                        list1 = soln_cons_map[e[0]]
                                        
                                        list1.append(e)
                                        
                                        soln_cons_map[e[0]]=list1

                                        
                                    else:
                                        
                                        list1=[]
                                        
                                        list1.append(e)
                                        
                                        soln_cons_map[e[0]]=list1
                                        
                                if e[3][0]==None:
                                    
                                    soln_none_map[e[0]] = e
                                    
                                    
                    #soln_map
                    
                    soln_main_final_map,additional_axoms = constructSolution(soln_cons_map, soln_none_map, len(list_sort))
                    
                    for index in soln_main_final_map:
                        
                        soln = soln_main_final_map[index]
                        
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms


            else:
                
                soln_cons_map={}
                
                soln_none_map={}
                
                soln_final_map={}
                
                isConstnat=None
                
                list_con_expression = []
                
                for x in condition_map:
                    if x is None:
                        for y in condition_map[x]:
                            if y[-1]!='Constant':
                                isConstnat=False
                                
                            soln_none_map[y[0]]=y
                    
                    else:
                        
                        list_con_expression.append(x)
                                
                none_cond=None
                
                if isConstnat is not None:
                    cond=None
                    cond_end=None
                    for x in condition_map:
                        if cond is None:
                            temp_cond = condition_map[x][0][3][0]
                            if temp_cond is not None:
                                cond = str(temp_cond)
                        else:
                            temp_cond = condition_map[x][0][3][0]
                            if temp_cond is not None:
                                cond ="['or',"+str(temp_cond)+","+cond+"]"
                                                        
                    none_cond = eval("['!',"+cond+"]")
                
                if isConstnat is None:
                
                    local_count=1
                                
                    perm = permutations(list_con_expression,len(list_con_expression))
                
                    for x in list(perm):
                                        
                        local_count=local_count+1
                    
                        soln_cons_map={}
                    
                        list_seq =[]
                    
                        for i in range(0,len(x)):
                        
                            if x[i] in condition_map:
                        
                                y = condition_map[x[i]]
                            
                                for e in y:
                                
                                    list_seq.append(e[5])
                                
                                    if e[0] not in soln_cons_map:
                                    
                                        temp_list=[]
                                    
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                                    else:
                                    
                                        temp_list = soln_cons_map[e[0]]
                                    
                                        #if e not in temp_list:
                                        
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                    
                    
                        soln_main_final_map, add_axoms = constructSolution(soln_cons_map, soln_none_map, len(x))
                    
                        for index in soln_main_final_map:
                        
                            for seq in list_seq:
                            
                                soln_main_final_map[index][-1] = fun_utiles.expr_replace(soln_main_final_map[index][-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))

                        
                            if index not in soln_final_map:
                            
                                temp_list=[]
                            
                                temp_list.append("['i2',0,'"+soln_main_final_map[index][2]+"',"+str(soln_main_final_map[index][3]))
                            
                                temp_list.append(str(soln_main_final_map[index][4]))
                            
                                temp_list.append("]")
                            
                                soln_final_map[index]=temp_list
                            
                            else:
                            
                                temp_list = soln_final_map[index]
                            
                                str_sol = temp_list[1]
                            
                                str_sol = "['or',"+str(str(soln_main_final_map[index][4]))+","+str_sol+"]"
                            
                                temp_list[1]=str_sol
                            
                                soln_final_map[index]=temp_list
                            
                        
                        
                        for axm in add_axoms:
                    
                            for seq in list_seq:
                            
                                axm[-1] = fun_utiles.expr_replace(axm[-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))
                            
                            additional_axoms.append(axm)

                        
                    for index in soln_final_map:
                    
                        soln = eval(soln_final_map[index][0]+","+soln_final_map[index][1]+soln_final_map[index][2])
                    
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms
                    
                    
                else:
                    
                        
                        
                    for y in  condition_map[None]:
                        
                        e_new2 = copy.deepcopy(none_cond)
                
                        e_new2 = fun_utiles.expr_complement(e_new2)
                    
                        equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(y[5])+"'],['"+y[7][2]+"']],"+"['<',['"+y[7][2]+"'],['_CE"+str(y[5])+"']]"+"],"+str(none_cond)+"]]")
            
                        e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+y[7][2]+"']"),eval("['_CE"+str(y[5])+"']"))
                        
                        equation2 = eval("['s0',"+str(e_new2)+"]")
                
                        constraint1 = eval("['a',['<=',['0'],['_CE"+str(y[5])+"']]]")
                
                        constraint2 = eval("['a',['<=',['0'],['_CS"+str(y[5])+"']]]")
                
                        constraint3 = eval("['a',['<',['_CS"+str(y[5])+"'],['_CE"+str(y[5])+"']]]")
                    
                        list1 =[]
                    
                        list1.append(equation1)
                    
                        list1.append(equation2)
                    
                        list1.append(constraint1)
                    
                        list1.append(constraint2)
                    
                        list1.append(constraint3)
                        
                        y[3][0] = none_cond
                        
                        y[8] = list1
                        
                        y[3][2] = 'Counter'
                        
                    
                    list_con_expression = condition_map.keys()
                    
                    local_count=1
                                
                    perm = permutations(list_con_expression,len(list_con_expression))
                
                    for x in list(perm):
                                                                    
                        local_count=local_count+1
                    
                        soln_cons_map={}
                        
                        soln_none_map={}
                    
                        list_seq =[]
                    
                        for i in range(0,len(x)):
                        
                            if i!=len(x)-1 and x[i] in condition_map:
                        
                                y = condition_map[x[i]]
                            
                                for e in y:
                                
                                    list_seq.append(e[5])
                                
                                    if e[0] not in soln_cons_map:
                                    
                                        temp_list=[]
                                    
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                                    else:
                                    
                                        temp_list = soln_cons_map[e[0]]
                                        
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                else:
                                    
                                    y = condition_map[x[i]]
                                    
                                    for e in y:
                                    
                                        soln_none_map[e[0]]=e


                        soln_main_final_map, add_axoms = constructSolution(soln_cons_map, soln_none_map, len(x)-1)
                    
                        for index in soln_main_final_map:
                        
                            for seq in list_seq:
                            
                                soln_main_final_map[index][-1] = fun_utiles.expr_replace(soln_main_final_map[index][-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))

                        
                            if index not in soln_final_map:
                            
                                temp_list=[]
                            
                                temp_list.append("['i2',0,'"+soln_main_final_map[index][2]+"',"+str(soln_main_final_map[index][3]))
                            
                                temp_list.append(str(soln_main_final_map[index][4]))
                            
                                temp_list.append("]")
                            
                                soln_final_map[index]=temp_list
                            
                            else:
                            
                                temp_list = soln_final_map[index]
                            
                                str_sol = temp_list[1]
                            
                                str_sol = "['or',"+str(str(soln_main_final_map[index][4]))+","+str_sol+"]"
                            
                                temp_list[1]=str_sol
                            
                                soln_final_map[index]=temp_list
                            
                        
                        
                        for axm in add_axoms:
                    
                            for seq in list_seq:
                            
                                axm[-1] = fun_utiles.expr_replace(axm[-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))
                            
                            additional_axoms.append(axm)

                        
                    for index in soln_final_map:
                    
                        soln = eval(soln_final_map[index][0]+","+soln_final_map[index][1]+soln_final_map[index][2])
                    
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms       
                            



 
                           
def solveGroupFunctionType(group_list, equations_map, basecase_map, list_equations):
    
    condition_map=None
    
    status = isGroupConditions(group_list)
    
    soln_cons_map={}
    
    soln_none_map={}
    
    soln_main_map={}
    
    soln_main_end_map={}
    
    soln_main_final_map={}
    
    main_soln_map={}
    
    soln_map={}
    
    additional_axoms = [] 
    
    final_soln_list= []
    
    if status is True:
        
        condition_map = constructInfoSystemGroupFunction(group_list, equations_map, basecase_map, list_equations)
                
        if condition_map is not None:
        
            type = isGroupMonotonic(condition_map)
                    
            if type is None:
            
                return None,None
        else:
            
            return None,None
        
    
    if condition_map is not None:
        
        constraint_list = []
    
        equation_list = []

        for x in condition_map:
            
            e_list = condition_map[x][1][8]
            
            if e_list is not None:
                for y in e_list:
                
                    constraint_list.append(FOL_translation.wff2z3_update(y))
                
                    equation_list.append(y)
                
                
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
                                
                if len(list_values)==len(condition_map)-1:
                
                    for x in list_values:
                    
                        for key,value in map_counter_CE.iteritems():
                        
                            if value==x:
                            
                                list_sort.append(key)
                                
                    
                    for y in list_sort:
                        
                        for x in condition_map:
                        
                            for e in condition_map[x]:
                                
                                if '_CE'+str(e[5])==y:
                                    
                                    
                                    if e[0] in soln_cons_map:
                                        
                                        list1 = soln_cons_map[e[0]]
                                        
                                        list1.append(e)
                                        
                                        soln_cons_map[e[0]]=list1

                                        
                                    else:
                                        
                                        list1=[]
                                        
                                        list1.append(e)
                                        
                                        soln_cons_map[e[0]]=list1
                                        
                                if e[3][0]==None:
                                    
                                    soln_none_map[e[0]] = e
                                    
                                    
                    #soln_map
                    
                    soln_main_final_map,additional_axoms = constructSolution(soln_cons_map, soln_none_map, len(list_sort))
                    
                    for index in soln_main_final_map:
                        
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms


            else:
                
                soln_cons_map={}
                
                soln_none_map={}
                
                soln_final_map={}
                
                isConstnat=None
                
                list_con_expression = []
                
                for x in condition_map:
                    if x is None:
                        for y in condition_map[x]:
                            if y[-1]!='Constant':
                                isConstnat=False
                                
                            soln_none_map[y[0]]=y
                    
                    else:
                        
                        list_con_expression.append(x)
                                
                none_cond=None
                
                if isConstnat is not None:
                    cond=None
                    cond_end=None
                    for x in condition_map:
                        if cond is None:
                            temp_cond = condition_map[x][0][3][0]
                            if temp_cond is not None:
                                cond = str(temp_cond)
                        else:
                            temp_cond = condition_map[x][0][3][0]
                            if temp_cond is not None:
                                cond ="['or',"+str(temp_cond)+","+cond+"]"
                                                        
                    none_cond = eval("['!',"+cond+"]")
                
                if isConstnat is None:
                
                    local_count=1
                                
                    perm = permutations(list_con_expression,len(list_con_expression))
                
                    for x in list(perm):
                                        
                        local_count=local_count+1
                    
                        soln_cons_map={}
                    
                        list_seq =[]
                    
                        for i in range(0,len(x)):
                        
                            if x[i] in condition_map:
                        
                                y = condition_map[x[i]]
                            
                                for e in y:
                                
                                    list_seq.append(e[5])
                                
                                    if e[0] not in soln_cons_map:
                                    
                                        temp_list=[]
                                    
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                                    else:
                                    
                                        temp_list = soln_cons_map[e[0]]
                                    
                                        #if e not in temp_list:
                                        
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                    
                    
                        soln_main_final_map, add_axoms = constructSolution(soln_cons_map, soln_none_map, len(x))
                    
                        for index in soln_main_final_map:
                        
                            for seq in list_seq:
                            
                                soln_main_final_map[index][-1] = fun_utiles.expr_replace(soln_main_final_map[index][-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))

                        
                            if index not in soln_final_map:
                            
                                temp_list=[]
                            
                                temp_list.append("['i2',0,'"+soln_main_final_map[index][2]+"',"+str(soln_main_final_map[index][3]))
                            
                                temp_list.append(str(soln_main_final_map[index][4]))
                            
                                temp_list.append("]")
                            
                                soln_final_map[index]=temp_list
                            
                            else:
                            
                                temp_list = soln_final_map[index]
                            
                                str_sol = temp_list[1]
                            
                                str_sol = "['or',"+str(str(soln_main_final_map[index][4]))+","+str_sol+"]"
                            
                                temp_list[1]=str_sol
                            
                                soln_final_map[index]=temp_list
                            
                        
                        
                        for axm in add_axoms:
                    
                            for seq in list_seq:
                            
                                axm[-1] = fun_utiles.expr_replace(axm[-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))
                            
                            additional_axoms.append(axm)

                        
                    for index in soln_final_map:
                    
                        soln = eval(soln_final_map[index][0]+","+soln_final_map[index][1]+soln_final_map[index][2])
                    
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms
                    
                    
                else:
                    
                        
                        
                    for y in  condition_map[None]:
                        
                        e_new2 = copy.deepcopy(none_cond)
                
                        e_new2 = fun_utiles.expr_complement(e_new2)
                    
                        equation1 = eval("['s1',['implies',"+"['and',"+"['<=',['_CS"+str(y[5])+"'],['"+y[7][2]+"']],"+"['<',['"+y[7][2]+"'],['_CE"+str(y[5])+"']]"+"],"+str(none_cond)+"]]")
            
                        e_new2 = fun_utiles.expr_replace(e_new2,eval("['"+y[7][2]+"']"),eval("['_CE"+str(y[5])+"']"))
                        
                        equation2 = eval("['s0',"+str(e_new2)+"]")
                
                        constraint1 = eval("['a',['<=',['0'],['_CE"+str(y[5])+"']]]")
                
                        constraint2 = eval("['a',['<=',['0'],['_CS"+str(y[5])+"']]]")
                
                        constraint3 = eval("['a',['<',['_CS"+str(y[5])+"'],['_CE"+str(y[5])+"']]]")
                    
                        list1 =[]
                    
                        list1.append(equation1)
                    
                        list1.append(equation2)
                    
                        list1.append(constraint1)
                    
                        list1.append(constraint2)
                    
                        list1.append(constraint3)
                        
                        y[3][0] = none_cond
                        
                        y[8] = list1
                        
                        y[3][2] = 'Counter'
                        
                    
                    list_con_expression = condition_map.keys()
                    
                    local_count=1
                                
                    perm = permutations(list_con_expression,len(list_con_expression))
                
                    for x in list(perm):
                                                                    
                        local_count=local_count+1
                    
                        soln_cons_map={}
                        
                        soln_none_map={}
                    
                        list_seq =[]
                    
                        for i in range(0,len(x)):
                        
                            if i!=len(x)-1 and x[i] in condition_map:
                        
                                y = condition_map[x[i]]
                            
                                for e in y:
                                
                                    list_seq.append(e[5])
                                
                                    if e[0] not in soln_cons_map:
                                    
                                        temp_list=[]
                                    
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                    
                                    else:
                                    
                                        temp_list = soln_cons_map[e[0]]
                                        
                                        temp_list.append(e)
                                    
                                        soln_cons_map[e[0]] = temp_list
                                else:
                                    
                                    y = condition_map[x[i]]
                                    
                                    for e in y:
                                    
                                        soln_none_map[e[0]]=e


                        soln_main_final_map, add_axoms = constructSolution(soln_cons_map, soln_none_map, len(x)-1)
                    
                        for index in soln_main_final_map:
                        
                            for seq in list_seq:
                            
                                soln_main_final_map[index][-1] = fun_utiles.expr_replace(soln_main_final_map[index][-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))

                        
                            if index not in soln_final_map:
                            
                                temp_list=[]
                            
                                temp_list.append("['i2',0,'"+soln_main_final_map[index][2]+"',"+str(soln_main_final_map[index][3]))
                            
                                temp_list.append(str(soln_main_final_map[index][4]))
                            
                                temp_list.append("]")
                            
                                soln_final_map[index]=temp_list
                            
                            else:
                            
                                temp_list = soln_final_map[index]
                            
                                str_sol = temp_list[1]
                            
                                str_sol = "['or',"+str(str(soln_main_final_map[index][4]))+","+str_sol+"]"
                            
                                temp_list[1]=str_sol
                            
                                soln_final_map[index]=temp_list
                            
                        
                        
                        for axm in add_axoms:
                    
                            for seq in list_seq:
                            
                                axm[-1] = fun_utiles.expr_replace(axm[-1],eval("['_CE"+str(seq)+"']"),eval("['_CE"+str(seq)+"_"+str(local_count)+"']"))
                            
                            additional_axoms.append(axm)

                        
                    for index in soln_final_map:
                    
                        soln = eval(soln_final_map[index][0]+","+soln_final_map[index][1]+soln_final_map[index][2])
                    
                        equation_base = str(simplify(index).subs(simplify(soln[2]+"+1"),0))
                                        
                        if equations_map[index] in list_equations:
                        
                            list_equations.remove(equations_map[index])
                        
                        if basecase_map[equation_base] in list_equations:
                        
                            list_equations.remove(basecase_map[equation_base])
                        
                        del basecase_map[equation_base]
                    
                        del equations_map[index]
                    
                        for key in equations_map:
                            e = equations_map[key]
                            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
                        for key in basecase_map:
                            e = basecase_map[key]
                            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
                        
                        final_soln_list.append(soln)

                
                    return final_soln_list,additional_axoms       


                        
            
def constructSolution(soln_cons_map, soln_none_map, size):

    soln_main_map={}
    
    soln_main_end_map={}
    
    soln_main_final_map={}

    prve_value_map={}
                    
    prve_seq_map={}
    
    additional_axoms = [] 
    
    pre_CE=None
    
    for i in range(0,size):
                        
        for x in soln_cons_map:
            
            y = soln_cons_map[x][i]
            
            if x not in soln_main_map:
            
                
                list1=[]
                                
                list2=[]
                                
                cond=y[3][0]
                                
                                
                cond = fun_utiles.expr_replace(cond,eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                                
                                
                value = copy.deepcopy(y[7][4])
                                
                                    
                prve_value_map[y[4]]= y[6][-1]
                                
                                
                value = fun_utiles.expr_replace(value,eval("['_CV"+str(y[4])+"']"),y[6][-1])
                                
                                                                                                
                pre_value = copy.deepcopy(value)
                                
                                
                pre_value = fun_utiles.expr_replace(pre_value,eval("['"+y[1]+"']"),eval("['-',['_CE"+str(y[5])+"'],['1']]"))
                                
                                
                list1.append(cond)
                
                                
                list1.append(value)
                                
                soln_main_map[x]=list1
                                                
                list2.append(pre_CE)
                                
                list2.append(pre_value)
                                
                prve_seq_map[x]=list2
                
                for e1 in y[8]:
                    
                    e=copy.deepcopy(e1)
                                    
                    if e[0]=='s1':
                        
                        e[1][2] = fun_utiles.expr_replace(e[1][2],eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                                        
                    if e[0]=='s0':
                                        
                        e[1] = fun_utiles.expr_replace(e[1],eval("['-',['_CE"+str(y[5])+"'],['1']]"),eval("['_CE"+str(y[5])+"']"))
                                    
                                                                    
                    e[-1] = fun_utiles.expr_replace(e[-1],eval("['_CS"+str(y[5])+"']"),eval("['0']"))
                                    
                    if e not in additional_axoms:
                                        
                        additional_axoms.append(e)
                        
                pre_CE = str(y[5])
                
            else:


                cond=y[3][0]
        
                cond = fun_utiles.expr_replace(cond,eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                                
                value = copy.deepcopy(y[7][4])
                                
                prve_value_map[y[4]] = prve_seq_map[x][1]
                                
                value = fun_utiles.expr_replace(value,eval("['_CV"+str(y[4])+"']"),prve_seq_map[x][1])
                                
                pre_value = copy.deepcopy(value)
                                
                pre_value = fun_utiles.expr_replace(pre_value,eval("['"+y[1]+"']"),eval("['-',['_CE"+str(y[5])+"'],['1']]"))
                                
                                                            
                list1 = soln_main_map[x]
                                
                list1.append(cond)
                                
                list1.append(value)

                soln_main_map[x] = list1
                            
                list2 = []
                            
                list2.append(pre_CE)
                                
                list2.append(pre_value)
                                
                prve_seq_map[x]=list2
                            
                                
                for e1 in y[8]:
                    
                    e=copy.deepcopy(e1)
                                    
                    if e[0]=='s1':
                                        
                        e[1][2] = fun_utiles.expr_replace(e[1][2],eval("['"+y[1]+"']"),eval("['-',['"+y[1]+"'],['1']]"))
                                        
                    if e[0]=='s0':
                                        
                        e[1] = fun_utiles.expr_replace(e[1],eval("['-',['_CE"+str(y[5])+"'],['1']]"),eval("['_CE"+str(y[5])+"']"))
                                    
                                                                    
                    if pre_CE is not None:
                        
                        if y[5]!=pre_CE:
                                                    
                            e[-1] = fun_utiles.expr_replace(e[-1],eval("['_CS"+str(y[5])+"']"),eval("['_CE"+str(pre_CE)+"']"))
                                    
                    if e not in additional_axoms:
                                        
                        additional_axoms.append(e)
                        
        pre_CE = str(y[5])


    for x in soln_none_map:
                            
        y = soln_none_map[x]
                        
        init_soln=None
                        
        if init_soln is None:
                                    
            init_soln="['i2','0','"+y[7][2]+"',"+str(y[7][3])
            soln_main_end_map[x] = init_soln
                            
                                                        
        if x not in soln_main_map:
                                                            
            list1=[]
                                
            list2=[]
                                                                
                                
            value = copy.deepcopy(y[7][4])
                                
                                
            prve_value_map[y[4]]= y[6][-1]
                                
                                
            value = fun_utiles.expr_replace(value,eval("['_CV"+str(y[4])+"']"),y[6][-1])
                                
                                                                                                
            pre_value = copy.deepcopy(value)
                                
                                
            pre_value = fun_utiles.expr_replace(pre_value,eval("['"+y[1]+"']"),eval("['-',['_CE"+str(y[5])+"'],['1']]"))
                                
                                
            pre_CE = str(y[5])
                
                                
            list1.append(cond)
                                
            list1.append(value)
                                
            soln_main_map[x]=list1
                                
            list2.append(pre_CE)
                                
            list2.append(pre_value)
                                
            prve_seq_map[x]=list2

                                                                    
        else:    
                                
                                                                
            value = copy.deepcopy(y[7][4])
                                
            prve_value_map[y[4]] = prve_seq_map[x][1]
                                
            value = fun_utiles.expr_replace(value,eval("['_CV"+str(y[4])+"']"),prve_seq_map[x][1])
                                
            pre_value = copy.deepcopy(value)
                                
            pre_value = fun_utiles.expr_replace(pre_value,eval("['"+y[1]+"']"),eval("['-',['_CE"+str(y[5])+"'],['1']]"))
                                
            pre_CE = str(y[5])
                            
            list1 = soln_main_map[x]
                                                            
            list1.append(None)
                                
            list1.append(value)
            
            soln_main_map[x] = list1
                            
            list2 = []
                            
            list2.append(pre_CE)
                                
            list2.append(pre_value)
                                
            prve_seq_map[x]=list2

    #print '---------------------------'
    #print prve_value_map
    #print '---------------------------'
    for x in soln_main_map:
        
        list =[]
        
        for y in soln_main_map[x]:  
                                
            for z in prve_value_map:
                                                                        
                if y is not None:
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~1'
                    #print y
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~1'
                    y = fun_utiles.expr_replace(y,eval("['_CV"+str(z)+"']"),prve_value_map[z])
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~2'
                    #print y
                    #print '~~~~~~~~~~~~~~~~~~~~~~~~~~2'

                                    
            list.append(y)
                                
            soln_main_map[x] = list
                    
                                
    for x in prve_seq_map:
                            
        for z in prve_value_map:
                                                                        
            prve_seq_map[x][1] = fun_utiles.expr_replace(prve_seq_map[x][1],eval("['_CV"+str(z)+"']"),prve_value_map[z])
    
    for x in soln_main_map:
                
        soln_str=None
                    
        soln_str_end=None

        for i in range(0,len(soln_main_map[x])):
                    
            if i%2==1: 
                        
                if soln_str is  None:
                            
                    if soln_main_map[x][i-1] is not None:
                                
                        soln_str="['ite',"+str(soln_main_map[x][i-1])+","+str(soln_main_map[x][i])
                        soln_str_end="]"
                                
                    else:
                                
                        soln_str=str(soln_main_map[x][i])
                                
                else:
                            
                    if soln_main_map[x][i-1] is not None:
                                
                        soln_str+=",['ite',"+str(soln_main_map[x][i-1])+","+str(soln_main_map[x][i])
                        soln_str_end+="]"
                                
                    else:
                                
                        soln_str+=","+str(soln_main_map[x][i])

        soln_main_final_map[x] = eval(soln_main_end_map[x]+","+soln_str+soln_str_end+"]")

    return soln_main_final_map,additional_axoms






        
        
        
                 





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
        
        print '--------------'
        print status
        print '--------------'
        
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
                                        
                                            print '~~~~~~~~~~~~~~~~~~1'
                                            print stmt
                                            print '~~~~~~~~~~~~~~~~~~1'

                                        
                                        
                                            stmt = fun_utiles.expr_replace(stmt,eval("['"+'_CV'+str(e[6][x][-1][4])+"']"),prv_value)
                                            
                                            
                                            print '~~~~~~~~~~~~~~~~~~2'
                                            print stmt
                                            print '~~~~~~~~~~~~~~~~~~2'

                                        
                                        
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
                    
                        print '~~~~~~~~~~~~~~~~~~###############'
                    
                        print prv_value
                        
                        print '_CV'+str(len(list_sort)+1)
                        
                        print str(soln_start)+","+str(else_value)+soln_end+"]"
                        
                        print '~~~~~~~~~~~~~~~~~~###############'
                    
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
                                                            
                                #e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
                                e[4] = fun_utiles.expr_replace(e[4],soln[-2],soln[-1])

            
                            for x in basecase_map:
                                e = basecase_map[x]
                                
                                e[3] = fun_utiles.expr_replace(e[3],soln[-2],soln[-1])
                                #e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

                        
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
                
                none_cond,list_seq = constructNoneCondition(e)
                
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
        


def findTheTypeOfEq(e):
    
    if len(e)==2:
        
        type1=None
        
        type2=None
        
        for x in e:
            
            if e[x][3][3] is None:
                
                if type1 is None:
            
                    type1 = getTypeEquation(e[x][3][1])
                    
            else:
                
                if type2 is None:
                    
                    type2 = e[x][3][3]
                    
        return type1, type2
    
    else:
        
        type=None
        
        type2=None
        
        for x in e:
            
            if e[x][3][3] is None:
                
                temp_type=getTypeEquation(e[x][3][1])
                                
                if temp_type =='constant':
            
                    type2 = temp_type
                    
                    
                if type is None and temp_type is not None:
            
                    type = temp_type
                    
                elif type=='increasing' and temp_type=='decreasing':
                    
                    return None
                
                elif type=='constant' and temp_type=='decreasing':
                    
                    type = temp_type
                    
                elif type=='constant' and temp_type=='increasing':
                    
                    type = temp_type
                    
                elif temp_type=='constant' and type=='decreasing':
                    
                    type = 'decreasing'
                    
                elif temp_type=='constant' and type=='increasing':
                    
                    type = 'increasing'
                    
                elif temp_type=='increasing' and type=='increasing':
                    
                    type = 'increasing'
                    
                elif temp_type=='decreasing' and type=='decreasing':
                    
                    type = 'decreasing'

                    
                else:
                    
                    return None,None
            else:
                
                temp_type = e[x][3][3]
                               
                if type is None:
            
                    type = temp_type
                    
                elif type=='increasing' and temp_type=='decreasing':
                    
                    return None,None
                
                elif type=='constant' and temp_type=='decreasing':
                    
                    type = temp_type
                    
                elif type=='constant' and temp_type=='increasing':
                    
                    type = temp_type
                    
                elif temp_type=='constant' and type=='decreasing':
                    
                    type = 'decreasing'
                    
                elif temp_type=='constant' and type=='increasing':
                    
                    type = 'increasing'
                    
                elif temp_type=='increasing' and type=='increasing':
                    
                    type = 'increasing'
                    
                elif temp_type=='decreasing' and type=='decreasing':
                    
                    type = 'decreasing'


                else:
                    
                    return None,None

                
                
        return type,type2
                    

        
    
        
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
        
        list_seq=None
                
        local_count=1
                
        list_con_expression = new_e[6].keys()
        
        
        type1,type2 = findTheTypeOfEq(new_e[6])
        
        #print type1
        
        #print type2
        
        if type1 is None:
            
            
            return None,None
        
        elif type1=='constant' and (type2=='increasing' or type2=='decreasing'):
            
            
            soln,additional_axoims = getFunction2Constant(new_e, e, equations_map, basecase_map, list_equations)
                    
            if soln is not None:
                        
                return soln,additional_axoims
                    
            else:
                        
                return None,None
        
        elif type2=='constant' and (type1=='increasing' or type1=='decreasing'):
            
            
            soln,additional_axoims = getFunction2ConstantRev(new_e, e, equations_map, basecase_map, list_equations)
                    
            if soln is not None:
                        
                return soln,additional_axoims
                    
            else:
                        
                return None,None
            
        elif (type1=='increasing' and type2=='decreasing') or (type1=='decreasing' and type2=='increasing'):
            
                
            soln,additional_axoims = getFunctionCycle(new_e, e, equations_map, basecase_map, list_equations)
                                                
            if soln is not None:
                        
               return soln,additional_axoims
        
            else:
        
               return None,None
           
           
        elif (type1=='increasing' or type1=='decreasing') and type2!='constant':
            
            
            none_cond,list_seq = constructNoneCondition(new_e)
        
        
            
        
        
        soln=None
                
        local_count=1
                
        list_con_expression = new_e[6].keys()
        
        if none_cond is None:
            
            list_con_expression.remove(None)
                                
                
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
    
    solution_map={}

    
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
            
            cond = fun_utiles.expr_replace(cond,eval("['"+str(new_e[6][x][3][1][2])+"']"),eval("['-',['"+str(new_e[6][x][3][1][2])+"'],['1']]"))

            

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
                    
                    print 
                
                    if new_e[6][x][3][5][1][2][0]=='<=' or new_e[6][x][3][5][1][2][0]=='>=' or new_e[6][x][3][5][1][2][0]=='==':
                    
                        equation_sol= copy.deepcopy(new_e[6][x][3][5][1][2])
                        
                        equation_sol[0]='-'
                                                
                        solution = solve(simplify(FOL_translation.expr2string1(equation_sol)), simplify("_X"))

                        
                        if solution is not None and len(solution)==1 :
                            
                            var_map={}
                        
                            equation_list=[]
                            
                            constraint_list=[]
                        
                            equation_list.append(new_e[6][x][3][5])
                            
                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][5]))
                            
                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][6]))

                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][7]))

                        
                            FOL_translation.getEqVariFunDetails(equation_list,var_map)
                        
                            for vfact in var_map:
                            
                                vfacts.append(var_map[vfact])

                            equation_sol = fun_utiles.expr_replace(equation_sol,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['-',['_X'],['1']]"))
                            
                            status = fun_utiles.query2z3_update(constraint_list,FOL_translation.wff2z3_update(eval("['a',['==',"+str(new_e[6][x][3][5][1][1][2][2])+",['"+str(solution[0])+"']]]")),vfacts,'')
                            
                            if 'Successfully Proved' in status:
                                
                                solution_map[str(new_e[6][x][3][5][1][1][2][2])]="['"+str(solution[0])+"']"
                                
                            else:
                                additional_axoms.append(new_e[6][x][3][5])
                
                                additional_axoms.append(new_e[6][x][3][6])
                
                                additional_axoms.append(new_e[6][x][3][7])
                        else:
                            additional_axoms.append(new_e[6][x][3][5])
                
                            additional_axoms.append(new_e[6][x][3][6])
                
                            additional_axoms.append(new_e[6][x][3][7])

                            
                            
                        
                        #print new_e[6][x][3][1][2]
                        #print new_e[6][x][3][5][1][1][2][2]
                        
                        
                    elif new_e[6][x][3][6][1][0]=='<=' or new_e[6][x][3][6][1][0]=='>=' or new_e[6][x][3][6][1][0]=='==':
                    
                        equation_sol= copy.deepcopy(new_e[6][x][3][6][1])
                        
                        equation_sol[0]='-'
                        
                        equation_sol = fun_utiles.expr_replace(equation_sol,new_e[6][x][3][5][1][1][2][2],eval("['_X']"))
                        
                        solution = solve(simplify(FOL_translation.expr2string1(equation_sol)), simplify("_X"))
                        
                        
                        if solution is not None and len(solution)==1:
                            
                            var_map={}
                        
                            equation_list=[]
                            
                            constraint_list=[]
                            
                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][5]))
                            
                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][6]))

                            constraint_list.append(FOL_translation.wff2z3_update(new_e[6][x][3][7]))

                        
                            equation_list.append(new_e[6][x][3][5])
                        
                            FOL_translation.getEqVariFunDetails(equation_list,var_map)
                        
                            for vfact in var_map:
                            
                                vfacts.append(var_map[vfact])

                            equation_sol = fun_utiles.expr_replace(equation_sol,eval("['"+new_e[6][x][3][1][2]+"']"),eval("['-',['_X'],['1']]"))
                            
                            status = fun_utiles.query2z3_update(constraint_list,FOL_translation.wff2z3_update(eval("['a',['==',"+str(new_e[6][x][3][5][1][1][2][2])+",['"+str(solution[0])+"']]]")),vfacts,'')
                            
                            if 'Successfully Proved' in status:
                                
                                solution_map[str(new_e[6][x][3][5][1][1][2][2])]="['"+str(solution[0])+"']"
                                
                            else:
                                additional_axoms.append(new_e[6][x][3][5])
                
                                additional_axoms.append(new_e[6][x][3][6])
                
                                additional_axoms.append(new_e[6][x][3][7])
                        else:
                            additional_axoms.append(new_e[6][x][3][5])
                
                            additional_axoms.append(new_e[6][x][3][6])
                
                            additional_axoms.append(new_e[6][x][3][7])
                            
                            
                        
                        #print new_e[6][x][3][5][1][1][2][2]
                    else:
                    
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

                    soln = soln.replace('Black',"['ite',['==',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['0']]"+",['"+str(factor+1)+"']],['0']],['-',"+str(elseValue)+",['"+str(result1)+"']],"+str(elseValue)+"]")
                    soln = eval(soln)
                    
                    
                else:

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
                    
                    if factor==2:
                        
                        soln = soln.replace('Black',"['ite',"+"['==',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['1']]"+","+"['-',"+str(elseValue)+",['"+str(simplify(-1*result2))+"']]"+",['ite',"+"['==',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['2']]"+","+"['+',"+"['-',"+str(elseValue)+",['"+str(simplify(-1*result2))+"']]"+",['"+str(result1)+"']]"+","+str(elseValue)+"]]")
                        soln = eval(soln)
                        
                    elif factor>2:
                                                
                        part1 = "['+',"+"['+',"+"['-',"+str(elseValue)+",['"+str(simplify(-1*result2))+"']]"+",['"+str(result1)+"']]"+","+"['*',['-',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['2']],"+"['"+str(factor)+"']"+"]"+"]"
                        
                        part2 = "['ite',"+"['>',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['2']]"+","+part1+","+str(elseValue)+"]"
                        
                        soln = soln.replace('Black',"['ite',"+"['==',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['1']]"+","+"['-',"+str(elseValue)+",['"+str(simplify(-1*result2))+"']]"+",['ite',"+"['==',['%',"+"['-',['"+str(e[1][2])+"'],['"+CE_count+"']],"+"['"+str(factor+1)+"']],['2']]"+","+"['+',"+"['-',"+str(elseValue)+",['"+str(simplify(-1*result2))+"']]"+",['"+str(result1)+"']]"+","+part2+"]]")
                        soln = eval(soln)

                    
                    else:
                        
                        soln = soln.replace('Black',"['ite',['!=',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']],['0']],['-',"+str(elseValue)+","+"['*',"+"['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']]"+",['"+str(-1*result2)+"']]"+"],"+str(elseValue)+"]")
                        soln = eval(soln)

                    #print FOL_translation.expr2string1(soln[-1])
                    
                else:
                    
                    soln = soln.replace('Black',"['ite',['!=',['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']],['0']],['+',"+str(elseValue)+","+"['*',"+"['%',"+"['+',['-',['"+str(e[1][2])+"'],['"+CE_count+"']],['1']]"+",['"+str(factor+1)+"']]"+",['"+str(result2)+"']]"+"],"+str(elseValue)+"]")
                    soln = eval(soln)
                    
            
            
            if soln is not None:
                
                
                if len(solution_map)>0:
                    
                    for key in solution_map:
                    
                        soln[-1] = fun_utiles.expr_replace(soln[-1],eval(key),eval(solution_map[key]))
                

                
                if equations_map[e[0]] in list_equations:
                    
                    list_equations.remove(equations_map[e[0]])
            
                if basecase_map[equation_base] in list_equations:
                                
                    list_equations.remove(basecase_map[equation_base])

                
                del basecase_map[equation_base]
        
                del equations_map[e[0]]
        
                for x in equations_map:
                    e = equations_map[x]
                    e[4] = fun_utiles.expr_replace(e[4],soln[-2],soln[-1])         
                    #e[4] = fun_utiles.expr_replace(e[4],e[6][x][-1][1][3],e[6][x][-1][1][4])
            
                for x in basecase_map:
                    e = basecase_map[x]
                    e[3] = fun_utiles.expr_replace(e[3],soln[-2],soln[-1])
                    #e[3] = fun_utiles.expr_replace(e[3],e[6][x][-1][1][3],e[6][x][-1][1][4])

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
                        
            
            cond1 = copy.deepcopy(cond)
            
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
                
                    
                    equation_list = []
                
                    constraint_list =[]
                    
                                    
                    cond1 = fun_utiles.expr_replace(cond1,eval("['"+e[1][2]+"']"),eval("['0']"))
                
                    temp_cond = eval("['a',"+str(cond1)+"]")
                
                    equation_list.append(temp_cond)
                
                    constraint_list.append(FOL_translation.wff2z3_update(temp_cond))
                
                    var_map={}
                
                    FOL_translation.getEqVariFunDetails(equation_list,var_map)
                
                    vfacts=[]
                
                    for vfact in var_map:
                        vfacts.append(var_map[vfact])

                    status = fun_utiles.query2z3_update(constraint_list,None,vfacts,'')
                    
                    
                    if 'Counter Example' in status and '[_f = [else -> Var(0)]]' in status:
                    
                        soln=eval("['"+new_e[6][x][3][1][0]+"','"+new_e[6][x][3][1][1]+"','"+new_e[6][x][3][1][2]+"',"+str(new_e[6][x][3][1][3])+","+str(e_base[3])+"]")
                
                
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
            
            cond_else = fun_utiles.expr_complement(cond_else)
                        
            value_else = fun_utiles.expr_replace(value_else,eval("['"+'_CV'+str(counter_else)+"']"),e_base[3])
            
            cond_else = fun_utiles.expr_replace(cond_else,eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),value_else)
            
            #base_update = "[''"
            
            #copy.deepcopy(e_base[3])
            
            #cond_else = fun_utiles.expr_replace(cond_else,eval("['"+'_CV'+str(new_e[6][x][3][4])+"']"),e_base[3])
            
            
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







def solveGroupConstantType(group_list, equations_map, basecase_map, list_equations):
        
    
    soln_map = {}
    
    final_soln_list = []
    
    main_map = {}
    
    var=None
    
    for x in group_list:
        
        
        for y in x[6]:
            
            if y in main_map.keys():
                
                list1 = main_map[y]
                
                x[6][y].append(x[1])
                
                list1.append(x[6][y])
                
            else:
                
                list1=[]
                
                x[6][y].append(x[1])
                
                list1.append(x[6][y])
                
                main_map[y] = list1
                 
    
    for x in main_map:
        
        list1 = main_map[x]
        
        a_list=[]
        
        
        for y in list1:
            
            new_e=copy.deepcopy(y[-1])
            
            equation_base = str(simplify(FOL_translation.expr2string1(new_e[3])).subs(simplify(str(new_e[2])+"+1"),0))
    
            e_base = basecase_map[equation_base]
            
            new_e[4]= y[1]

            a_list.append(e_base)
            
            a_list.append(new_e)
    
        res_equ,soln = rec_solver_group(a_list)
                
        list1.append(soln)
        
        if len(res_equ)>0:
            
            return None
        
        
    
    for x in main_map:
        
        list1 = main_map[x]
        
        for y in list1[-1]:
            
            if y in soln_map.keys():
                
                soln_list=soln_map[y]
                
                if list1[0][0] is not None:
            
                    soln_list.append("['ite',"+str(list1[0][0])+","+str(list1[-1][y][-1]))

                    
                else:
                
                    soln_list.append(str(list1[-1][y][-1]))

            else:
                soln_list=[]
                
                soln_list.append("['"+list1[-1][y][0]+"',"+list1[-1][y][1]+",'"+list1[-1][y][2]+"',"+str(list1[-1][y][3]))
                
                var=list1[-1][y][2]
                
                if list1[0][0] is not None:
            
                    soln_list.append("['ite',"+str(list1[0][0])+","+str(list1[-1][y][-1]))
                    
                else:
                
                    soln_list.append(str(list1[-1][y][-1]))
                    
                soln_map[y]=soln_list


    for x in soln_map:
        
        soln=None
        solnend=None
        
        for y in soln_map[x]:
            
            if soln is None:
                soln=y
                solnend="]"
            else:
                if "ite" in y:
                    soln+=","+y
                    solnend=solnend+"]"
                else:
                    solnend=y+solnend
                    
        
        
        soln = eval(soln+","+solnend)
        
        equation_base = str(simplify(x).subs(simplify(str(var)+"+1"),0))
        
        if equations_map[x] in list_equations:
            
            list_equations.remove(equations_map[x])
            
        if basecase_map[equation_base] in list_equations:
            list_equations.remove(basecase_map[equation_base])

                
        del basecase_map[equation_base]
        
        del equations_map[x]
        
        for x in equations_map:
            e = equations_map[x]
            e[4] = fun_utiles.expr_replace(e[4],soln[3],soln[4])
            
        for x in basecase_map:
            e = basecase_map[x]
            e[3] = fun_utiles.expr_replace(e[3],soln[3],soln[4])
        
        if final_soln_list is None:
            
            soln_list=[]
            final_soln_list.append(soln)
            
        else:
            
            final_soln_list.append(soln)

    return final_soln_list
        
    







def solvePeriodicType(e, equations_map, basecase_map, list_equations):
    
    equation_base = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),0))
    
    equation_left = str(simplify(e[0]).subs(simplify(str(e[1][2])+"+1"),simplify(str(e[1][2]))))
    
    e_base = basecase_map[equation_base]
    
    new_expr=copy.deepcopy(e[1][3])
    
    new_expr = fun_utiles.expr_replace(new_expr,eval("['+',"+"['"+e[1][2]+"'],['1']]"),eval("['"+e[1][2]+"']"))
    
    term_list=[]
    
    for x in e[6]:
        if e[6][x][2]=='Periodic':
            
            list1=[]
            
            list1.append(e[6][x][4])
            
            list1.append(e[6][x][3])

            coeff_expr = simplify(FOL_translation.expr2string1(e[6][x][1]))
    
            term = simplify(equation_left)
            
            coeff_const = coeff_expr.coeff(term)
            
            if str(coeff_const)=='1':
                
                result = coeff_expr - coeff_const*simplify(equation_left)
                
                list1.append(result)
                
                term_list.append(list1)
                
        elif e[6][x][2]==None:
            
            list1=[]
            
            coeff_expr = simplify(FOL_translation.expr2string1(e[6][x][1]))
    
            term = simplify(equation_left)
            
            coeff_const = coeff_expr.coeff(term)
            
            if str(coeff_const)=='1':
                
                result = coeff_expr - coeff_const*simplify(equation_left)
                
                list1.append(result)
                
                term_list.append(list1)

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
            
            #stmt_update="['+',['+',"+str(e_base[3])+",['*',"+str(stmt_update1)+",['-',['"+var+"'],['/',['"+var+"'],"+str(initer_update)+"]]]],"+"['*',['/',['"+var+"'],"+str(initer_update)+"],"+str(stmt_update2)+"]]"
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
            
        else:
            
            utiles_translation.resetGlobal()
            

            statement_temp = utiles_translation.createASTStmt(str(term_list[1][1]))
            initer_update = utiles_translation.expressionCreator_C(statement_temp)
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[1][2]))
            stmt_update1 = utiles_translation.expressionCreator_C(statement_temp)
            
            
            utiles_translation.resetGlobal()
            statement_temp = utiles_translation.createASTStmt(str(term_list[0][0]))
            stmt_update2 = utiles_translation.expressionCreator_C(statement_temp)
            
            
            stmt_update="['+',['+',"+str(e_base[3])+",['*',"+str(stmt_update1)+",['-',['"+var+"'],['/',['"+var+"'],"+str(initer_update)+"]]]],"+"['*',['/',['"+var+"'],"+str(initer_update)+"],"+str(stmt_update2)+"]]"
            #stmt_update="['+',['+',"+str(e_base[3])+",['*',"+str(stmt_update2)+",['-',['"+var+"'],['/',['"+var+"'],"+str(initer_update)+"]]]],"+"['*',['/',['"+var+"'],"+str(initer_update)+"],"+str(stmt_update1)+"]]"
            
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
                                result = getWolframalphaCache(righthandstmt,righthandstmt_base)
                                
                                if result is None:
                                    
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
					result=fun_utiles.translatepowerToFun(str(result))
                                        
				expression=str(str(term2)+"="+str(result))
                                utiles_translation.resetGlobal()
                                statement_temp = utiles_translation.createASTStmt(expression)
                                
                                closed_form_soln = utiles_translation.construct_expressionC(e1[1],e1[2],expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.lvalue))),expr_replace_power(eval(utiles_translation.expressionCreator_C(statement_temp.rvalue))))
				#tree = p.parse_expression(expression)
				#closed_form_soln=construct_expression(tree,e1[1],e1[2])
                                
			
	#return None
	return closed_form_soln




def getWolframalphaCache(expression,base_expression):
    
	#cache_map={'(n + 1)**3 + T(n)':['0','(n**2*(n + 1)**2)/2'],'(i + n + 1)**3 + T(n)':['N_1','N_1 + (n*(n + (1 + 2*i) )*(- (2 - 2*i)  + n*(n + (1 + 2*i) )))/4']}
	cache_map={'T(n) - 1':['N_1','N_1 - n'],'n**2 + T(n)':['N_1','N_1 + n*(n - 1)*(2*n - 1)/6'],'(n+1)**2 + T(n)':['N_1','N_1 + n*(n + 1)*(2*n + 1)/6'],'n**3 + T(n)':['N_1','N_1+(n**2*(n - 1)**2)/4'],'(n + 1)**3 + T(n)':['N_1','N_1+(n**2*(n + 1)**2)/4'],'n**4 + T(n)':['N_1','N_1+n*(n*n*(3*n*(2*n-5)+10)-1)/30'],'(n + 1)**4 + T(n)':['N_1','N_1+n*(n+1)*(2*n+1)*(3*n*(n+1)-1)/30'],'(n + 1)**5 + T(n)':['N_1','N_1+(n)**2*(2*n*(n+1)-1)*(n+1)**2/12'], 'n**5 + T(n)':['N_1','N_1+(n+1)**2*(2*(n-1)*n-1)*n**2/12'],'n**6 + T(n)':['N_1','N_1 + (6*n**7-21*n**6+21*n**5-7*n**3+n)/42'],'(n+1)**6 + T(n)':['N_1','N_1 + (6*n**7+21*n**6+21*n**5-7*n**3+n)/42'],'n**7 + T(n)':['N_1','N_1 + (3*n**8-12*n**7+14*n**6-7*n**4+2*n**2)/24'],'(n+1)**7 + T(n)':['N_1','N_1 + (3*n**8+12*n**7+14*n**6-7*n**4+2*n**2)/24'],'n**8 + T(n)':['N_1','N_1 + (10*n**9-45*n**8+60*n**7-42*n**5+20*n**3-3*n)/90'],'(n+1)**8 + T(n)':['N_1','N_1 + (10*n**9+45*n**8+60*n**7-42*n**5+20*n**3-3*n)/90'],'n**9 + T(n)':['N_1','N_1 + ((2*(n-5)*n+15)*n**6-14*n**6+10*n**2-3)/20'],'(n+1)**9 + T(n)':['N_1','N_1 + ((2*(n+5)*n+15)*n**6-14*n**6+10*n**2-3)/20'],'n**10 + T(n)':['N_1','N_1 + n*(6*n**10-33*n**9+55*n**8-66*n**6+66*n**4-33*n**2+5)/66'],'(n+1)**10 + T(n)':['N_1','N_1 + n*(6*n**10-33*n**9+55*n**8-66*n**6+66*n**4-33*n**2+5)/66']}
    
	for element in cache_map.keys():
		if simplify(element)==simplify(expression):
                        try:
                            
                            return simplify(cache_map[element][1]).subs(simplify(cache_map[element][0]),simplify(base_expression))
                            
                        except ValueError:
                            return None
			
	return None




"""
Recurrences Solving Module by 
#Add by Pritom Rajkhowa

"""
    
def solve_rec_m(e1,list1):
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
	if list1 is not None:
            for e2 in list1: 
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



def rec_solver_group(a):
    constant_fun_map={}
    equation_map={}
    base_map={}
    final_solution_map={}
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
        for xx in solution_map.keys():
            final_solution_map[xx]=solution_map[xx]

	if len(equation_map)==0 or len(solution_map)==0:
            break
        
    return a,final_solution_map



#solve_recurrence(rec_equ,var)
