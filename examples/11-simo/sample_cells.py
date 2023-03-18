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
  --radius=0.2 --n_r=8""")
# %% chs
runfile('primitive.py',#noqa
  args="""-A --diameter 1 --thickness 0.03 --mesh_size=0.2 --primitive=chs
   --count=64""")
# %% cold-formed-u
runfile('cold-formed-u.py',#noqa
  args="""-A -W 1 -H 2 --thickness=0.1 --mesh_size=0.5""")
# %% plot_warping_values
section.plot_warping_values()#noqa
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
# %% inset axes
#(fig,ax)=section.plot_warping_values()#noqa
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
fig = plt.figure()
fig, ax1 = plt.subplots()
ax1.set_title('Inset axes')
fig.__dict__
ax=ax_v
plt.show()
ax_v.draw()
if False:
    axins = zoomed_inset_axes(ax, zoom=0.5, loc='upper right')
    x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xticklabels([])
    axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins, edgecolor="black")
    plt.show()
