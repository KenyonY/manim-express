import numpy as np

from tests_import import *


class Text_AutoAxes(EagerModeScene):
    def clip2(self):
        # number_line = SciNumberLine([-0.55, -0.5])
        # self.add(number_line.move_to(UP*3))

        ax = SciAxes((-3, 7), (-0, 10), height=8, width=8)
        self.add(ax)

        circle = ax.get_parametric_curve(
            lambda theta: [np.cos(theta), np.sin(theta)],
        ).move_to(RIGHT*3)

        circle2 = ParametricCurve(
            lambda theta: ax.c2p(np.cos(theta), np.sin(theta)),
            t_range=[-3, 7]
        ).move_to(LEFT*2)
        self.write(circle)
        self.write(circle2)

        # sin_graph = ax.get_graph(
        #     lambda x: 2 * math.sin(x),
        #     color=BLUE,
        # )
        # self.show_creation(sin_graph)
        relu_graph = ax.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # self.write(relu_graph)

    def clip11(self):
        theta = np.linspace(0, np.pi * 2, 100)
        x, y = np.cos(theta), np.sin(theta)
        self.plot(x, y, axes_ratio=1)
        pltobj = self.show_plot()
        self.wait()
        self.fade_out(pltobj)


CONFIG.preview = True
Text_AutoAxes().render()
