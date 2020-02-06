import importlib

import pytest

packages = [
    # these are problem libraries that don't always seem to import, mostly due
    # to dependencies outside the python world
    'netCDF4', 'h5py', 'rasterio', 'geopandas', 'cartopy', 'geoviews',
    # these are things we can't live without, just to be safe
    'gcsfs', 's3fs', 'xarray', 'intake', 'dask', 'distributed',
    ]

@pytest.mark.parametrize('package_name', packages, ids=packages)
def test_import(package_name):
    importlib.import_module(package_name)
