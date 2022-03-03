from manim_express import *
from manim_express.backend.manimgl.express.scatter import *
from manim_express.backend.manimgl.express.plot import m_line, m_scatter
from manim_express.backend.manimgl.express.surface import CustomSurface
from manim_express.backend.manimgl.express.eager import EagerModeScene, CONFIG, Size
from manim_express.backend.manimgl.express.plot import *
from manimlib import *
from manim_express.hand_draw import *
from manimlib.utils.rate_functions import linear, smooth, double_smooth, exponential_decay
from manim_express.math import Quaternion, Vec3
from manim_express.backend.manimgl.express import SciNumberLine


CONFIG.preview = True
CONFIG.color = rgb_to_hex([0.3, 0.4, 0.5]) # this will override the `color` option in custom_config.yml
CONFIG.gif = False
# SceneArgs.frame_rate = 60
CONFIG.uhd = True

