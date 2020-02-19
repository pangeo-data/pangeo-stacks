import os

def test_start():
    print(os.environ)
    if os.environ.get('PANGEO_STACK') is not None:
        assert os.environ['PANGEO_STACK'] == 'pangeo-notebook'
