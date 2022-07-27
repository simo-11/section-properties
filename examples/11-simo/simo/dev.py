# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:36:57 2022

@author: simo.nikula@gmail.com
"""
#import argparse
from sectionproperties.analysis.section import Section

class DevSection(Section):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

def add_common_arguments(parser):
    parser.add_argument("--rtol", help="relative tolerance",
                        default=1e-3,type=float)
    parser.add_argument("-M","--plot_mesh", help="plot each mesh",
                        action="store_true")
    parser.add_argument("-G","--plot_geometry", help="plot geometry",
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
    parser.add_argument("--time_info",
                        help="show detailed info for computation",
                        action="store_true")
    parser.add_argument("--plot_warping_values",
                        help="plot warping values for each iteration",
                        action="store_true")
    parser.add_argument("--write_warping_csv",
                        help="write warping values for each iteration",
                        action="store_true")
