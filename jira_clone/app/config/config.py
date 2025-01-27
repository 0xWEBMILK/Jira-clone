from dataclasses import dataclass
from configparser import ConfigParser

@dataclass
class DatabaseConfig:
    dev_url: str
    prod_url: str
    test_url: str

@dataclass
class ApplicationConfig:
    dev_mode: bool

@dataclass
class Config:
    database: DatabaseConfig
    application: ApplicationConfig


def get_config(path):
    config = ConfigParser()
    config.read(path+'config.ini')

    database_config = config['Database']
    application_config = config['Application']

    return Config(
        DatabaseConfig(
            dev_url=database_config.get('dev_url'),
            prod_url=database_config.get('prod_url'),
            test_url=database_config.get('test_url')
        ),
        ApplicationConfig(
            dev_mode=application_config.getboolean('dev_mode')
        )
    )