# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:19:57 2024

This file is used to document and provide means to reproduce
run and also debug cells if needed.

@author: simo nikula
"""
# %% rectangles
import matplotlib.pyplot as plt
for h in (100,80,60,30,10,3,1):
    gPlotDone=False
    for ec_in_h in (6,10):
        ms=h/1000./10/(ec_in_h*ec_in_h)
        section=None
        runfile('primitive.py',#noqa
          args=f"""-A -W=0.1 -H={h/1000}
          --mesh_size={ms}
          --primitive=rectangle""")
        if not gPlotDone:
            pdf=plt.figure()
            fn=section.gfn(section.default_filename(".pdf","geometry"))
            section.geometry.plot_geometry(
                labels=()
                ,title=f"solid rectangle 100x{h} mm"
                ,cp=False
                ,legend=False
                ,filename=fn)
            print(f'Wrote {fn}')
            gPlotDone=True
        (fig,ax)=section.contour_warping_values(levels=51)
        fn=section.gfn(section.default_filename(".pdf","contour"))
        plt.savefig(fn)
        print(f'Wrote {fn}')
        plt.show();
        section.write_warping_csv()
        section.write_warping_gltf()
        section.write_warping_ply()
# %%



