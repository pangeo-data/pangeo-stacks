import os

def test_start():
    assert os.environ['PANGEO_STACK'] == 'pangeo-notebook'

