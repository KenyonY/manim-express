from manim_express import EagerModeScene, Size, SceneArgs
from manim_express.plot import m_line, m_scatter
from manimlib import *
import matplotlib.pyplot as plt
import numpy as np
from manim_express.math import Quaternion, Vec3


SceneArgs.color = rgb_to_hex([0.3, 0.4, 0.5]) # this will coverride the `color` option in custom_config.yml
SceneArgs.gif = False
# SceneArgs.frame_rate = 60
SceneArgs.uhd = True

