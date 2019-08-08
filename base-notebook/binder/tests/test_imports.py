import importlib
import sys
from distutils.version import LooseVersion
import pytest

packages = [
    # these are things we can't live without, just to be safe
    'dask', 'distributed'
    # jupyterhub and related utilities
    'jupyterhub', 'nbgitpuller'
    ]


@pytest.mark.parametrize('package_name', packages, ids=packages)
def test_import(package_name):
    importlib.import_module(package_name)


# for current repo2docker config
def test_conda_environment():
    assert sys.prefix == '/srv/conda/envs/notebook'


# would be better to automatically get these from environment.yml
def test_pinned_versions():
    import tornado
    import dask_kubernetes
    import dask_labextension

    assert LooseVersion(tornado.version) == LooseVersion('5.1.1')
    assert LooseVersion(dask_kubernetes.__version__) >= LooseVersion('0.8')
    assert LooseVersion(dask_labextension.__version__) == LooseVersion('0.3.1')
