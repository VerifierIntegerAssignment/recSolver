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
X(_n1) = ite((C>0),(A+(2*_n1)),ite((B>0),(((((2*A)+((2*B)*_n1))-_n1)+(_n1**2))/2),A))
Y(_n1) = ite((C>0),((((A*_n1)+B)+(_n1**2))-_n1),ite((B>0),(B+_n1),B))

ADDITIONAL AXOIMS
No Additional Axoims
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

ADDITIONAL AXOIMS
No Additional Axoims
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

ADDITIONAL AXOIMS
No Additional Axoims

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

ADDITIONAL AXOIMS
No Additional Axoims


```


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

ADDITIONAL AXOIMS
No Additional Axoims



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

ADDITIONAL AXOIMS
No Additional Axoims



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

ADDITIONAL AXOIMS
No Additional Axoims




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

ADDITIONAL AXOIMS
No Additional Axoims




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

ADDITIONAL AXOIMS
No Additional Axoims




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
X(_n1) = ite((((1+(5*(_n1-1)))%2)==0),(1+(5*_n1)),(1+(5*_CE1)))

ADDITIONAL AXOIMS
((0<=_n1) and (_n1<_CE1)) -> (((1+(5*(_n1-1)))%2)==0)
(((1+(5*(_CE1-1)))%2)!=0)
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
No Additional Axoims




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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
No Additional Axoims






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

ADDITIONAL AXOIMS
No Additional Axoims



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

ADDITIONAL AXOIMS
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

ADDITIONAL AXOIMS
No Additional Axoims

```

