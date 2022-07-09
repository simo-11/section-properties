r"""

Cold-formed-u-section
--------------

Mesh is refined until relative change of torsion and warping constants
is not more than rtol
"""
import math
import argparse
from sectionproperties.analysis.section import Section

import numpy as np
from shapely.geometry import Polygon
import sectionproperties.pre.geometry as geometry
import sectionproperties.pre.pre as pre
from sectionproperties.pre.library.utils import draw_radius


def u_section(
    d: float,
    b: float,
    t: float,
    r_out: float,
    n_r: int,
    material: pre.Material = pre.DEFAULT_MATERIAL,
) -> geometry.Geometry:
    """Constructs a U section (typical of cold-formed steel)
    with the bottom left corner at the
    origin *(0, 0)*, with depth/height *d*, width *b*, thickness *t*
    and outer radius *r_out*,
    using *n_r* points to construct the radius.
    If the outer radius is less than the thickness,
    the inner radius is set to zero.
    Code is based on steel_sections.cee_section

    :param float d: Depth/Height
    :param float b: Width
    :param float t: Thickness
    :param float r_out: Outer radius
    :param int n_r: Number of points discretising the outer radius
    :param Optional[sectionproperties.pre.pre.Material]:
        Material to associate with this geometry

    """
    points = []
    # calculate internal radius
    r_in = max(r_out - t, 0)
    # construct the outer bottom left radius
    points += draw_radius([r_out, r_out], r_out, np.pi, n_r)
    # bottom right corner
    points.append([b,0])
    points.append([b,t])
    # construct the inner bottom left radius
    points += draw_radius([t + r_in, t + r_in], r_in, 1.5 * np.pi, n_r, False)
    # construct the inner top left radius
    points += draw_radius([t + r_in, d - t - r_in], r_in, np.pi, n_r, False)
    # top right corner
    points.append([b,d-t])
    points.append([b,d])
    # construct the outer top left radius
    points += draw_radius([r_out, d - r_out], r_out, 0.5 * np.pi, n_r)
    polygon = Polygon(points)
    return geometry.Geometry(polygon, material)


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-W","--width", help="width",
                    default=0.05,type=float)
parser.add_argument("-H","--height", help="height",
                    default=0.1,type=float)
parser.add_argument("-T","--thickness", help="thickness",
                    default=0.004,type=float)
parser.add_argument("-R","--radius", help="""outer radius,
if < thickness, 2*thickness is used""",
                    default=0,type=float)
parser.add_argument("--n_r", help="number of points in radius",
                    default=4,type=int)
parser.add_argument("--rtol", help="relative tolerance",
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
args = parser.parse_args()
if args.radius<args.thickness:
    args.radius=2*args.thickness
print("""Cold-formed-U: width = {0:.5g}, height = {1:.5g},
thickness= {2:.5g}, outer radius={3:.5g}, n_r={4}
rtol={5:g}""".
      format(args.width, args.height,args.thickness,
             args.radius,args.n_r,args.rtol))
rtol=args.rtol
bending=args.bending
frame_analysis=args.frame_analysis
geometry = u_section(args.height, args.width,
                              args.thickness, args.radius, args.n_r)
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
section.plot_centroids()
print("Shear center: ({0:.3g},{1:.3g})".format(*section.get_sc()))
