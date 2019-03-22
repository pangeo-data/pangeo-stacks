import pytest

packages = ['intake', 'gcsfs', 'xarray', 'netCDF4', 'rasterio']

@pytest.mark.parametrize('package_name', packages, ids=packages)
def test_import(package_name):
    __import__(package_name)

