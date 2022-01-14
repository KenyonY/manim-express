from .eager import EagerModeScene as GlEagerScene
from .backend.manimgl.express import CONFIG
from .backend.manimgl.express.surface import CustomSurface
from .points import *
from sparrow.file_ops import yaml_load
from sparrow.string.color_string import rgb_string
from sparrow.path import rel_to_abs
# import pkg_resources
# __version__ = pkg_resources.get_distribution(_version_config['name']).version

plan_root_path = __file__

_version_config = yaml_load(rel_to_abs("./version-config.yaml"))
__version__ = _version_config['version']

print(f"{rgb_string(_version_config['name'], color='#34A853')} version: {rgb_string(__version__, color='#C9E8FF')}")
