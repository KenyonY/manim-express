from manimlib import *
from manim_express import EagerModeScene
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(5*x)

# matplotlib
import matplotlib.pyplot as plt
plt.plot(x, y, color='green', linewidth=2)
plt.show()

# manim_express
from manim_express.utils import m_line, m_scatter
scene = EagerModeScene()

line = m_line(x, y, color=GREEN, width=2)
scene.add(line)
scene.hold_on()
