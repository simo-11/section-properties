# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:42:59 2023

This file is used to speedup testing of various fragments of code
known as cells e.g. in Spyder which provides means to run and debug cells.
Matlab has quite similar feature for matlab-scripts but uses
%% as cell separator


@author: snikula
"""
# %% rectangle
runfile('primitive.py',#noqa
  args="""-A -W 1 -H 1 --mesh_size=0.05 --primitive=rectangle""")
# %% circle
runfile('primitive.py',#noqa
  args="""-A --diameter 1 --mesh_size=0.05 --primitive=circular""")
# %% rhs
runfile('primitive.py',#noqa
  args="""-A -W 1 -H 1 --thickness=0.03 --mesh_size=0.05 --primitive=rhs
  --radius=0 --n_r=8""")
# %% chs
runfile('primitive.py',#noqa
  args="""-A --diameter 1 --thickness 0.03 --mesh_size=0.2 --primitive=chs
   --count=64""")
# %% cold-formed-u
runfile('cold-formed-u.py',#noqa
  args="""-A -W 1 -H 2 --thickness=0.1 --mesh_size=0.5""")
# %% plot_geometry
section.geometry.plot_geometry()#noqa
# %% plot_warping_values
section.plot_warping_values()#noqa
# %% contour_warping_values
section.contour_warping_values(levels=51)#noqa
# %% torsion stress plots from upstream
"""
Note to myself, figure details on how warping function values (at nodes)
are used with shape function derivates (at gauss integration points)
to get correct shear stresses.
https://sectionproperties.readthedocs.io/en/latest/rst/theory.html
refers to usage of smoothing matrix.
"""
stress_post = section.calculate_stress(Mzz=1e6)#noqa
ax_v=stress_post.plot_vector_mzz_zxy()
ax_c_xy=stress_post.plot_stress_mzz_zxy(normalize=False)
#ax_c_x=stress_post.plot_stress_mzz_zx()
#ax_c_y=stress_post.plot_stress_mzz_zy()
# %% inset axes for contour_warping_values
import matplotlib.pyplot as plt
levels=51
fn=None
title=None
s=section#noqa
w=s.args.width#noqa
h=s.args.height#noqa
if s.is_shs():#noqa
    fn='warping-of-shs.pdf'
    title='Warping distribution of SHS using section properties'
(fig,ax)=s.contour_warping_values(levels=levels)#noqa
if title:
    ax.set_title(title)
axins = ax.inset_axes([0.1, 0.1, 0.7, 0.7])
s.set_box_aspect(axins)
x=s.mesh_nodes[:,0]
y=s.mesh_nodes[:,1]
triangles=s.get_triangles()#noqa
z=s.section_props.omega#noqa
trictr = axins.tricontourf(x, y, triangles, z,levels=levels)
# subregion of the original image
x1, x2, y1, y2 = 0.92*w, 1.0*w, 0.92*h, 1.0*h
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax.indicate_inset_zoom(axins, edgecolor="black")
if fn!=None:
    plt.savefig(fn)
    print('Wrote {0}'.format(fn))
plt.show()
