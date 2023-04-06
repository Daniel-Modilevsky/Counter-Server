class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///counter.db'


class TestConfig:
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///test.db'
