r"""

Cold-formed-u-section
--------------

Mesh is refined until relative change of torsion and warping constants
is not more than rtol
"""
import math
import csv
import argparse
from sectionproperties.analysis.section import Section

import numpy as np
from shapely.geometry import Polygon
import sectionproperties.pre.geometry as geometry
import sectionproperties.pre.pre as pre
from sectionproperties.pre.library.utils import draw_radius
import matplotlib.pyplot as plt
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

parser = argparse.ArgumentParser(description=
    ('Calculate section properties for cold-formed U-section.'),
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
parser.add_argument("--n_r", help="number of points in radius, 0 or >1",
                    default=4,type=int)
parser.add_argument("--rtol", help="relative tolerance",
                    default=1e-3,type=float)
parser.add_argument("-M","--plot_mesh", help="Plot each mesh",
                    action="store_true")
parser.add_argument("-G","--plot_geometry", help="Plot geometry",
                    action="store_true")
parser.add_argument("-P","--plot_section", help="Plot section",
                    action="store_true")
parser.add_argument("-B","--bending", help="show bending related constants",
                    action="store_true")
parser.add_argument("-F","--frame_analysis",
                    help="show frame analysis results",
                    action="store_true")
parser.add_argument("-A","--run_analysis",
                    help="run analysis",
                    action="store_true")
parser.add_argument("--plot_warping_values",
                    help="plot warping values for each iteration",
                    action="store_true")
parser.add_argument("--write_warping_csv",
                    help="write warping values for each iteration",
                    action="store_true")
args = parser.parse_args()
if args.n_r>0:
    if args.radius<args.thickness:
        args.radius=2*args.thickness
    if args.n_r==1:
       args.n_r=2
else:
    args.radius=0
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
if args.plot_section:
    fig, axes = plt.subplots()
    fig.set_size_inches(4,4)
    axes.set_aspect("equal", anchor="C")
    axes.set_title('U-{0:g}x{1:g}x{2:g}'.
                   format(args.height,args.width,args.thickness))
    # plot outline
    for (f) in geometry.facets:
        axes.plot(
            [geometry.points[f[0]][0], geometry.points[f[1]][0]],
            [geometry.points[f[0]][1], geometry.points[f[1]][1]],
            'k-',
            )
    axes.set_xticks([0,args.width])
    axes.set_yticks([0,args.height])
    t=args.thickness
    r_in=args.radius-t
    n_r=args.n_r
    if n_r>0:
        ai=n_r//2-1
        ap=draw_radius([t + r_in, t + r_in], r_in, 1.5 * np.pi, n_r, False)
        axes.annotate('r={0:.5g}'.format(args.thickness),
                      xycoords='data',
                      xy=(ap[ai][0],ap[ai][1]),
                      xytext=(0.25*args.width,0.25*args.height),
                      arrowprops=dict(arrowstyle='->')
                      )
    fn='USection-{0:g}x{1:g}x{2:g}.pdf'.format(*tuple([f * 1000 for f in
                       (args.height,args.width,args.thickness)]));
    plt.tight_layout()
    plt.savefig(fn);
    print("Saved {0}".format(fn))
    plt.show()
if args.plot_geometry:
    geometry.plot_geometry()
a=geometry.calculate_area()
it0=a
iw0=a
ms=min(args.width,args.height)
vertices0=0 # sometimes requesting smaller mesh size generates same mesh
if args.run_analysis:
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
            print("Shear center: ({0:.3g},{1:.3g})".format(*section.get_sc()))
            if args.plot_warping_values:
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
            if args.write_warping_csv:
                x=section.mesh_nodes[:,0]
                y=section.mesh_nodes[:,1]
                z=section.section_props.omega
                rows=np.empty([len(x),3],dtype=float)
                rows[:,0]=x
                rows[:,1]=y
                rows[:,2]=z
                fn='USection-{0:g}x{1:g}x{2:g}-{3:g}-{4:g}-{5}.csv'.format(
                     *tuple([f * 1000 for f in
                        (args.height,args.width,args.thickness,args.radius)]),
                     args.n_r,len(x));
                with open(fn, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(rows)
                print("Wrote {0}".format(fn))
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
