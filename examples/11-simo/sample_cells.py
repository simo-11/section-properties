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
import builtins
builtins.runfile(
    'C:/github/section-properties/examples/11-simo/primitive.py',
        args="""--plot_warping_values
        -A -W 1 -H 1 --mesh_size=0.05
        --primitive=rectangle
        """)
# %% circle
import builtins
builtins.runfile(
    'C:/github/section-properties/examples/11-simo/primitive.py',
        args="""--plot_warping_values
        -A --diameter 1 --mesh_size=0.05
        --primitive=circular
        """)
# %% rhs
import builtins
builtins.runfile(
    'C:/github/section-properties/examples/11-simo/primitive.py',
        args="""--plot_warping_values
        -A -W 1 -H 1 --thickness=0.1 --mesh_size=0.5
        --primitive=rhs
        """)
# %% cold-formed-u
import builtins
builtins.runfile(
    'C:/github/section-properties/examples/11-simo/cold-formed-u.py',
        args="""--plot_warping_values
        -A -W 1 -H 2 --thickness=0.1 --mesh_size=0.5
        """)
# %% torsion stress plots from upstream
"""
Note to myself, figure details on how warping function values (at nodes)
are used with shape function derivates (at gauss integration points)
to get correct shear stresses.
https://sectionproperties.readthedocs.io/en/latest/rst/theory.html
refers to usage of smoothing matrix.
"""
stress_post = section.calculate_stress(Mzz=1e6)#noqa
stress_post.plot_vector_mzz_zxy()
stress_post.plot_stress_mzz_zxy()
stress_post.plot_stress_mzz_zx()
stress_post.plot_stress_mzz_zy()
# %% warping
section.plot_warping_values()#noqa
