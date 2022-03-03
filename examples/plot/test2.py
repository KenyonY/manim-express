import matplotlib.pyplot as plt
from examples.example_imports import *



class PlotScene(EagerModeScene):
    def clip1(self):
        axes = Axes(
            x_range=(1., 1.521, 0.1),
            y_range=(0, 10, 0.1),
        )
        self.add(axes)
        axes.add_coordinate_labels()
        x = np.linspace(1.234, 1.521, 100)
        self.hold_on()

x = np.linspace(-101, 1000, 1000)
scene = EagerModeScene()

# scene.plot(x, x)
# scene.show_plot()
# number_line = NumberLine((0.01, 0.02, ))
number_line = SciNumberLine((100, 200.2, 1), )
number_line.add_numbers()
scene.add(number_line)

scene.hold_on()


# PlotScene().render()
