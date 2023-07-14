import os
import string

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_config(mode):
    if mode == 'prod':
        return ProductionConfig()
    elif mode == 'test':
        return TestingConfig()
    else:
        return DevelopmentConfig()


class Config():
    DEBUG = False
    TESTING = False

    MAX_NUM_WORKERS = 3
    PASSWORD_LEN = int(os.environ.get('PASSWORD_LEN', 3))
    SIZE_OF_ALPHABET = len(string.ascii_letters)
    CHECK_IN_PERIOD_SEC = 3
    JOB, ACK_JOB, PING, NOT_DONE, DONE_NOT_FOUND, DONE_FOUND, SHUTDOWN = range(1, 8)
    # # Logging
    # LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)


class DevelopmentConfig(Config):
    CONFIG_TYPE = 'dev'
    DEBUG = True


class ProductionConfig(Config):
    CONFIG_TYPE = 'prod'
    # TODO: add port settings


class TestingConfig(Config):
    CONFIG_TYPE = 'test'
    TESTING = True
