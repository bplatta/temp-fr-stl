#!/usr/bin/python3

import sys

from api import analyze_stl_file, view_analysis

full_path = sys.argv[1]
view_analysis(
    analyze_stl_file(
        full_path))
