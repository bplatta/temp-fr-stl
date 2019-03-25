#!/usr/bin/python3

import sys

from api import analyze_stl_file, view_analysis

if len(sys.argv) < 2:
    print('Missing required path param: python cli.py /my/path/to/file.stl')
    exit(1)

full_path = sys.argv[1]
view_analysis(
    analyze_stl_file(
        full_path))
