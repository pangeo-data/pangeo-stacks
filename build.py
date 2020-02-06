#!/usr/bin/env python3
"""
Build an image in the pangeo stack.
"""
import docker
import os
from repo2docker.app import Repo2Docker
import argparse

def docker_build(image_spec, path, build_args, cache_from=None):
    pwd = os.getcwd()
    print(f'Building {image_spec}')
    os.system('docker images')

    if os.path.exists(os.path.join(path, 'Dockerfile')):
        df_path = os.path.join(path, 'Dockerfile')
    else:
        df_path = os.path.join(path, 'binder', 'Dockerfile')

    cmd = f'docker build {path} -t {image_spec} -f {df_path}'
    if cache_from:
        cmd +=' --cache-from {cache_from}'
    for k, v in build_args.items():
        cmd += f' --build-arg {k}={v}'
    print(cmd)
    os.system(cmd)


def pull_latest(image_latest):
    print(f'Pulling {image_latest} for docker layer cache...')
    cmd = f'docker pull {image_latest}'
    print(cmd)
    os.system(cmd)


def r2d_build(image, image_spec, cache_from):
    r2d = Repo2Docker()

    r2d.subdir = image
    r2d.output_image_spec = image_spec
    r2d.user_id = 1000
    r2d.user_name = 'jovyan'
    r2d.cache_from = cache_from

    r2d.initialize()
    r2d.build()


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'image',
        help='Image to build. Subdirectory with this name must exist'
    )
    argparser.add_argument(
        '--tag',
        help='Docker image tag'
    )
    argparser.add_argument(
        '--image-prefix',
        help='Prefix for image to be built. Usually contains registry url and name',
        default='pangeo/'
    )

    args = argparser.parse_args()
    image_name = f'{args.image_prefix}{args.image}'
    tag = args.tag
    image_spec = f'{image_name}:{tag}'
    image_latest = f'{image_name}:latest'

    print(f'Building {image_name}')
    client = docker.from_env()

    pull_latest(image_latest)
    cache_from = [image_latest]

    dockerfile_paths = [
        os.path.join(args.image, 'binder', 'Dockerfile'),
        os.path.join(args.image, 'Dockerfile')
    ]
    if any((os.path.exists(df) for df in dockerfile_paths)):
        # Use docker if we have a Dockerfile
        # Can be just r2d once we can pass arbitrary BUILD ARGs to it
        # https://github.com/jupyter/repo2docker/issues/645
        docker_build(
            image_spec,
            args.image,
            {
                'VERSION': tag
            }
            cache_from=image_latest,
        )
    else:
        # Build regular image
        r2d_build(
            args.image,
            image_spec,
            cache_from
        )

    # Build onbuild image
    docker_build(
        f'{image_name}-onbuild:{tag}',
        'onbuild',
        {'BASE_IMAGE_SPEC': image_spec}
    )


if __name__ == '__main__':
    main()
