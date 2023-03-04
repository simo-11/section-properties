# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:42:59 2023

This file is used to speedup testing of various fragments of code
known as cells e.g. in Spyder which provides means to run and debug cells.
Matlab has quite similar feature for matlab-scripts but uses
%% as cell separator


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
# %%% torsion stress vector plot from upstream
"""
Note to myself, figure details on how warping function values (at nodes)
are used with shape function derivates (at gauss integration points)
to get correct shear stresses.
https://sectionproperties.readthedocs.io/en/latest/rst/theory.html
refers to usage of smoothing matrix.
"""
stress_post = section.calculate_stress(Mzz=1e6)#noqa
stress_post.plot_vector_mzz_zxy()
# %%% warping
section.plot_warping_values()#noqa
# %%
