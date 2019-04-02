import importlib

import pytest

packages = [
    # these are things we can't live without, just to be safe
    'dask', 'distributed'
    ]

@pytest.mark.parametrize('package_name', packages, ids=packages)
def test_import(package_name):
    importlib.import_module(package_name)
