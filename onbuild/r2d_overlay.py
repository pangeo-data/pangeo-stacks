#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse

NB_UID = int(os.environ.get('NB_UID', 1000))
REPO_DIR = os.environ['REPO_DIR']
# We copy contents of *child* image to a subdirectory temporarily
# This helps us apply customizations that were only from the
# child, and re-do the packages of the parent.
ONBUILD_CONTENTS_DIR = os.path.join(REPO_DIR, '.onbuild-child')

def become(uid):
    # FIXME: Uh, maybe not do this
    os.setgid(uid)
    os.setuid(uid)

def binder_path(path):
    if os.path.exists(os.path.join(ONBUILD_CONTENTS_DIR, 'binder')):
        return os.path.join(ONBUILD_CONTENTS_DIR, 'binder', path)
    return os.path.join(ONBUILD_CONTENTS_DIR, path)


def apply_environment():
    env_path = binder_path('environment.yml')
    if os.path.exists(env_path):
        return [
            f'conda env update -n root -f {env_path}',
            f'conda clean -tipsy',
            f'conda list -n root',
            f'rm -rf /srv/conda/pkgs'
        ]


def apply_requirements():
    req_path = binder_path('requirements.txt')
    env_path = binder_path('environment.yml')

    if os.path.exists(req_path) and not os.path.exists(env_path):
        return [
            f'python3 -m pip install --no-cache-dir -r {req_path}'
        ]


def apply_postbuild():
    pb_path = binder_path('postBuild')

    if os.path.exists(pb_path):
        return [
            f'chmod +x {pb_path}',
            f'./{pb_path}'
        ]


def build():
    applicators = [
        apply_environment,
        apply_requirements,
        apply_postbuild
    ]

    for applicator in applicators:
        commands = applicator()

        if commands:
            for command in commands:
                subprocess.check_call(
                    ['/bin/bash', '-c', command], preexec_fn=become(NB_UID)
                )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'action',
        choices=('build', 'start')
    )

    args = argparser.parse_args()

    if args.action == 'build':
        build()
    else:
        raise Exception("start isn't implemented yet")

if __name__ == '__main__':
    main()