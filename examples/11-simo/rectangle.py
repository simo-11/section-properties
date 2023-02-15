r"""

Rectangle
--------------

Calculate section properties of rectangle.
Mesh is refined until relative change of torsion and warping constants
is not more than rtol unless mesh_size is given
"""
import math
import argparse
import sectionproperties.pre.library.primitive_sections as sections
#from sectionproperties.analysis.section import Section
import simo.dev
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-W","--width", help="width of square",
                    default=0.0032024,type=float)
parser.add_argument("-H","--height", help="height of square",
                    default=0.012377,type=float)
simo.dev.add_common_arguments(parser)
args = parser.parse_args()
simo.dev.check_arguments(parser,args)
print("Rectangle: width = {0:.5g} and height = {1:.5g}".
      format(args.width, args.height))
bending=args.bending
frame_analysis=args.frame_analysis
geometry = sections.rectangular_section(args.width, args.height)
if args.plot_geometry:
    geometry.plot_geometry()
a=geometry.calculate_area()
it0=a
iw0=a
ms=math.pow(min(args.width,args.height)/2,2)
vertices0=0 # sometimes requesting smaller mesh size generates same mesh
section=None
while simo.dev.run(args):
    ms=0.82*ms
    if args.mesh_size:
        ms=args.mesh_size
    geometry.create_mesh(mesh_sizes=[ms])
    vertices=geometry.mesh.get('vertices').size
    if vertices0==vertices:
        continue
    vertices0=vertices
    section = simo.dev.DevSection(geometry, time_info=args.time_info)
    section.set_args(args)
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
        if args.plot_warping_values:
            section.plot_warping_values()
        if args.write_warping_csv:
            fn=("rectangle-{0:g}-{1:g}-{2}.csv".
                format(1000*args.width,1000*args.height,
                       len(section.section_props.omega)))
            section.write_warping_csv(fn)
        if args.write_triangles_csv:
            fn=("rectangle-tri-{0:g}-{1:g}-{2}.csv".
                format(1000*args.width,1000*args.height,
                       len(section.section_props.omega)))
            section.write_triangles_csv(fn)
    itDiff=abs((it-it0)/it0)
    if section.done(ms,itDiff,iwDiff):
        break
    else:
        it0=it
        iw0=iw
