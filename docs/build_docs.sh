#!/bin/bash

set -e

cd docs
python3 ./build_stacks_rst.py
make html
cd -
