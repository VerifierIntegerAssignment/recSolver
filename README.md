# recSolver

Recurrences Equations Solver(recSolver) is a framework that solve various kinds of recurrences relations. recSolver has the power to solve various kinds of recurrences like linear or non-linear, homogeneous or non-homogeneous, conditional and mutually recursive.


### Awards & Achievements

## Publications


# See below for system requirements, installation, usage, and everything else.

### Support

* If something is not working or missing, open an [issue](https://github.com/VerifierIntegerAssignment/VerifierIntegerAssignment.github.io/issues).

* As a last resort, send mail to 
  [Pritom Rajkhowa](mailto:pritom.rajkhowa@gmail.com), [Fangzhen Lin](mailto:flin@cs.ust.hk), or both.





### System Requirements and Installation

In practice we have run recSolver on standard Ubuntu 16.04 LTS distribution. recSolver is provided as a set of binaries and libraries for
Ubuntu 16.04 LTS distribution. 

#### Download 


##### Clone over HTTPS:

 $ git clone https://github.com/VerifierIntegerAssignment/recSolver.git
 
 #### Running recSolver


recSolver framework is run by using the `recSolver.py` tool in the recSolver directory.
For a given input recurrence equations, the tool tried to find the closed from solution(s). 

#### Running Command

PATH_TO_recSolver/recSolver.py equation/equations variable



#### Output :
```
-DISPLAY CLOSED FORM SOLUTION IF FRAMAEWORK ABLE TO FIND CLOSED FORM SOLUTION OF INPUT EQUATION(S)
```

### Using The recSolver

Next, we illustrate how to use recSolverto find the closed form solution of input equation(s)

#### How to run this Example 
```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=X(_n1)+1;Y(_n1+1)=X(_n1)+Y(_n1)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (A+_n1)
Y(_n1) = ((((((2*A)*_n1)+(2*B))-_n1)+(_n1**2))/2)

ADDITIONAL AXIOMS
No Additional AXIOMS

```




#### Example 2 
```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
Z(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+F)
X(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+D)
Y(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+H)

ADDITIONAL AXIOMS
No Additional AXIOMS
```

#### Example 3 

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;M(0)=j;M(_n1+1)=X(_n1)+M(_n1);X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
M((_n1+1)) = (((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+D)+M(_n1))

CLOSED FORM SOLUTION
Z(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+F)
X(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+D)
Y(_n1) = ((((power(3,_n1)*power(l,_n1))*(C+(A+B)))+((F+(D+H))+((l*(1-(power(3,_n1)*power(l,_n1))))/(1-(3*l)))))+H)

ADDITIONAL AXIOMS
No Additional AXIOMS

```
#### Example 4 

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+F"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
X((_n1+1)) = ((((l*X(_n1))+(m*Y(_n1)))+(n*Z(_n1)))+D)
Y((_n1+1)) = ((((l*X(_n1))+(m*Y(_n1)))+(n*Z(_n1)))+H)
Z((_n1+1)) = ((((l*X(_n1))+(m*Y(_n1)))+(n*Z(_n1)))+F)

CLOSED FORM SOLUTION
No Solution

ADDITIONAL AXIOMS
No Additional AXIOMS


```



#### Example 5

```python
$recSolver/recSolver.py  "X(0)=A;X(_n1+1)=ite(B>0,X(_n1)+1,ite(C>0,X(_n1)+2,X(_n1)))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((C>0),(A+(2*_n1)),ite((B>0),(A+_n1),A))

ADDITIONAL AXIOMS
No Additional AXIOMS



```

#### Example 6

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(_n1==1,1,(_n1+1)*X(_n1))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = factorial(_n1)

ADDITIONAL AXIOMS
No Additional AXIOMS



```

#### Example 7

```python
$recSolver/recSolver.py  "X(0)=0;X(_n1+1)=ite(_n1==1,1,(1+X(_n1)));Y(0)=1;Y(_n1+1)=ite(_n1==1,1,(_n1+1)*Y(_n1))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = _n1
Y(_n1) = factorial(_n1)

ADDITIONAL AXIOMS
No Additional AXIOMS




```

#### Example 8

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ((1+(A*(_n1-(_n1/5))))+((_n1/5)*B))

ADDITIONAL AXIOMS
No Additional AXIOMS




```



#### Example 9

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(_n1%5==0,X(_n1)+A,X(_n1)+B);Y(0)=1;Y(_n1+1)=ite(C>0,Y(_n1)+A,Y(_n1)+B)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ((1+(A*(_n1-(_n1/5))))+((_n1/5)*B))
Y(_n1) = ite((C>0),((A*_n1)+1),((B*_n1)+1))

ADDITIONAL AXIOMS
No Additional AXIOMS




```


#### Example 10

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1)+5,X(_n1))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((1+(5*_n1))%2)!=0),(1+(5*_n1)),(1+(5*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(5*_n1))%2)!=0)
(((1+(5*_CE1))%2)==0)
(0<=_CE1)





```


#### Example 11

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((1+(5*_n1))%2)==0),(1+(5*_n1)),(1+(5*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(5*_n1))%2)==0)
(((1+(5*_CE1))%2)!=0)
(0<=_CE1)




```


#### Example 12

```python
$recSolver/recSolver.py  "X(0)=2;X(_n1+1)=ite(X(_n1)%2==0,X(_n1),X(_n1)+5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((1+(5*_n1))%2)==0),(1+(5*_n1)),(1+(5*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(5*_n1))%2)==0)
(((1+(5*_CE1))%2)!=0)
(0<=_CE1)




```

#### Example 13

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1)+5,X(_n1)-5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (1+(5*_n1))

ADDITIONAL AXIOMS
No Additional AXIOMS




```


#### Example 14

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite(((1+(5*_n1))<A),(1+(5*_n1)),ite(((((_n1-_CE2)+0)%2)==0),((1+(5*_CE2))-5),(1+(5*_CE2))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE2)) -> ((1+(5*(_n1-1)))<A)
((1+(5*(_CE2-1)))>=A)
(0<=_CE2)




```


#### Example 15

```python
$recSolver/recSolver.py  "X(0)=10;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((10+(5*_n1))-(5*_n1))>A),(10+(5*_n1)),(10+(5*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((10+(5*_n1))-(5*_n1))>A)
(((10+(5*_CE1))-(5*_CE1))<=A)
(0<=_CE1)





```


#### Example 16

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+5,X(_n1)-15)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite(((1+(5*_n1))<A),(1+(5*_n1)),ite(((((_n1-_CE2)+0)%4)==0),((1+(5*_CE2))-15),(((1+(5*_CE2))-15)+(((_n1-_CE2)%4)*5))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE2)) -> ((1+(5*(_n1-1)))<A)
((1+(5*(_CE2-1)))>=A)
(0<=_CE2)






```




#### Example 17

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-5,X(_n1)+15)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((1+(15*_n1))-(5*_n1))>A),(1+(15*_n1)),(1+(15*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(15*_n1))-(5*_n1))>A)
(((1+(15*_CE1))-(5*_CE1))<=A)
(0<=_CE1)






```




#### Example 18

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+15,X(_n1)-5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite(((1+(15*_n1))<A),(1+(15*_n1)),ite(((((_n1-_CE2)+1)%4)!=0),((1+(15*_CE2))-((((_n1-_CE2)+1)%4)*5)),(1+(15*_CE2))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE2)) -> ((1+(15*(_n1-1)))<A)
((1+(15*(_CE2-1)))>=A)
(0<=_CE2)






```



#### Example 19

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)>A,X(_n1)-15,X(_n1)+5)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((((1+(5*_n1))-(15*_n1))>A),(1+(5*_n1)),(1+(5*_CE1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(5*_n1))-(15*_n1))>A)
(((1+(5*_CE1))-(15*_CE1))<=A)
(0<=_CE1)






```


#### Example 20

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)>0,X(_n1)+5,X(_n1))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (1+(5*_n1))

ADDITIONAL AXIOMS
No Additional AXIOMS






```


#### Example 21

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(_n1<50,X(_n1)+1,ite(_n1<70,X(_n1)+2,ite(_n1<90,X(_n1)+3,X(_n1))))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite(((_n1-1)<50),(1+_n1),ite(((_n1-1)<70),((1+(51-1))+(2*_n1)),ite(((_n1-1)<90),(((1+(51-1))+(2*(71-1)))+(3*_n1)),(((1+(51-1))+(2*(71-1)))+(3*(91-1))))))

ADDITIONAL AXIOMS
No Additional AXIOMS
```


#### Example 22

```python

$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,X(_n1)+2)"  "_n1"

```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (ite(!(((1+(_n1-1))<A)),(1+(2*_n1)),((1+(2*(_CE1_2-1)))+_n1)) or ite(((1+(_n1-1))<A),(1+_n1),((1+(_CE2_3-1))+(2*_n1))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1_2)) -> !(((1+(_n1-1))<A))
((1+(_CE1_2-1))<A)
(0<=_CE1_2)
((_CE1_2<=_n1) and (_n1<_CE2_2)) -> (((1+(2*(_CE1-1)))+(_n1-1))<A)
(((1+(2*(_CE1-1)))+(_CE2_2-1))>=A)
(0<=_CE2_2)
(_CE1_2<_CE2_2)
((0<=_n1) and (_n1<_CE2_3)) -> ((1+(_n1-1))<A)
((1+(_CE2_3-1))>=A)
(0<=_CE2_3)
(0<_CE2_3)
((_CE2_3<=_n1) and (_n1<_CE1_3)) -> !((((1+(_CE2_3-1))+(_n1-1))<A))
(((1+(_CE2_3-1))+(_CE1_3-1))<A)
(0<=_CE1_3)
(2<=_CE1_3)

```

#### Example 23

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(X(_n1)<A,X(_n1)+1,X(_n1)+2)"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (ite(((_n1-1)<A),(1+_n1),((1+(_CE1_2-1))+(2*_n1))) or ite(!(((_n1-1)<A)),(1+(2*_n1)),((1+(2*(_CE2_3-1)))+_n1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1_2)) -> ((_n1-1)<A)
((_CE1_2-1)>=A)
(0<=_CE1_2)
(0<_CE1_2)
((_CE1_2<=_n1) and (_n1<_CE2_2)) -> !(((_n1-1)<A))
((_CE2_2-1)<A)
(0<=_CE2_2)
(1<=_CE2_2)
((0<=_n1) and (_n1<_CE2_3)) -> !(((_n1-1)<A))
((_CE2_3-1)<A)
(0<=_CE2_3)
((_CE2_3<=_n1) and (_n1<_CE1_3)) -> ((_n1-1)<A)
((_CE1_3-1)>=A)
(0<=_CE1_3)
(_CE2_3<_CE1_3)

```



#### Example 24

```python
$recSolver/recSolver.py  "X(0)=1;X(_n1+1)=ite(_n1<A,X(_n1)+1,ite(_n1<B,X(_n1)+2,ite(_n1<C,X(_n1)+3,X(_n1))))"  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (((((((((((((((((((((((ite(((_n1-1)<A),(1+_n1),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(_CE1_2-1)),ite(((_n1-1)<C),((1+(_CE1-1))+(3*_n1)),(((1+(_CE1-1))+(3*(_CE3_2-1)))+(2*_n1))))) or ite(((_n1-1)<A),(1+_n1),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(_CE1_3-1)),ite(((_n1-1)<B),((1+(_CE1-1))+(2*_n1)),(((1+(_CE1-1))+(2*(_CE4_3-1)))+(3*_n1)))))) or ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<C),((1+(_CE1_4-1))+(3*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(_CE1-1))+(3*(_CE3_4-1))),(((1+(_CE1-1))+(3*(_CE3-1)))+(2*_n1)))))) or ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<C),((1+(_CE1_5-1))+(3*_n1)),ite(((_n1-1)<B),(((1+(_CE1-1))+(3*(_CE3_5-1)))+(2*_n1)),(((1+(_CE1-1))+(3*(_CE3-1)))+(2*(_CE4_5-1))))))) or ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<B),((1+(_CE1_6-1))+(2*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(_CE1-1))+(2*(_CE4_6-1))),(((1+(_CE1-1))+(2*(_CE4-1)))+(3*_n1)))))) or ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<B),((1+(_CE1_7-1))+(2*_n1)),ite(((_n1-1)<C),(((1+(_CE1-1))+(2*(_CE4_7-1)))+(3*_n1)),(((1+(_CE1-1))+(2*(_CE4-1)))+(3*(_CE3_7-1))))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<C),((1+(_CE1_8-1))+(3*_n1)),(((1+(_CE1-1))+(3*(_CE3_8-1)))+(2*_n1)))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<A),(1+_n1),ite(((_n1-1)<B),((1+(_CE1_9-1))+(2*_n1)),(((1+(_CE1-1))+(2*(_CE4_9-1)))+(3*_n1)))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<A),((1+(3*(_CE3_10-1)))+_n1),(((1+(3*(_CE3-1)))+(_CE1_10-1))+(2*_n1)))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<B),((1+(3*(_CE3_11-1)))+(2*_n1)),(((1+(3*(_CE3-1)))+(2*(_CE4_11-1)))+_n1))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<A),((1+(2*(_CE4_12-1)))+_n1),(((1+(2*(_CE4-1)))+(_CE1_12-1))+(3*_n1)))))) or ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),1,ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<C),((1+(2*(_CE4_13-1)))+(3*_n1)),(((1+(2*(_CE4-1)))+(3*(_CE3_13-1)))+_n1))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<A),((1+(3*(_CE3_14-1)))+_n1),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(3*(_CE3-1)))+(_CE1_14-1)),(((1+(3*(_CE3-1)))+(_CE1-1))+(2*_n1)))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<A),((1+(3*(_CE3_15-1)))+_n1),ite(((_n1-1)<B),(((1+(3*(_CE3-1)))+(_CE1_15-1))+(2*_n1)),(((1+(3*(_CE3-1)))+(_CE1-1))+(2*(_CE4_15-1))))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(3*(_CE3_16-1))),ite(((_n1-1)<A),((1+(3*(_CE3-1)))+_n1),(((1+(3*(_CE3-1)))+(_CE1_16-1))+(2*_n1)))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(3*(_CE3_17-1))),ite(((_n1-1)<B),((1+(3*(_CE3-1)))+(2*_n1)),(((1+(3*(_CE3-1)))+(2*(_CE4_17-1)))+_n1))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<B),((1+(3*(_CE3_18-1)))+(2*_n1)),ite(((_n1-1)<A),(((1+(3*(_CE3-1)))+(2*(_CE4_18-1)))+_n1),(((1+(3*(_CE3-1)))+(2*(_CE4-1)))+(_CE1_18-1)))))) or ite(((_n1-1)<C),(1+(3*_n1)),ite(((_n1-1)<B),((1+(3*(_CE3_19-1)))+(2*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(3*(_CE3-1)))+(2*(_CE4_19-1))),(((1+(3*(_CE3-1)))+(2*(_CE4-1)))+_n1))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<A),((1+(2*(_CE4_20-1)))+_n1),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(2*(_CE4-1)))+(_CE1_20-1)),(((1+(2*(_CE4-1)))+(_CE1-1))+(3*_n1)))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<A),((1+(2*(_CE4_21-1)))+_n1),ite(((_n1-1)<C),(((1+(2*(_CE4-1)))+(_CE1_21-1))+(3*_n1)),(((1+(2*(_CE4-1)))+(_CE1-1))+(3*(_CE3_21-1))))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(2*(_CE4_22-1))),ite(((_n1-1)<A),((1+(2*(_CE4-1)))+_n1),(((1+(2*(_CE4-1)))+(_CE1_22-1))+(3*_n1)))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),(1+(2*(_CE4_23-1))),ite(((_n1-1)<C),((1+(2*(_CE4-1)))+(3*_n1)),(((1+(2*(_CE4-1)))+(3*(_CE3_23-1)))+_n1))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<C),((1+(2*(_CE4_24-1)))+(3*_n1)),ite(((_n1-1)<A),(((1+(2*(_CE4-1)))+(3*(_CE3_24-1)))+_n1),(((1+(2*(_CE4-1)))+(3*(_CE3-1)))+(_CE1_24-1)))))) or ite(((_n1-1)<B),(1+(2*_n1)),ite(((_n1-1)<C),((1+(2*(_CE4_25-1)))+(3*_n1)),ite(!(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B))),((1+(2*(_CE4-1)))+(3*(_CE3_25-1))),(((1+(2*(_CE4-1)))+(3*(_CE3-1)))+_n1)))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1_2)) -> ((_n1-1)<A)
((_CE1_2-1)>=A)
(0<=_CE1_2)
(0<_CE1_2)
((_CE1_2<=_n1) and (_n1<_CE2_2)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_2-1)<A) and ((_CE2_2-1)<C)) and ((_CE2_2-1)<B))
(0<=_CE2_2)
(1<=_CE2_2)
((_CE2_2<=_n1) and (_n1<_CE3_2)) -> ((_n1-1)<C)
((_CE3_2-1)>=C)
(0<=_CE3_2)
(_CE2_2<_CE3_2)
((_CE3_2<=_n1) and (_n1<_CE4_2)) -> ((_n1-1)<B)
((_CE4_2-1)>=B)
(0<=_CE4_2)
(_CE3_2<_CE4_2)
((0<=_n1) and (_n1<_CE1_3)) -> ((_n1-1)<A)
((_CE1_3-1)>=A)
(0<=_CE1_3)
(0<_CE1_3)
((_CE1_3<=_n1) and (_n1<_CE2_3)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_3-1)<A) and ((_CE2_3-1)<C)) and ((_CE2_3-1)<B))
(0<=_CE2_3)
(1<=_CE2_3)
((_CE2_3<=_n1) and (_n1<_CE4_3)) -> ((_n1-1)<B)
((_CE4_3-1)>=B)
(0<=_CE4_3)
(_CE2_3<_CE4_3)
((_CE4_3<=_n1) and (_n1<_CE3_3)) -> ((_n1-1)<C)
((_CE3_3-1)>=C)
(0<=_CE3_3)
(_CE4_3<_CE3_3)
((0<=_n1) and (_n1<_CE1_4)) -> ((_n1-1)<A)
((_CE1_4-1)>=A)
(0<=_CE1_4)
(0<_CE1_4)
((_CE1_4<=_n1) and (_n1<_CE3_4)) -> ((_n1-1)<C)
((_CE3_4-1)>=C)
(0<=_CE3_4)
(_CE1_4<_CE3_4)
((_CE3_4<=_n1) and (_n1<_CE2_4)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_4-1)<A) and ((_CE2_4-1)<C)) and ((_CE2_4-1)<B))
(0<=_CE2_4)
(3<=_CE2_4)
((_CE2_4<=_n1) and (_n1<_CE4_4)) -> ((_n1-1)<B)
((_CE4_4-1)>=B)
(0<=_CE4_4)
(_CE2_4<_CE4_4)
((0<=_n1) and (_n1<_CE1_5)) -> ((_n1-1)<A)
((_CE1_5-1)>=A)
(0<=_CE1_5)
(0<_CE1_5)
((_CE1_5<=_n1) and (_n1<_CE3_5)) -> ((_n1-1)<C)
((_CE3_5-1)>=C)
(0<=_CE3_5)
(_CE1_5<_CE3_5)
((_CE3_5<=_n1) and (_n1<_CE4_5)) -> ((_n1-1)<B)
((_CE4_5-1)>=B)
(0<=_CE4_5)
(_CE3_5<_CE4_5)
((_CE4_5<=_n1) and (_n1<_CE2_5)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_5-1)<A) and ((_CE2_5-1)<C)) and ((_CE2_5-1)<B))
(0<=_CE2_5)
(4<=_CE2_5)
((0<=_n1) and (_n1<_CE1_6)) -> ((_n1-1)<A)
((_CE1_6-1)>=A)
(0<=_CE1_6)
(0<_CE1_6)
((_CE1_6<=_n1) and (_n1<_CE4_6)) -> ((_n1-1)<B)
((_CE4_6-1)>=B)
(0<=_CE4_6)
(_CE1_6<_CE4_6)
((_CE4_6<=_n1) and (_n1<_CE2_6)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_6-1)<A) and ((_CE2_6-1)<C)) and ((_CE2_6-1)<B))
(0<=_CE2_6)
(4<=_CE2_6)
((_CE2_6<=_n1) and (_n1<_CE3_6)) -> ((_n1-1)<C)
((_CE3_6-1)>=C)
(0<=_CE3_6)
(_CE2_6<_CE3_6)
((0<=_n1) and (_n1<_CE1_7)) -> ((_n1-1)<A)
((_CE1_7-1)>=A)
(0<=_CE1_7)
(0<_CE1_7)
((_CE1_7<=_n1) and (_n1<_CE4_7)) -> ((_n1-1)<B)
((_CE4_7-1)>=B)
(0<=_CE4_7)
(_CE1_7<_CE4_7)
((_CE4_7<=_n1) and (_n1<_CE3_7)) -> ((_n1-1)<C)
((_CE3_7-1)>=C)
(0<=_CE3_7)
(_CE4_7<_CE3_7)
((_CE3_7<=_n1) and (_n1<_CE2_7)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_7-1)<A) and ((_CE2_7-1)<C)) and ((_CE2_7-1)<B))
(0<=_CE2_7)
(3<=_CE2_7)
((0<=_n1) and (_n1<_CE2_8)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_8-1)<A) and ((_CE2_8-1)<C)) and ((_CE2_8-1)<B))
(0<=_CE2_8)
((_CE2_8<=_n1) and (_n1<_CE1_8)) -> ((_n1-1)<A)
((_CE1_8-1)>=A)
(0<=_CE1_8)
(_CE2_8<_CE1_8)
((_CE1_8<=_n1) and (_n1<_CE3_8)) -> ((_n1-1)<C)
((_CE3_8-1)>=C)
(0<=_CE3_8)
(_CE1_8<_CE3_8)
((_CE3_8<=_n1) and (_n1<_CE4_8)) -> ((_n1-1)<B)
((_CE4_8-1)>=B)
(0<=_CE4_8)
(_CE3_8<_CE4_8)
((0<=_n1) and (_n1<_CE2_9)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_9-1)<A) and ((_CE2_9-1)<C)) and ((_CE2_9-1)<B))
(0<=_CE2_9)
((_CE2_9<=_n1) and (_n1<_CE1_9)) -> ((_n1-1)<A)
((_CE1_9-1)>=A)
(0<=_CE1_9)
(_CE2_9<_CE1_9)
((_CE1_9<=_n1) and (_n1<_CE4_9)) -> ((_n1-1)<B)
((_CE4_9-1)>=B)
(0<=_CE4_9)
(_CE1_9<_CE4_9)
((_CE4_9<=_n1) and (_n1<_CE3_9)) -> ((_n1-1)<C)
((_CE3_9-1)>=C)
(0<=_CE3_9)
(_CE4_9<_CE3_9)
((0<=_n1) and (_n1<_CE2_10)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_10-1)<A) and ((_CE2_10-1)<C)) and ((_CE2_10-1)<B))
(0<=_CE2_10)
((_CE2_10<=_n1) and (_n1<_CE3_10)) -> ((_n1-1)<C)
((_CE3_10-1)>=C)
(0<=_CE3_10)
(_CE2_10<_CE3_10)
((_CE3_10<=_n1) and (_n1<_CE1_10)) -> ((_n1-1)<A)
((_CE1_10-1)>=A)
(0<=_CE1_10)
(_CE3_10<_CE1_10)
((_CE1_10<=_n1) and (_n1<_CE4_10)) -> ((_n1-1)<B)
((_CE4_10-1)>=B)
(0<=_CE4_10)
(_CE1_10<_CE4_10)
((0<=_n1) and (_n1<_CE2_11)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_11-1)<A) and ((_CE2_11-1)<C)) and ((_CE2_11-1)<B))
(0<=_CE2_11)
((_CE2_11<=_n1) and (_n1<_CE3_11)) -> ((_n1-1)<C)
((_CE3_11-1)>=C)
(0<=_CE3_11)
(_CE2_11<_CE3_11)
((_CE3_11<=_n1) and (_n1<_CE4_11)) -> ((_n1-1)<B)
((_CE4_11-1)>=B)
(0<=_CE4_11)
(_CE3_11<_CE4_11)
((_CE4_11<=_n1) and (_n1<_CE1_11)) -> ((_n1-1)<A)
((_CE1_11-1)>=A)
(0<=_CE1_11)
(_CE4_11<_CE1_11)
((0<=_n1) and (_n1<_CE2_12)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_12-1)<A) and ((_CE2_12-1)<C)) and ((_CE2_12-1)<B))
(0<=_CE2_12)
((_CE2_12<=_n1) and (_n1<_CE4_12)) -> ((_n1-1)<B)
((_CE4_12-1)>=B)
(0<=_CE4_12)
(_CE2_12<_CE4_12)
((_CE4_12<=_n1) and (_n1<_CE1_12)) -> ((_n1-1)<A)
((_CE1_12-1)>=A)
(0<=_CE1_12)
(_CE4_12<_CE1_12)
((_CE1_12<=_n1) and (_n1<_CE3_12)) -> ((_n1-1)<C)
((_CE3_12-1)>=C)
(0<=_CE3_12)
(_CE1_12<_CE3_12)
((0<=_n1) and (_n1<_CE2_13)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_13-1)<A) and ((_CE2_13-1)<C)) and ((_CE2_13-1)<B))
(0<=_CE2_13)
((_CE2_13<=_n1) and (_n1<_CE4_13)) -> ((_n1-1)<B)
((_CE4_13-1)>=B)
(0<=_CE4_13)
(_CE2_13<_CE4_13)
((_CE4_13<=_n1) and (_n1<_CE3_13)) -> ((_n1-1)<C)
((_CE3_13-1)>=C)
(0<=_CE3_13)
(_CE4_13<_CE3_13)
((_CE3_13<=_n1) and (_n1<_CE1_13)) -> ((_n1-1)<A)
((_CE1_13-1)>=A)
(0<=_CE1_13)
(_CE3_13<_CE1_13)
((0<=_n1) and (_n1<_CE3_14)) -> ((_n1-1)<C)
((_CE3_14-1)>=C)
(0<=_CE3_14)
(0<_CE3_14)
((_CE3_14<=_n1) and (_n1<_CE1_14)) -> ((_n1-1)<A)
((_CE1_14-1)>=A)
(0<=_CE1_14)
(_CE3_14<_CE1_14)
((_CE1_14<=_n1) and (_n1<_CE2_14)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_14-1)<A) and ((_CE2_14-1)<C)) and ((_CE2_14-1)<B))
(0<=_CE2_14)
(1<=_CE2_14)
((_CE2_14<=_n1) and (_n1<_CE4_14)) -> ((_n1-1)<B)
((_CE4_14-1)>=B)
(0<=_CE4_14)
(_CE2_14<_CE4_14)
((0<=_n1) and (_n1<_CE3_15)) -> ((_n1-1)<C)
((_CE3_15-1)>=C)
(0<=_CE3_15)
(0<_CE3_15)
((_CE3_15<=_n1) and (_n1<_CE1_15)) -> ((_n1-1)<A)
((_CE1_15-1)>=A)
(0<=_CE1_15)
(_CE3_15<_CE1_15)
((_CE1_15<=_n1) and (_n1<_CE4_15)) -> ((_n1-1)<B)
((_CE4_15-1)>=B)
(0<=_CE4_15)
(_CE1_15<_CE4_15)
((_CE4_15<=_n1) and (_n1<_CE2_15)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_15-1)<A) and ((_CE2_15-1)<C)) and ((_CE2_15-1)<B))
(0<=_CE2_15)
(4<=_CE2_15)
((0<=_n1) and (_n1<_CE3_16)) -> ((_n1-1)<C)
((_CE3_16-1)>=C)
(0<=_CE3_16)
(0<_CE3_16)
((_CE3_16<=_n1) and (_n1<_CE2_16)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_16-1)<A) and ((_CE2_16-1)<C)) and ((_CE2_16-1)<B))
(0<=_CE2_16)
(3<=_CE2_16)
((_CE2_16<=_n1) and (_n1<_CE1_16)) -> ((_n1-1)<A)
((_CE1_16-1)>=A)
(0<=_CE1_16)
(_CE2_16<_CE1_16)
((_CE1_16<=_n1) and (_n1<_CE4_16)) -> ((_n1-1)<B)
((_CE4_16-1)>=B)
(0<=_CE4_16)
(_CE1_16<_CE4_16)
((0<=_n1) and (_n1<_CE3_17)) -> ((_n1-1)<C)
((_CE3_17-1)>=C)
(0<=_CE3_17)
(0<_CE3_17)
((_CE3_17<=_n1) and (_n1<_CE2_17)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_17-1)<A) and ((_CE2_17-1)<C)) and ((_CE2_17-1)<B))
(0<=_CE2_17)
(3<=_CE2_17)
((_CE2_17<=_n1) and (_n1<_CE4_17)) -> ((_n1-1)<B)
((_CE4_17-1)>=B)
(0<=_CE4_17)
(_CE2_17<_CE4_17)
((_CE4_17<=_n1) and (_n1<_CE1_17)) -> ((_n1-1)<A)
((_CE1_17-1)>=A)
(0<=_CE1_17)
(_CE4_17<_CE1_17)
((0<=_n1) and (_n1<_CE3_18)) -> ((_n1-1)<C)
((_CE3_18-1)>=C)
(0<=_CE3_18)
(0<_CE3_18)
((_CE3_18<=_n1) and (_n1<_CE4_18)) -> ((_n1-1)<B)
((_CE4_18-1)>=B)
(0<=_CE4_18)
(_CE3_18<_CE4_18)
((_CE4_18<=_n1) and (_n1<_CE1_18)) -> ((_n1-1)<A)
((_CE1_18-1)>=A)
(0<=_CE1_18)
(_CE4_18<_CE1_18)
((_CE1_18<=_n1) and (_n1<_CE2_18)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_18-1)<A) and ((_CE2_18-1)<C)) and ((_CE2_18-1)<B))
(0<=_CE2_18)
(1<=_CE2_18)
((0<=_n1) and (_n1<_CE3_19)) -> ((_n1-1)<C)
((_CE3_19-1)>=C)
(0<=_CE3_19)
(0<_CE3_19)
((_CE3_19<=_n1) and (_n1<_CE4_19)) -> ((_n1-1)<B)
((_CE4_19-1)>=B)
(0<=_CE4_19)
(_CE3_19<_CE4_19)
((_CE4_19<=_n1) and (_n1<_CE2_19)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_19-1)<A) and ((_CE2_19-1)<C)) and ((_CE2_19-1)<B))
(0<=_CE2_19)
(4<=_CE2_19)
((_CE2_19<=_n1) and (_n1<_CE1_19)) -> ((_n1-1)<A)
((_CE1_19-1)>=A)
(0<=_CE1_19)
(_CE2_19<_CE1_19)
((0<=_n1) and (_n1<_CE4_20)) -> ((_n1-1)<B)
((_CE4_20-1)>=B)
(0<=_CE4_20)
(0<_CE4_20)
((_CE4_20<=_n1) and (_n1<_CE1_20)) -> ((_n1-1)<A)
((_CE1_20-1)>=A)
(0<=_CE1_20)
(_CE4_20<_CE1_20)
((_CE1_20<=_n1) and (_n1<_CE2_20)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_20-1)<A) and ((_CE2_20-1)<C)) and ((_CE2_20-1)<B))
(0<=_CE2_20)
(1<=_CE2_20)
((_CE2_20<=_n1) and (_n1<_CE3_20)) -> ((_n1-1)<C)
((_CE3_20-1)>=C)
(0<=_CE3_20)
(_CE2_20<_CE3_20)
((0<=_n1) and (_n1<_CE4_21)) -> ((_n1-1)<B)
((_CE4_21-1)>=B)
(0<=_CE4_21)
(0<_CE4_21)
((_CE4_21<=_n1) and (_n1<_CE1_21)) -> ((_n1-1)<A)
((_CE1_21-1)>=A)
(0<=_CE1_21)
(_CE4_21<_CE1_21)
((_CE1_21<=_n1) and (_n1<_CE3_21)) -> ((_n1-1)<C)
((_CE3_21-1)>=C)
(0<=_CE3_21)
(_CE1_21<_CE3_21)
((_CE3_21<=_n1) and (_n1<_CE2_21)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_21-1)<A) and ((_CE2_21-1)<C)) and ((_CE2_21-1)<B))
(0<=_CE2_21)
(3<=_CE2_21)
((0<=_n1) and (_n1<_CE4_22)) -> ((_n1-1)<B)
((_CE4_22-1)>=B)
(0<=_CE4_22)
(0<_CE4_22)
((_CE4_22<=_n1) and (_n1<_CE2_22)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_22-1)<A) and ((_CE2_22-1)<C)) and ((_CE2_22-1)<B))
(0<=_CE2_22)
(4<=_CE2_22)
((_CE2_22<=_n1) and (_n1<_CE1_22)) -> ((_n1-1)<A)
((_CE1_22-1)>=A)
(0<=_CE1_22)
(_CE2_22<_CE1_22)
((_CE1_22<=_n1) and (_n1<_CE3_22)) -> ((_n1-1)<C)
((_CE3_22-1)>=C)
(0<=_CE3_22)
(_CE1_22<_CE3_22)
((0<=_n1) and (_n1<_CE4_23)) -> ((_n1-1)<B)
((_CE4_23-1)>=B)
(0<=_CE4_23)
(0<_CE4_23)
((_CE4_23<=_n1) and (_n1<_CE2_23)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_23-1)<A) and ((_CE2_23-1)<C)) and ((_CE2_23-1)<B))
(0<=_CE2_23)
(4<=_CE2_23)
((_CE2_23<=_n1) and (_n1<_CE3_23)) -> ((_n1-1)<C)
((_CE3_23-1)>=C)
(0<=_CE3_23)
(_CE2_23<_CE3_23)
((_CE3_23<=_n1) and (_n1<_CE1_23)) -> ((_n1-1)<A)
((_CE1_23-1)>=A)
(0<=_CE1_23)
(_CE3_23<_CE1_23)
((0<=_n1) and (_n1<_CE4_24)) -> ((_n1-1)<B)
((_CE4_24-1)>=B)
(0<=_CE4_24)
(0<_CE4_24)
((_CE4_24<=_n1) and (_n1<_CE3_24)) -> ((_n1-1)<C)
((_CE3_24-1)>=C)
(0<=_CE3_24)
(_CE4_24<_CE3_24)
((_CE3_24<=_n1) and (_n1<_CE1_24)) -> ((_n1-1)<A)
((_CE1_24-1)>=A)
(0<=_CE1_24)
(_CE3_24<_CE1_24)
((_CE1_24<=_n1) and (_n1<_CE2_24)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_24-1)<A) and ((_CE2_24-1)<C)) and ((_CE2_24-1)<B))
(0<=_CE2_24)
(1<=_CE2_24)
((0<=_n1) and (_n1<_CE4_25)) -> ((_n1-1)<B)
((_CE4_25-1)>=B)
(0<=_CE4_25)
(0<_CE4_25)
((_CE4_25<=_n1) and (_n1<_CE3_25)) -> ((_n1-1)<C)
((_CE3_25-1)>=C)
(0<=_CE3_25)
(_CE4_25<_CE3_25)
((_CE3_25<=_n1) and (_n1<_CE2_25)) -> !(((((_n1-1)<A) and ((_n1-1)<C)) and ((_n1-1)<B)))
((((_CE2_25-1)<A) and ((_CE2_25-1)<C)) and ((_CE2_25-1)<B))
(0<=_CE2_25)
(3<=_CE2_25)
((_CE2_25<=_n1) and (_n1<_CE1_25)) -> ((_n1-1)<A)
((_CE1_25-1)>=A)
(0<=_CE1_25)
(_CE2_25<_CE1_25)

```




#### Example 25

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=ite(B>0,X(_n1)+Y(_n1),ite(C>0,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(B>0,Y(_n1)+1,ite(C>0,X(_n1)+Y(_n1),Y(_n1)))"
  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite((C>0),(A+(2*_n1)),ite((B>0),(((((2*A)+((2*B)*_n1))-_n1)+(_n1**2))/2),A))
Y(_n1) = ite((C>0),((((A*_n1)+B)+(_n1**2))-_n1),ite((B>0),(B+_n1),B))

ADDITIONAL AXIOMS
No Additional AXIOMS

```


#### Example 26

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=ite(_n1<50,X(_n1)+Y(_n1),ite(_n1<70,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(_n1<50,Y(_n1)+1,ite(_n1<70,X(_n1)+Y(_n1),Y(_n1)))"
  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = ite(((_n1-1)<50),(((((2*A)+((2*B)*_n1))-_n1)+(_n1**2))/2),ite(((_n1-1)<70),((((((2*A)+((2*B)*(_CE1-1)))-(_CE1-1))+((_CE1-1)**2))/2)+(2*_n1)),((((((2*A)+((2*B)*(_CE1-1)))-(_CE1-1))+((_CE1-1)**2))/2)+(2*(_CE2-1)))))
Y(_n1) = ite(((_n1-1)<50),(B+_n1),ite(((_n1-1)<70),(((((((((2*A)+((2*B)*(_CE1-1)))-(_CE1-1))+((_CE1-1)**2))/2)*_n1)+(B+(_CE1-1)))+(_n1**2))-_n1),(((((((((2*A)+((2*B)*(_CE1-1)))-(_CE1-1))+((_CE1-1)**2))/2)*(_CE2-1))+(B+(_CE1-1)))+((_CE2-1)**2))-(_CE2-1))))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1)) -> ((_n1-1)<50)
(_CE1>=50)
(0<=_CE1)
(0<_CE1)
((_CE1<=_n1) and (_n1<_CE2)) -> ((_n1-1)<70)
(_CE2>=70)
(0<=_CE2)
(_CE1<_CE2)

```



#### Example 27

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=ite(_n1<C,X(_n1)+Y(_n1),ite(_n1<D,X(_n1)+2,X(_n1)));Y(_n1+1)=ite(_n1<C,Y(_n1)+1,ite(_n1<D,X(_n1)+Y(_n1),Y(_n1)))"
  "_n1"
```

#### Output 

```python
NOt ABLE TO SOLVE FOLLOWING
No Equations Left

CLOSED FORM SOLUTION
X(_n1) = (ite(((_n1-1)<D),(A+(2*_n1)),ite(((_n1-1)<C),(((((2*(A+(2*(_CE3_3-1))))+((2*((((_CV3*(_CE3_3-1))+B)+((_CE3_3-1)**2))-(_CE3_3-1)))*_n1))-_n1)+(_n1**2))/2),(((((2*(A+(2*(_CE3_3-1))))+((2*((((_CV3*(_CE3_3-1))+B)+((_CE3_3-1)**2))-(_CE3_3-1)))*(_CE2_3-1)))-(_CE2_3-1))+((_CE2_3-1)**2))/2))) or ite(((_n1-1)<C),(((((2*A)+((2*B)*_n1))-_n1)+(_n1**2))/2),ite(((_n1-1)<D),((((((2*A)+((2*B)*(_CE2_2-1)))-(_CE2_2-1))+((_CE2_2-1)**2))/2)+(2*_n1)),((((((2*A)+((2*B)*(_CE2_2-1)))-(_CE2_2-1))+((_CE2_2-1)**2))/2)+(2*(_CE3_2-1))))))
Y(_n1) = (ite(((_n1-1)<D),((((A*_n1)+B)+(_n1**2))-_n1),ite(((_n1-1)<C),(((((A*(_CE3_3-1))+B)+((_CE3_3-1)**2))-(_CE3_3-1))+_n1),(((((A*(_CE3_3-1))+B)+((_CE3_3-1)**2))-(_CE3_3-1))+(_CE2_3-1)))) or ite(((_n1-1)<C),(B+_n1),ite(((_n1-1)<D),(((((((((2*A)+((2*B)*(_CE2_2-1)))-(_CE2_2-1))+((_CE2_2-1)**2))/2)*_n1)+(B+(_CE2_2-1)))+(_n1**2))-_n1),(((((((((2*A)+((2*B)*(_CE2_2-1)))-(_CE2_2-1))+((_CE2_2-1)**2))/2)*(_CE3_2-1))+(B+(_CE2_2-1)))+((_CE3_2-1)**2))-(_CE3_2-1)))))

ADDITIONAL AXOIMS
((0<=_n1) and (_n1<_CE2_2)) -> ((_n1-1)<C)
(_CE2_2>=C)
(0<=_CE2_2)
(0<=0)
(0<_CE2_2)
((_CE2_2<=_n1) and (_n1<_CE3_2)) -> ((_n1-1)<D)
(_CE3_2>=D)
(0<=_CE3_2)
(_CE2_2<_CE3_2)
((0<=_n1) and (_n1<_CE3_3)) -> ((_n1-1)<D)
(_CE3_3>=D)
(0<=_CE3_3)
(0<=0)
(0<_CE3_3)
((_CE3_3<=_n1) and (_n1<_CE2_3)) -> ((_n1-1)<C)
(_CE2_3>=C)
(0<=_CE2_3)
(_CE3_3<_CE2_3)

```



#### Example 28

```python
$recSolver/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=ite(X(_n1)+Y(_n1)<C,X(_n1)+Y(_n1),X(_n1)+2);Y(_n1+1)=ite(X(_n1)+Y(_n1)<C,Y(_n1)+1,X(_n1)+Y(_n1))"
  "_n1"
```

#### Output 

```python
X(_n1) = (ite((((((((2*(((((2*A)+((2*(B+(_CE2_3-1)))*(_CE2_3-1)))-(_CE2_3-1))+((_CE2_3-1)**2))/2))+((2*(B+(_CE2_3-1)))*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+((B+(_CE2_3-1))+(_n1-1)))<C),(((((2*A)+((2*(B+(_CE2_3-1)))*_n1))-_n1)+(_n1**2))/2),(((((2*(((((2*A)+((2*(B+(_CE2_3-1)))*(_CE2_3-1)))-(_CE2_3-1))+((_CE2_3-1)**2))/2))+((2*(B+(_CE2_3-1)))*_n1))-_n1)+(_n1**2))/2)) or ite(!((((((((2*_CV2)+((2*_CV4)*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+(_CV4+(_n1-1)))<C)),(A+(2*_n1)),((A+(2*(_CE1_2-1)))+(2*_n1))))
Y(_n1) = (ite((((((((2*(((((2*A)+((2*(B+(_CE2_3-1)))*(_CE2_3-1)))-(_CE2_3-1))+((_CE2_3-1)**2))/2))+((2*(B+(_CE2_3-1)))*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+((B+(_CE2_3-1))+(_n1-1)))<C),(B+_n1),((B+(_CE2_3-1))+_n1)) or ite(!((((((((2*_CV2)+((2*_CV4)*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+(_CV4+(_n1-1)))<C)),(((((A+(2*(_CE1_2-1)))*_n1)+B)+(_n1**2))-_n1),(((((A+(2*(_CE1_2-1)))*_n1)+(((((A+(2*(_CE1_2-1)))*(_CE1_2-1))+B)+((_CE1_2-1)**2))-(_CE1_2-1)))+(_n1**2))-_n1)))

ADDITIONAL AXIOMS
((0<=_n1) and (_n1<_CE1_2)) -> !((((((((2*_CV2)+((2*_CV4)*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+(_CV4+(_n1-1)))<C))
(((((((2*_CV2)+((2*_CV4)*_CE1_2))-_CE1_2)+(_CE1_2**2))/2)+(_CV4+_CE1_2))<C)
(0<=_CE1_2)
(0<=0)
(0<_CE1_2)
((0<=_n1) and (_n1<_CE2_3)) -> (((((((2*_CV2)+((2*_CV4)*(_n1-1)))-(_n1-1))+((_n1-1)**2))/2)+(_CV4+(_n1-1)))<C)
(((((((2*_CV2)+((2*_CV4)*_CE2_3))-_CE2_3)+(_CE2_3**2))/2)+(_CV4+_CE2_3))>=C)
(0<=_CE2_3)
(0<=0)
(0<_CE2_3)


```
