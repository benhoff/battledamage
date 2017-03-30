from os import path as _path
from os import mkdir as _mkdir

from battle_damage.database_models import Base


def _get_config_filepath():
    home_directory = _path.expanduser('~')
    config = _path.abspath(_path.join(home_directory,
                                      '.config'))

    return config


def get_database_filepath():
    config = _get_config_filepath()
    battle_path = _path.join(config, 'battledamage')

    return battle_path


def get_sqlite_url():
    battle_path = get_database_filepath()
    return 'sqlite:///{}'.format(battle_path)


def make_database():
    config = _get_config_filepath()
    battle_path = get_database_filepath()

    if not _path.isdir(config):
        _mkdir(config)
    if not _path.isdir(battle_path):
        _mkdir(battle_path)

    battle_database = _path.join(battle_path, 'materials.sqlite')

    if not _path.isfile(battle_database):
        engine = _create_engine('sqlite:///{}'.format(database_filepath))
        Base.metadata.create_all(engine)
