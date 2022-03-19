from manim_express import *
from manim_express.eager import EagerModeScene, Size
from manimlib import *
from manim_express.backend.manimgl.express.scatter import *
from manim_express.backend.manimgl.express.plot import m_line, m_scatter
from manim_express.backend.manimgl.express.surface import CustomSurface
from manimlib.utils.rate_functions import linear, smooth, double_smooth, exponential_decay
from manim_express.math import *
from manim_express.nn import *
from manim_express.backend.tick import Ticker
from manim_express.backend.manimgl.express.coordinate_sys import *



# CONFIG.color = rgb_to_hex([0.3, 0.4, 0.5]) # this will override the `color` option in custom_config.yml
CONFIG.gif = False
# SceneArgs.frame_rate = 60
CONFIG.uhd = True