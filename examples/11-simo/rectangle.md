# Rectangle

## In spyder

Create data files in csv format for warping functions
```
runcell('rectangle 100-100', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
rectangle: width = 0.1 and height = 0.1
It = 1.43e-05, Iw = 1.3e-10, k(steel) = 205.28
meshSize = 0.001, 41 nodes, 16 elements
runcell('write_warping_csv', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Wrote warping-rectangle-100-100-41.csv

rectangle: width = 0.1 and height = 0.1
It = 1.41e-05, Iw = 1.35e-10, k(steel) = 200.51
meshSize = 0.0001, 357 nodes, 162 elements
runcell('write_warping_csv', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Wrote warping-rectangle-100-100-357.csv
```
## In matlab 

Create surface fit to data provided by csv files using Curve fitting toolbox
 * cubicinterp - Cubic spline interpolation
 * poly44 - polynomial surfaces where i is the degree in x and j is the degree in y. The maximum for both i and j is five. For rectangle 44 gives quite good results.
 * anonymous function - see fittype for details
   * test process by using known analytical solution https://en.wikiversity.org/wiki/Warping_functions#Example_3:_Rectangular_Cylinder for few lowest values of n  

using 41 node function as input to cubicinterp produces reasonable approximation and recalculated value of Iw is about 8 % too high
```
> fprintf("%s\n",pwd)
C:\Users\simon\github\section-properties\examples\11-simo
>> dir gen/*.csv
warping-rectangle-100-100-41.csv
>> t41=readtable('gen/warping-rectangle-100-100-41.csv');
>> c41=fit([t41.x t41.y],t41.w,'cubicinterp');
>> plot(c41,[t41.x t41.y],t41.w);
```
![image](https://github.com/simo-11/section-properties/assets/1210784/7a02dc7d-5467-40ac-988a-1167b797ca06)
```
>> fun41=@(x,y)c41(x,y).^2;
>> fprintf("%.3g\n",integral2(fun41,0.,0.1,0,0.1))
1.46e-10
```
Using 357 nodes reduces error in Iw to less than 1 %.
```
>> t2=readtable('gen/warping-rectangle-100-100-357.csv');
>> f2=fit([t2.x t2.y],t2.w,'cubicinterp');
>> plot(f2,[t2.x t2.y],t2.w);
>> w2=@(x,y)f2(x,y).^2;
>> fprintf("%.3g\n",integral2(w2,0.,0.1,0,0.1))
1.36e-10
```
Create mex_function using [w_100_100_41.m](w_100_100_41.m) is not supported
```
x=0.1;y=0.025;codegen w_100_100_41.m -args {x,y}
Undefined function or variable 'f1'. For code generation, all variables must be fully
defined before use.
>> x=0.1;y=0.025;codegen w_100_100_41.m -args {f1,x,y}
Function input at args{1} does not have a valid type.

Caused by:
    Type conversion failed at <obj>(1).expr.
        Class function_handle is not supported by coder.Type.
```
### Upper level script
Reads all files selected by rectangle dimensions and performs cubicinterp and poly44 fits.
```
>> c100=testRectangle(height=100,width=100)
>> c100{1}
 struct with fields:

                  t: [357×3 table]
               file: "C:\Users\simon\github\section-properties\examples\11-simo\gen/warping-rectangle-100-100-357.csv"
        cubicinterp: 1.3570e-10
    cubicinterp_fit: [1×1 sfit]
             poly44: 1.3591e-10
         poly44_fit: [1×1 sfit]
>> figure(101)
>> plot(c100{1}.poly44_fit,[c100{1}.t.x c100{1}.t.y],c100{1}.t.w);
```
![image](https://github.com/simo-11/section-properties/assets/1210784/0d7dee0b-3db8-4541-8883-41deed27b57b)

Checking parameters for models providing them.
Comments after --
```
>> w=testRectangle(debugLevel=2,models=["poly44"],plot=0);
file=warping-rectangle-100-100-357.csv
x values: 0 - 0.1
y values: 0 - 0.1
w values: -0.000366 - 0.000366
model=poly44
     Linear model Poly44:
     f(x,y) = p00 + p10*x + p01*y + p20*x^2 + p11*x*y + p02*y^2 + p30*x^3 + p21*x^2*y 
                    + p12*x*y^2 + p03*y^3 + p40*x^4 + p31*x^3*y + p22*x^2*y^2 
                    + p13*x*y^3 + p04*y^4
     Coefficients (with 95% confidence bounds):
       p00 =   1.644e-07  (-6.632e-06, 6.961e-06) -- not important <0.001*w  
       p10 =    -0.03778  (-0.03834, -0.03721) -- important, transforms origin
       p01 =     0.03776  (0.0372, 0.03833) -- important, transforms origin
       p20 =       1.134  (1.115, 1.153) -- important 
       p11 =  -0.0001405  (-0.0147, 0.01442) -- not important <0.003*w
       p02 =      -1.133  (-1.152, -1.114) -- important
       p30 =      -7.564  (-7.828, -7.3) -- important
       p21 =      -22.67  (-22.86, -22.47) -- important
       p12 =       22.67  (22.47, 22.86) -- important
       p03 =       7.548  (7.282, 7.815) -- important
       p40 =     0.04689  (-1.232, 1.325) -- not important
       p31 =       151.1  (150, 152.2) -- important
       p22 =     0.02697  (-1.039, 1.093) -- not important
       p13 =      -151.1  (-152.2, -150) -- important
       p04 =     0.03326  (-1.261, 1.327) -- not important
```

## 100-10
Iw should be about 6.6e-12

### Spyder
```
runcell('rectangle 100-10', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Reloaded modules: simo, simo.dev
rectangle: width = 0.1 and height = 0.01
It = 3.13e-08, Iw = 6.64e-12, k(steel) = 42.54
meshSize = 1e-05, 375 nodes, 160 elements
runcell('write_warping_csv', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Wrote warping-rectangle-10-100-375.csv
```
### Matlab
```
>> r=testRectangle(height=10,width=100,plot=1);
```
![image](https://github.com/simo-11/section-properties/assets/1210784/8ac719b9-badd-45c2-b8c1-9966f7061771)


## 100-4
Iw should be about 4.4e-13

### Spyder

```
runcell('rectangle 100-4', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
rectangle: width = 0.004 and height = 0.1
It = 2.09e-09, Iw = 4.42e-13, k(steel) = 42.66
meshSize = 1e-05, 171 nodes, 56 elements
runcell('write_warping_csv', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Wrote warping-rectangle-100-4-171.csv

runcell('rectangle 100-4', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
rectangle: width = 0.004 and height = 0.1
It = 2.08e-09, Iw = 4.41e-13, k(steel) = 42.58
meshSize = 1e-06, 1397 nodes, 620 elements
runcell('write_warping_csv', 'C:/Users/simon/github/section-properties/examples/11-simo/sample_cells.py')
Wrote warping-rectangle-100-4-1397.csv
```
### matlab
```
>> r=testRectangle(height=100,width=4,plot=1)
```
![image](https://github.com/simo-11/section-properties/assets/1210784/7dd79516-126c-4dee-be22-dfe763fa7476)

![image](https://github.com/simo-11/section-properties/assets/1210784/49bf0827-c37c-4ad0-ad57-badac2ce67d6)
