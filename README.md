Pangeo Stacks
=============

Currated Docker images for use with Jupyter

[![Build Status](https://travis-ci.org/pangeo-data/pangeo-stacks.svg?branch=master)](https://travis-ci.org/pangeo-data/pangeo-stacks)

Current Notebook Images:
1. Base Notebook: ![](https://img.shields.io/docker/pulls/pangeo/base-notebook.svg)
1. Pangeo Notebook: ![](https://img.shields.io/docker/pulls/pangeo/pangeo-notebook.svg)

### build locally
```
repo2docker --debug --user-name=jovyan --appendix="`cat appendix.txt`" ./base-notebook
```
