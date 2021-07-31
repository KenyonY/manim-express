from .eager import *
from .surface import CustomSurface
from sparrow.file_ops import yaml_load, ppath


_config = yaml_load(ppath("version-config.yaml"))
__version__ = _config["version"]
print(f"{_config['name']} version: {__version__}")
