r"""

Rectangle
--------------

Calculate section properties of rectangle.
Mesh is refined until relative change of torsion and warping constants
is not more than rtol
"""
import math
import argparse
import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section
import matplotlib.pyplot as plt
import numpy as np
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-W","--width", help="width of square",
                    default=0.0032024,type=float)
parser.add_argument("-H","--height", help="height of square",
                    default=0.012377,type=float)
parser.add_argument("-R","--rtol", help="relative tolerance",
                    default=1e-3,type=float)
parser.add_argument("-M","--plot_mesh", help="Plot each mesh",
                    action="store_true")
parser.add_argument("-G","--plot_geometry", help="Plot geometry",
                    action="store_true")
parser.add_argument("-B","--bending", help="Show bending related constants",
                    action="store_true")
parser.add_argument("-F","--frame_analysis",
                    help="Show frame analysis results",
                    action="store_true")
parser.add_argument("-T","--time_info",
                    help="Show detailed info for computation",
                    action="store_true")
parser.add_argument("--print_warping_values",
                    help="Print warping values",
                    action="store_true")
args = parser.parse_args()
print("Rectangle: width = {0:.5g} and height = {1:.5g}, rtol={2:g}".
      format(args.width, args.height,args.rtol))
rtol=args.rtol
bending=args.bending
frame_analysis=args.frame_analysis
geometry = sections.rectangular_section(args.width, args.height)
if args.plot_geometry:
    geometry.plot_geometry()
a=geometry.calculate_area()
it0=a
iw0=a
ms=min(args.width,args.height)
vertices0=0 # sometimes requesting smaller mesh size generates same mesh
while True:
    ms=0.5*ms
    geometry.create_mesh(mesh_sizes=[ms])
    vertices=geometry.mesh.get('vertices').size
    if vertices0==vertices:
        ms=0.5*ms
        continue
    vertices0=vertices
    section = Section(geometry, time_info=args.time_info)
    if args.plot_mesh:
        section.plot_mesh()
    section.calculate_geometric_properties()
    if bending:
        print(("A = {0:.3g}, Ixx = {2:.3g}, Iyy = {1:.3g}, Ixy = {3:.3g}")
              .format(section.get_area(),*section.get_ic()))
        bending=False
    if frame_analysis:
        (area, ixx, iyy, ixy, it, phi)=section.calculate_frame_properties()
        print(("f: A = {0:.3g}, Ixx = {2:.3g}, Iyy = {1:.3g}, "+
               "Ixy = {3:.3g}, J = {4:.3g}")
              .format(area,ixx,iyy,ixy,it))
        iwDiff=0
        iw=0
    else:
        section.calculate_warping_properties()
        it = section.get_j()
        if math.isnan(it):
            continue
        iw = section.get_gamma()
        iwDiff=abs((iw-iw0)/iw0)
        print(("It = {0:.3g}, Iw = {1:.3g}").format(it,iw))
        if args.print_warping_values:
            print("Warping values: x, y, warping")
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        # Axes3D currently only supports the aspect argument 'auto'.
        #   You passed in 1
        # ax.set_adjustable('box')
        # ax.set_aspect(1)
        x=section.mesh_nodes[:,0]
        y=section.mesh_nodes[:,1]
        z=section.section_props.omega
        ma=section.mesh_elements
        ne=len(ma)
        nt=4*ne
        ti=0
        # triangles
        triangles=np.empty([nt, 3],dtype=int)
        for i in range(0,ne):
            me=ma[i]
            triangles[ti,0]=me[0]
            triangles[ti,1]=me[3]
            triangles[ti,2]=me[5]
            ti+=1
            triangles[ti,0]=me[3]
            triangles[ti,1]=me[1]
            triangles[ti,2]=me[4]
            ti+=1
            triangles[ti,0]=me[3]
            triangles[ti,1]=me[4]
            triangles[ti,2]=me[5]
            ti+=1
            triangles[ti,0]=me[5]
            triangles[ti,1]=me[4]
            triangles[ti,2]=me[2]
            ti+=1
        ax.plot_trisurf(x, y,triangles, z)
        plt.show();
    itDiff=abs((it-it0)/it0)
    if(itDiff<rtol and iwDiff<rtol ):
        break
    else:
        it0=it
        iw0=iw
        print(("meshSize = {0:.3g}, {3} nodes, {4} elements, "+
                      "itDiff = {1:.3g}, iwDiff = {2:.3g}")
              .format(ms,itDiff,iwDiff,
                  section.num_nodes,len(section.elements)))
