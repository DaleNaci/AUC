import pathlib
import configparser

datafolder = (pathlib.Path(__file__).parent.absolute()).joinpath(pathlib.Path("Data")).resolve()

config = configparser.ConfigParser()
config.read(datafolder / 'database.ini')
document = config['DATABASE']['name']
admin = config['ROLES']['admin']
mod = config['ROLES']['mod']
strikechannel = int(config['CHANNELS']['strike'])

__all__ = ["commands", "database"]