from .eager import *
from .surface import CustomSurface
from .points import *
from sparrow.file_ops import yaml_load, ppath
from sparrow.color_str import rgb_string

plan_root_path = __file__

_version_config = yaml_load(ppath("version-config.yaml", __file__))
__version__= _version_config['version']
print(f"{rgb_string(_version_config['name'], color='#34A853')} version: {rgb_string(__version__, color='#C9E8FF')}")
