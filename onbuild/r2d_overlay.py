#!/usr/bin/env python3
import subprocess
import sys
import os
import argparse
import re

NB_UID = int(os.environ.get('NB_UID', 1000))
REPO_DIR = os.environ['REPO_DIR']
# We copy contents of *child* image to a subdirectory temporarily
# This helps us apply customizations that were only from the
# child, and re-do the packages of the parent.
ONBUILD_CONTENTS_DIR = os.path.join(REPO_DIR, '.onbuild-child')


def become(uid):
    def wrap(func):
        def _pre_exec():
            # TODO: Look at the security of this very, very carefully
            os.setgid(uid)
            os.setuid(uid)
        func._pre_exec = _pre_exec
        return func
    return wrap

def binder_path(path):
    has_binder = os.path.isdir(os.path.join(ONBUILD_CONTENTS_DIR, "binder"))
    has_dotbinder = os.path.isdir(os.path.join(ONBUILD_CONTENTS_DIR, ".binder"))

    if has_binder and has_dotbinder:
        raise RuntimeError(
            "The repository contains both a 'binder' and a '.binder' "
            "directory. However they are exclusive."
        )

    if has_dotbinder:
        binder_dir =  ".binder"
    elif has_binder:
        binder_dir = "binder"
    else:
        binder_dir = ""

    return os.path.join(ONBUILD_CONTENTS_DIR, binder_dir, path)


@become(NB_UID)
def apply_environment():
    NB_PYTHON_PREFIX = os.environ['NB_PYTHON_PREFIX']
    env_path = binder_path('environment.yml')
    if os.path.exists(env_path):
        return [
            f'conda env update --verbose -p {NB_PYTHON_PREFIX} -f {env_path}',
            f'conda clean --all -f -y',
            f'conda list -p {NB_PYTHON_PREFIX}',
            f'rm -rf /srv/conda/pkgs'
        ]


@become(NB_UID)
def apply_requirements():
    req_path = binder_path('requirements.txt')
    env_path = binder_path('environment.yml')
    NB_PYTHON_PREFIX = os.environ['NB_PYTHON_PREFIX']
    if os.path.exists(req_path) and not os.path.exists(env_path):
        return [
            f'{NB_PYTHON_PREFIX}/bin/pip install --no-cache-dir -r {req_path}'
        ]


@become(NB_UID)
def apply_postbuild():
    pb_path = binder_path('postBuild')

    if os.path.exists(pb_path):
        return [
            f'chmod +x {pb_path}',
            # since pb_path is a fully qualified path, no need to add a ./
            f'{pb_path}'
        ]


@become(0)
def apply_apt():
    apt_path = binder_path('apt.txt')
    if os.path.exists(apt_path):
        with open(apt_path) as f:
            extra_apt_packages = []
            for l in f:
                package = l.partition('#')[0].strip()
                if not package:
                    continue
                # Validate that this is, indeed, just a list of packages
                # We're doing shell injection around here, gotta be careful.
                # FIXME: Add support for specifying version numbers
                if not re.match(r"^[a-z0-9.+-]+", package):
                    raise ValueError("Found invalid package name {} in "
                                        "apt.txt".format(package))
                extra_apt_packages.append(package)

        return [
            "apt-get -qq update",
            "apt-get install --yes --no-install-recommends {}".format(' '.join(extra_apt_packages)),
            "apt-get -qq purge",
            "apt-get -qq clean",
            "rm -rf /var/lib/apt/lists/*"
        ]

def build():
    applicators = [
        apply_apt,
        apply_environment,
        apply_requirements,
        apply_postbuild
    ]

    for applicator in applicators:
        commands = applicator()

        if commands:
            for command in commands:
                subprocess.check_call(
                    ['/bin/bash', '-c', command], preexec_fn=applicator._pre_exec
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
