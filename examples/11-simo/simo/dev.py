# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:36:57 2022

@author: simo.nikula@gmail.com
"""
#import argparse
from sectionproperties.analysis.section import Section
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

class DevSection(Section):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triangles=None
        self.args=None
    """
    """
    def get_triangles(self):
        if not isinstance(self.triangles,np.ndarray):
            ma=self.mesh_elements
            ne=len(ma)
            nt=4*ne
            ti=0
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
            self.triangles=triangles
        return self.triangles

    def set_args(self,args):
        self.args=args

    def get_box_aspect(self):
        if self.args is None:
            return (4,4,2)
        z=min(self.args.width,self.args.height)*self.args.z_scale
        return (self.args.width,self.args.height,z)

    def plot_warping_values(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.set_box_aspect(self.get_box_aspect())
        x=self.mesh_nodes[:,0]
        y=self.mesh_nodes[:,1]
        z=self.section_props.omega
        triangles=self.get_triangles()
        ax.plot_trisurf(x, y,triangles, z)
        title=('{0} nodes, {1} elements'.format
            (self.num_nodes,len(self.elements)))
        ax.set_title(title)
        xticks=np.linspace(min(x),max(x),3)
        ax.set_xticks(xticks)
        zticks=np.linspace(min(self.section_props.omega),
                           max(self.section_props.omega),3)
        ax.set_zticks(zticks)
        plt.show()
        return (fig,ax)

    def get_k(self,nu: float=0.3):
        return math.sqrt(self.get_j()/((2*(1+nu))*self.get_gamma()))

    def write_warping_csv(self,fn):
        x=self.mesh_nodes[:,0]
        y=self.mesh_nodes[:,1]
        z=self.section_props.omega
        rows=np.empty([len(x),3],dtype=float)
        rows[:,0]=x
        rows[:,1]=y
        rows[:,2]=z
        with open(fn, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x','y','w'])
            writer.writerows(rows)
        print("Wrote {0}".format(fn))

    def write_triangles_csv(self,fn):
        rows=self.get_triangles();
        with open(fn, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['f','s','t'])
            writer.writerows(rows)
        print("Wrote {0}".format(fn))

    def done(self,ms,itDiff,iwDiff):
        if self.args.mesh_size:
            print(("meshSize = {0:.3g}, {1} nodes, {2} elements")
              .format(ms,self.num_nodes,len(self.elements)))
        else:
            print(("meshSize = {0:.3g}, {3} nodes, {4} elements, "+
                 "itDiff = {1:.3g}, iwDiff = {2:.3g}")
              .format(ms,itDiff,iwDiff,
                      self.num_nodes,len(self.elements)))
        return self.args.mesh_size or (
            itDiff<self.args.rtol and iwDiff<self.args.rtol)

def add_common_arguments(parser):
    parser.add_argument("--rtol", help="relative tolerance",
                        default=1e-2,type=float)
    parser.add_argument("--mesh_size",
                        help="fixed meshSize, rtol is not used",
                        type=float)
    parser.add_argument("-M","--plot_mesh", help="plot each mesh",
                        action="store_true")
    parser.add_argument("-G","--plot_geometry", help="plot geometry",
                        action="store_true")
    parser.add_argument("-P","--plot_section", help="Plot section",
                    action="store_true")
    parser.add_argument("-B","--bending",
                        help="show bending related constants",
                        action="store_true")
    parser.add_argument("-F","--frame_analysis",
                        help="show frame analysis results",
                        action="store_true")
    parser.add_argument("-A","--run_analysis",
                        help="run analysis",
                        action="store_true")
    parser.add_argument("--time_info",
                        help="show detailed info for computation",
                        action="store_true")
    parser.add_argument("--plot_warping_values",
                        help="plot warping values for each iteration",
                        action="store_true")
    parser.add_argument("--z_scale",
                        help="scaling of z in plot_warping_values",
                        default=0.5,type=float)
    parser.add_argument("--write_warping_csv",
                        help="write warping values for each iteration",
                        action="store_true")
    parser.add_argument("--write_triangles_csv",
                        help="write triangles for each iteration",
                        action="store_true")
    parser.add_argument("-W","--width", help="width",
                        default=1,type=float)
    parser.add_argument("-H","--height", help="height",
                        default=1,type=float)
    parser.add_argument("-T","--thickness", help="thickness",
                        default=0.004,type=float)
    parser.add_argument("-R","--radius", help="""outer radius,
    if < thickness, 2*thickness is used""",
                        default=0,type=float)
    parser.add_argument("--n_r", help="number of points in radius, 0 or >1",
                        default=4,type=int)
    parser.add_argument("-D","--diameter", help="diameter",
                        default=1,type=float)
    parser.add_argument("-N","--count", help="count of points",
                        default=32,type=float)

def check_arguments(parser,args):
    if (not args.plot_section and not args.plot_geometry
        and not args.run_analysis and not args.mesh_size
        and not args.plot_warping_values):
        parser.print_help()

def run(args):
    return (args.run_analysis or args.mesh_size or args.plot_warping_values)
