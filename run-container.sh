#!/bin/bash

stl_file=$1
docker run -it --rm --name stl-analyze-py3 \
    -v "$PWD:/usr/src/app" \
    -w "/usr/src/app" \
    python:3 python /usr/src/app/cli.py $stl_file
