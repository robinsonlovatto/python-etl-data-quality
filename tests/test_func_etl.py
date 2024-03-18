from app.etl import configuration, extract, load, transformation


def test_config():
    assert configuration() == 'postgres pass'