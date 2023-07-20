from config import get_config, ProductionConfig, TestingConfig, DevelopmentConfig


# Tests that get_config returns ProductionConfig object when mode is 'prod'
def test_production_config():
    assert isinstance(get_config('prod'), ProductionConfig)


# Tests that get_config returns TestingConfig object when mode is 'test'
def test_testing_config():
    assert isinstance(get_config('test'), TestingConfig)


# Tests that get_config returns DevelopmentConfig object when mode is not 'prod' or 'test'
def test_development_config():
    assert isinstance(get_config('dev'), DevelopmentConfig)


# Tests that get_config returns DevelopmentConfig object when mode is None
def test_development_config_none():
    assert isinstance(get_config(None), DevelopmentConfig)


# Tests that get_config returns DevelopmentConfig object when mode is an empty string
def test_development_config_empty_string():
    assert isinstance(get_config(''), DevelopmentConfig)


# Tests that get_config returns DevelopmentConfig object when mode is an invalid string
def test_development_config_invalid_string():
    assert isinstance(get_config('invalid'), DevelopmentConfig)


