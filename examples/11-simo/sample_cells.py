# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:42:59 2023

@author: snikula
"""
# %% initialize rectangle using normal run
import builtins
builtins.runfile(
    'C:/github/section-properties/examples/11-simo/rectangle.py',
        args='--plot_warping_values -A -W 1 -H 4 --mesh_size=0.05')
# %% initialize rectangle using debugger
import builtins
builtins.debugfile(
    'C:/github/section-properties/examples/11-simo/rectangle.py',
        args='--plot_warping_values -A -W 1 -H 4 --mesh_size=0.05')
# %%% torsion vector plot from upstream
stress_post = section.calculate_stress(Mzz=1e6)#noqa
stress_post.plot_vector_mzz_zxy()
# %%% warping
section.plot_warping_values()#noqa
# %%
