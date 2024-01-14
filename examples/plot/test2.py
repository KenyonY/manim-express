import matplotlib.pyplot as plt
import numpy as np

from examples.example_imports import *



class PlotScene(EagerModeScene):
    def clip1(self):
        theta = np.linspace(0, np.pi*2, 300)
        r = 1
        x, y = r*np.cos(theta), r*np.sin(theta)

        # self.plot(x, y, axes_ratio=1)
        # self.plot(x, y)
        # self.show_plot()

        self.scatter2d(x, y, size=0.01)

        self.hold_on()


PlotScene().render()
