Pangeo Stacks
=============
*Currated Docker images for use with Jupyter and [Pangeo](http://pangeo.io/)*

![Action Status](https://github.com/pangeo-data/pangeo-stacks/workflows/build/badge.svg)

This repository contains a few currated Docker images that can be used with deployments of the [Pangeo Helm Chart](https://github.com/pangeo-data/helm-chart). Each of the images in this repository are configured and built using [repo2docker](https://repo2docker.readthedocs.io) and are continuously deployed to DockerHub. Importantly, each image built in this repo includes the minimum required libraries to do scalable computations with Pangeo (via dask-kubernetes).

### Current Notebook Images:

| Image           | Description                                   | Link | Badges  |
|-----------------|-----------------------------------------------|------|---------|
| base-notebook   | A bare-bones image with Jupyter and Dask.     | [DockerHub](https://hub.docker.com/r/pangeo/base-notebook) | [![](https://img.shields.io/docker/pulls/pangeo/base-notebook.svg)](https://hub.docker.com/r/pangeo/base-notebook) [![](https://images.microbadger.com/badges/image/pangeo/base-notebook.svg)](https://microbadger.com/images/pangeo/base-notebook "Get your own image badge on microbadger.com")[![](https://images.microbadger.com/badges/version/pangeo/base-notebook.svg)](https://microbadger.com/images/pangeo/base-notebook "Get your own version badge on microbadger.com")     |
| pangeo-notebook | A complete image with lots of Python packages | [DockerHub](https://hub.docker.com/r/pangeo/pangeo-notebook) | [![](https://img.shields.io/docker/pulls/pangeo/pangeo-notebook.svg)](https://hub.docker.com/r/pangeo/pangeo-notebook) [![](https://images.microbadger.com/badges/image/pangeo/pangeo-notebook.svg)](https://microbadger.com/images/pangeo/pangeo-notebook "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/pangeo/pangeo-notebook.svg)](https://microbadger.com/images/pangeo/pangeo-notebook "Get your own version badge on microbadger.com") |
| pangeo-esip | An image customized for ESIP use | [DockerHub](https://hub.docker.com/r/pangeo/pangeo-esip) | [![](https://img.shields.io/docker/pulls/pangeo/pangeo-esip.svg)](https://hub.docker.com/r/pangeo/pangeo-esip) [![](https://images.microbadger.com/badges/image/pangeo/pangeo-esip.svg)](https://microbadger.com/images/pangeo/pangeo-esip "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/pangeo/pangeo-esip.svg)](https://microbadger.com/images/pangeo/pangeo-notebook "Get your own version badge on microbadger.com") |

### Customize images with the -onbuild variants

You can customize the images here in comon ways by using the image variants
that have the `-onbuild` suffix. If your Dockerfile inherits from an
`-onbuild` Pangeo image, you automatically get the following features:

1. The contents of your directory are copied with appropriate permissions
   into the image. The files will be present under the directory pointed
   to by `${REPO_DIR}` docker environment variable.
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
   FROM pangeo/pangeo-notebook-onbuild:<version>
   ```

2. Add a `requirements.txt` file with the following contents

   ```
   django
   ```

And that's it! Now you can build the image any way you wish (on a binder instance,
with repo2docker, or just with `docker build`), and it'll do the customizations
for you automatically.

### Adding new images

It is easy to add additional images. The basic steps involved are:

1. Open an [Issue](https://github.com/pangeo-data/pangeo-stacks/issues/new) to discuss adding your image.
2. Copy the `base-notebook` directory and name it something informative.
3. Modify the contents of the `binder` directory, adding any configuration you need according to the [repo2docker documentation](https://repo2docker.readthedocs.io/en/latest/config_files.html).
4. Edit the TravisCI configuration file to inclue the new image.
5. Push your changes to GitHub and open a Pull Request.

### CI/CD

The images in Pangeo-stacks are built and deployed continuously using [TravisCI](https://travis-ci.org/pangeo-data/pangeo-stacks). Images are versioned using the [CALVER](https://calver.org/) system.

### Build locally
The images here can be built locally using [repo2docker](https://repo2docker.readthedocs.io). The following example demonstrates how to build the `base-notebook` image:

```shell
repo2docker --no-run --user-name=jovyan --user-id 1000 \
    --image-name=pangeo/base-notebook ./base-notebook
```

### Related projects

- [Jupyter/docker-stacks](https://github.com/jupyter/docker-stacks): Ready-to-run Docker images containing Jupyter applications
- [repo2docker](https://repo2docker.readthedocs.io): A tool to build, run, and push Docker images from source code repositories that run via a Jupyter server
- [Pangeo Helm Chart](https://github.com/pangeo-data/helm-chart): The helm chart for installing Pangeo.
