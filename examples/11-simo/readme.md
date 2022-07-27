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

#### matplotlib.pyplot plotting
Usable but a bit limited 3D-plotting can be created e.g. using plot_trisurf in matplotlib.pyplot.
Sample is available in [rectangle.py](rectangle.py) and [cold-formed-u.py](rectangle.py)
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

