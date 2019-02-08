import pytest
import dask.distributed.Client


@pytest.fixture(scope='module')
def client():
    with Client(n_workers=4) as dask_client:
        yield dask_client

def test_check_dask_version(client):
    print(client)
    versions = client.get_versions(check=True)
    assert len(versions) == 4
