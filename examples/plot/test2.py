import matplotlib.pyplot as plt
import numpy as np

from examples.example_imports import *



class PlotScene(EagerModeScene):
    def clip1(self):
        theta = np.linspace(0, np.pi*2, 1000)
        self.plot(np.cos(theta), np.sin(theta), axes_ratio=1)
        self.show_plot()

        self.hold_on()

PlotScene().render()