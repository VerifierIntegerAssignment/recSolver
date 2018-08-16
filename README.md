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

In practice we have run VIAP on standard Ubuntu 16.04 LTS distribution. VIAP is provided as a set of binaries and libraries for
Ubuntu 16.04 LTS distribution. 

#### Download 


##### Clone over HTTPS:

 $ git clone https://github.com/VerifierIntegerAssignment/recSolver.git
 
 #### Running VIAP


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
$viap/recSolver.py  "X(0)=A;Y(0)=B;X(_n1+1)=X(_n1)+1;Y(_n1+1)=X(_n1)+Y(_n1)"  "_n1"
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
$viap/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"  "_n1"
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
$viap/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;M(0)=j;M(_n1+1)=X(_n1)+M(_n1);X(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+l*Y(_n1)+l*Z(_n1)+F"  "_n1"
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
$viap/recSolver.py  "X(0)=A;Y(0)=B;Z(0)=C;X(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+D;Y(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+H;Z(_n1+1)=l*X(_n1)+m*Y(_n1)+n*Z(_n1)+F"  "_n1"
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


