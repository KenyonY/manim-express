from examples.example_imports import *
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0,0.006, 100)
x = np.cos(theta)
y = np.sin(theta)
plt.plot(theta, y)
plt.show()
# CONFIG.preview=True
# scene = EagerModeScene()
# axes = Axes(x_range=[-3, 100, 10], y_range=(-1, 80, 10))
# axes.add_coordinate_labels()
# scene.play(Write(axes, lag_ratio=0.01))
# scene.plot(x, y, )
# scene.show_plot()

# scene.hold_on()
