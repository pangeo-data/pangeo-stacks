#!/usr/bin/env python3
"""
Build an image in the pangeo stack.
"""
import subprocess
from dateutil.parser import parse
from datetime import datetime
import pytz
import docker
import os
from functools import lru_cache
from repo2docker.app import Repo2Docker
import argparse


def sha_and_date():
    # git log --pretty='%cd %h %gd %gs' --date=iso -n 100
    lines = subprocess.check_output([
        "git",
        "log",
        "--pretty='%cd %h %gd %gs'",
        "--date=iso",
        "-n", "100",
    ]).decode('utf-8').strip().split('\n')

    d = {}
    for line in lines:
        l = line.replace("'", "").strip().split()
        sha = l[-1]
        iso_date = l[0]
        d[sha] = parse(iso_date)
    return d


@lru_cache(128)
def image_exists_in_registry(client, image_spec):
    """
    Return true if image exists in docker registry
    """
    try:
        image_manifest = client.images.get_registry_data(image_spec)
        return image_manifest is not None
    except docker.errors.APIError:
        return False


def docker_build(image_spec, path, build_args):
    pwd = os.getcwd()
    print(f'Building {image_spec}')
    print(f'PWD={pwd}')
    os.system('docker images')

    if os.path.exists(os.path.join(path, 'Dockerfile')):
        df_path = os.path.join(path, 'Dockerfile')
    else:
        df_path = os.path.join(path, 'binder', 'Dockerfile')

    cmd = [
       'docker', 'build',
       path
       '-t', image_spec,
       '-f', df_path
    ]
    for k, v in build_args.items():
       cmd += [' --build-arg', f'{k}={v}']

    subprocess.check_call(cmd, shell=True)


def docker_verify(image, image_spec):
    if os.path.exists(os.path.join(image, 'binder/verify')):
        print(f'Validating {image_spec}')
        # Validate the built image
        subprocess.check_call([
            'docker',
            'run',
            '-i', '-t',
            image_spec,
            'binder/verify'
        ], shell=True)
    else:
        print(f'No verify script found for {image_spec}')


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
        '--image-prefix',
        help='Prefix for image to be built. Usually contains registry url and name',
        default='pangeo/'
    )

    args = argparser.parse_args()

    image_name = f'{args.image_prefix}{args.image}'
    print(f'Building {image_name}')
    client = docker.from_env()
    cache_from = []

    sha_date = sha_and_date()

    # Pull the most recent built image available for this docker image
    # We can re-use the cache from that, significantly speeding up
    # our image builds
    for sha, date in sha_date.items():
        # Stick to UTC for calver
        existing_calver = date.astimezone(pytz.utc).strftime('%Y.%m.%d')
        existing_image_spec = f'{image_name}:{existing_calver}-{sha}'
        if image_exists_in_registry(client, existing_image_spec):
            print(f'Re-using cache from {existing_image_spec}')
            cache_from = [existing_image_spec]
            subprocess.check_call([
                'docker',
                'pull', existing_image_spec
            ], shell=True)
            break

    calver = datetime.utcnow().strftime('%Y.%m.%d')
    sha = next(iter(sha_date))
    tag = f'{calver}-{sha}'
    image_spec = f'{image}:{tag}'
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
        )
    else:
        # Build regular image
        r2d_build(
            args.image,
            image_spec,
            cache_from
        )
    docker_verify(args.image, image_spec)

    # Build onbuild image
    docker_build(
        f'{image_name}-onbuild:{tag}',
        'onbuild',
        {'BASE_IMAGE_SPEC': f'{image_name}:{tag}'}
    )


if __name__ == '__main__':
    main()
