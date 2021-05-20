from manimlib import *
from manim_express import EagerModeScene, Size, SceneArgs
import numpy as np

x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(5*x)

# matplotlib
import matplotlib.pyplot as plt
plt.plot(x, y, color='green', linewidth=2)
plt.show()

# manim_express
from manim_express.utils import m_line, m_scatter
SceneArgs.color="#222222"
scene = EagerModeScene(screen_size=Size.big)

line = m_line(x, y, color=GREEN, width=2)
scene.add(line)
scene.hold_on()
