from manim_express import *
from manimlib import *
from manim_express.scatter import *
from manim_express.plot import m_line, m_scatter
from manim_express.surface import CustomSurface
from manimlib.utils.rate_functions import linear, smooth, double_smooth, exponential_decay
from manim_express.math import *
from manim_express.nn import *

# CONFIG.color = rgb_to_hex([0.3, 0.4, 0.5]) # this will override the `color` option in custom_config.yml
CONFIG.gif = False
# SceneArgs.frame_rate = 60
CONFIG.uhd = True