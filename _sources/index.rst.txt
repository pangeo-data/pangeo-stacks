.. Sphinx Pangeo Test documentation master file, created by
   sphinx-quickstart on Tue Apr  2 16:50:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pangeo Stacks
=============

Welcome to the Pangeo Stacks documentation.
The Pangeo Stacks live in the following GitHub repository:
`https://github.com/pangeo-data/pangeo-stacks <https://github.com/pangeo-data/pangeo-stacks>`_

This project includes set of currated Docker images intended to be used in
Pangeo Cloud Deployments of JupyterHub (see also `Pangeo Helm Chart`_).
For more information on using these images with JupyterHub, refer to the 
`Zero to JupyterHub`_ documentation. Each of the images in this repository are configured
and built using repo2docker_ and are continuously deployed to
`DockerHub <https://hub.docker.com/u/pangeo>`_. Importantly, each image built in this
project includes the minimum required libraries to do scalable computations with Pangeo
(via dask-kubernetes).

Contents
--------

This website is a statically generated Sphinx site from which you can browse the images and their contents.

.. toctree::
   :maxdepth: 3

   images

Onbuild Images
--------------

You can customize the images here in comon ways by using the image variants
that have the `-onbuild` suffix. If your Dockerfile inherits from an
`-onbuild` Pangeo image, you automatically get the following features:

1. The contents of your directory are copied with appropriate permissions
   into the image. The files will be present under the directory pointed
   to by ``${REPO_DIR}`` docker environment variable.
2. If you have any of the following files in your repository, they are
   used to automatically customize the image similar to what `repo2docker`
   (used by mybinder.org) does:

   a. `requirements.txt` installs python packages with `pip`
   b. `environment.yml` installs `conda` packages
   c. `apt.txt` lists ubuntu packages to be installed
   d. `postBuild` is a script (in any language) that is run automatically
      after other customization steps for you to execute arbitrary code.

   These files could also be inside a `binder/` directory rather than
   the top level of your repository if you would like.

For example, if you want to start from the base `pangeo-notebook` image but
add the `django` python package, you would do the following.

1. Create a `Dockerfile` in your repo with *just* the following content:

   ```
   FROM pangeo/pangeo-notebook:<version>
   ```

2. Add a `requirements.txt` file with the following contents

   ```
   django
   ```

And that's it! Now you can build the image any way you wish (on a binder instance,
with repo2docker, or just with `docker build`), and it'll do the customizations
for you automatically.

.. _Pangeo Helm Chart: https://github.com/pangeo-data/helm-chart
.. _Zero to JupyterHub: https://zero-to-jupyterhub.readthedocs.io/en/latest/user-environment.html#choose-and-use-an-existing-docker-image
.. _repo2docker: https://repo2docker.readthedocs.io/en/latest/
