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
args = parser.parse_args()
print("Rectangle: width = {0:.5g} and height = {1:.5g}, rtol={2:g}".
      format(args.width, args.height,args.rtol))
rtol=args.rtol
bending=args.bending
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
    section = Section(geometry)
    if args.plot_mesh:
        section.plot_mesh()
    section.calculate_geometric_properties()
    if bending:
        print(("A = {0:.3g}, Ixx = {2:.3g}, Iyy = {1:.3g}, Ixy = {3:.3g}")
              .format(section.get_area(),*section.get_ic()))
        bending=False
    section.calculate_warping_properties()
    it = section.get_j()
    if math.isnan(it):
        continue
    iw = section.get_gamma()
    itDiff=abs((it-it0)/it0)
    iwDiff=abs((iw-iw0)/iw0)
    print(("It = {0:.3g}, Iw = {1:.3g}, "+
          "meshSize = {2:.3g}, {5} nodes, {6} elements, "+
          "itDiff = {3:.3g}, iwDiff = {4:.3g}")
          .format(it,iw,ms,itDiff,iwDiff,
                  section.num_nodes,len(section.elements)))
    if(itDiff<rtol and iwDiff<rtol ):
        break
    else:
        it0=it
        iw0=iw
