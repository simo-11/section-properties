# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:19:57 2024

This file is used to document and provide means to reproduce
run and also debug cells if needed.

@author: simo nikula
"""
# %% rectangle 100-100
import matplotlib.pyplot as plt
mesh_sizes=(0.01,3e-4, 1e-4, 3e-5)
n=len(mesh_sizes)
for i in range(0, n):
    section=None
    runfile('primitive.py',#noqa
      args="""-A -W=0.1 -H=0.1 
      --mesh_size={0} 
      --primitive=rectangle""".format(mesh_sizes[i]))
    if i == 0:
        pdf=plt.figure()
        fn=section.gfn(section.default_filename(".pdf","geometry"))
        section.geometry.plot_geometry(
            labels=()
            ,title="solid square 100x100 mm"
            ,cp=False
            ,legend=False
            ,filename=fn)
        print('Wrote {0}'.format(fn))
    section.write_warping_csv()
    section.write_warping_gltf()
    section.write_warping_ply()
# %% rectangle 100-10
import matplotlib.pyplot as plt
mesh_sizes=(3e-4, 1e-4, 3e-5)
n=len(mesh_sizes)
for i in range(0, n):
    section=None
    runfile('primitive.py',#noqa
      args="""-A -W=0.1 -H=0.01 
      --mesh_size={0} 
      --primitive=rectangle""".format(mesh_sizes[i]))
    if i == 0:
        pdf=plt.figure()
        fn=section.gfn(section.default_filename(".pdf","geometry"))
        section.geometry.plot_geometry(
            labels=()
            ,title="solid square 100x100 mm"
            ,cp=False
            ,legend=False
            ,filename=fn)
        print('Wrote {0}'.format(fn))
    section.write_warping_csv()
    section.write_warping_gltf()
# %%



