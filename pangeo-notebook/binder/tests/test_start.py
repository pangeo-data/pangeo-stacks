from os import environ

def test_start():
    if environ.get('PANGEO_STACK') is not None:
        assert os.environ['PANGEO_STACK'] == 'pangeo-notebook'
