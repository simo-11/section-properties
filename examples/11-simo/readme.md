# Topics

## Provide warping function information
 * Plot
 * Numerical values
 * Function fitting approximation

### Analysis
Warping values are available in section.section_props.omega\[el.node_ids\] where el in section.mesh_elements.
coordinates in section.mesh_nodes.
See 
 * assemble_sc_warping_integrals in section.py
 * shear_warping_integrals in fea.py

### Changes
Samples in [rectangle.py](rectangle.py) and [cold-formed-u.py](rectangle.py).

#### matplotlib.pyplot plotting
Usable but a bit limited 3D-plotting can be created e.g. using plot_trisurf in matplotlib.pyplot.

```
runfile('C:/github/section-properties/examples/11-simo/rectangle.py',args='-H 1 -W 1 --plot_warping_values')
Rectangle: width = 1 and height = 1, rtol=0.001
It = 0.167, Iw = -5.42e-20
meshSize = 0.5, 9 nodes, 2 elements, itDiff = 0.833, iwDiff = 1
It = 0.167, Iw = -4.24e-22
meshSize = 0.25, 13 nodes, 4 elements, itDiff = 3.33e-16, iwDiff = 0.992
It = 0.146, Iw = 0.000174
meshSize = 0.125, 25 nodes, 8 elements, itDiff = 0.125, iwDiff = 4.1e+17
It = 0.143, Iw = 0.000156
meshSize = 0.0625, 41 nodes, 16 elements, itDiff = 0.0204, iwDiff = 0.102
It = 0.141, Iw = 0.000136
meshSize = 0.0312, 101 nodes, 42 elements, itDiff = 0.0133, iwDiff = 0.125
It = 0.141, Iw = 0.000136
meshSize = 0.0156, 226 nodes, 101 elements, itDiff = 0.00196, iwDiff = 0.00344
It = 0.141, Iw = 0.000135
meshSize = 0.00781, 441 nodes, 204 elements, itDiff = 0.000631, iwDiff = 0.0085
It = 0.141, Iw = 0.000135
meshSize = 0.00391, 875 nodes, 414 elements, itDiff = 9.25e-05, iwDiff = 0.00145
It = 0.141, Iw = 0.000134
```
![image](https://user-images.githubusercontent.com/1210784/181192924-d4a3a8c4-e9c9-48e5-b856-8a9118d6f1ac.png)
..
![image](https://user-images.githubusercontent.com/1210784/181192982-88108a68-e043-4a60-97b1-2fe65506ae38.png)
..
![image](https://user-images.githubusercontent.com/1210784/181193045-34c49540-47ef-4b10-aa98-31479f368e90.png)

#### write coordinates, warping and triangles to csv 
 * --write_warping_csv
   * coordinates for nodes x, y 
   * warping value w 
 * --write_triangles_csv
   * triangles for visualization
   * each parabolic (six noded) triangle is subdivided to four three noded triangles 
   * indexes are 0-based
```
runfile('C:/github/section-properties/examples/11-simo/cold-formed-u.py',args='-A -B --write_warping_csv --write_triangles_csv')
Cold-formed-U: width = 0.05, height = 0.1,
thickness= 0.004, outer radius=0.008, n_r=4
rtol=0.001
A = 0.000744, Ixx = 1.81e-07, Iyy = 1.12e-06, Ixy = 2.12e-22
Centroid: (0.0144,0.05)
It = 3.91e-09, Iw = 2.75e-10
Shear center: (-0.0166,0.05)
Wrote USection-100x50x4-8-4-249.csv
Wrote USection-tri-100x50x4-8-4-249.csv
meshSize = 0.025, 249 nodes, 86 elements, itDiff = 1, iwDiff = 1
It = 3.91e-09, Iw = 2.75e-10
Shear center: (-0.0166,0.05)
Wrote USection-100x50x4-8-4-267.csv
Wrote USection-tri-100x50x4-8-4-267.csv
```
##### Usage in matlab for interpolation of scattered data
```
t=readtable('C:/github/section-properties/examples/11-simo/USection-100x50x4-8-4-267.csv');
F = scatteredInterpolant(t.x,t.y,t.w);
F([0.05 0.05 0.05],[0 0.002 0.004])
ans =
   -0.0032   -0.0033   -0.0034
```

##### Usage in matlab e.g. for plotting
```
t=readtable('C:/github/section-properties/examples/11-simo/USection-100x50x4-8-4-267.csv');
t2=readtable('C:/github/section-properties/examples/11-simo/USection-tri-100x50x4-8-4-267.csv');
T=[t2.f, t2.s, t2.t]+1; % +1 to get proper indexes to coordinates in t
TO=triangulation(T,t.x,t.y,t.w);
trisurf(TO)
axis equal;
```
Or using ancf-rhs\cross-section\show_section
```
show_section('USection','100x50x4-8-4-267');
```
Use daspect command in matlab to scale data for viewing e.g. instead of default [1 1 1] due to axis equal
```
daspect([1 1 0.2])
```
![image](https://user-images.githubusercontent.com/1210784/181523464-fcfa25a5-6be3-4f1d-bf58-70d1d6397418.png)
..
![image](https://user-images.githubusercontent.com/1210784/181523584-a583d1db-8aca-4058-a63b-55e7a41bbb1d.png)