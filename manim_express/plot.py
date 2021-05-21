import numpy as np
from manimlib import *


def m_line(x,
           y,
           z=None,
           axes=None,
           color=None,
           width=None,
           optacity=None,
           background=None):
    """point data to line"""
    L = len(x)
    x, y = np.array(x), np.array(y)
    if z is None:
        z = np.zeros(x.shape)
    if axes is None:
        # last_little_line = Line([x[L - 1], y[L - 1], z[0]], [x[0], y[0], z[0]])
        line = VGroup(*[
            Line([x[i], y[i], 0], [x[i + 1], y[i + 1]]).set_stroke(
                color=color,
                width=width,
                opacity=optacity,
                background=background) for i in range(len(x) - 1)
        ])
    elif type(axes) is Axes:
        # last_little_line = Line(axes.c2p(x[L - 1], y[L - 1]),
        #                         axes.c2p(x[0], y[0]))
        line = VGroup(*[
            Line(axes.c2p(x[i], y[i]), axes.c2p(x[i + 1], y[
                i + 1])).set_stroke(color=color,
                                    width=width,
                                    opacity=optacity,
                                    background=background)
            for i in range(len(x) - 1)
        ])
    else:  # ThreeDAxes
        # last_little_line = Line(axes.c2p(x[L - 1], y[L - 1], z[0]),
        #                         axes.c2p(x[0], y[0], z[0])).set_stroke(
        #     color=color, width=width, opacity=optacity, background=background)

        line = VGroup(*[
            Line(axes.c2p(x[i], y[i], z[i]), axes.c2p(x[i + 1], y[
                i + 1], z[i])).set_stroke(color=color,
                                          width=width,
                                          opacity=optacity,
                                          background=background)
            for i in range(len(x) - 1)
        ])
    return line


def m_scatter(x, y, z=None, axes=None):
    """for scatter plot"""
    x, y = np.array(x), np.array(y)
    if z is None:
        z = np.zeros(x.shape)
    dots = VGroup(
        *
        [Dot(radius=.01).move_to([xi, yi, zi]) for xi, yi, zi in zip(x, y, z)])

    return dots


class Plot:
    def __init__(self):
        self._axes = None
        self._xmin = np.Inf
        self._xmax = -np.inf
        self._ymin = np.Inf
        self._ymax = -np.inf
        self._unit_x = 0
        self._unit_y = 0
        self._xdata = []
        self._ydata = []
        self._color_list = []
        self._width_list = []
        self._axes_line_list = []
        self._axes_width = 10
        self._axes_height = 6.2
        self._axes_ratio = 0.62
        self._show_axes = True

    def create_axes(self, x_label_min, x_label_max, y_label_min, y_label_max):
        x_length = x_label_max - x_label_min
        y_length = y_label_max - y_label_min
        dx = x_length / 20
        dy = y_length / 15

        xmin, xmax = x_label_min - EPSILON, x_label_max + dx
        ymin, ymax = y_label_min - EPSILON, y_label_max + dy

        n_x, n_y = 10, 5
        if self._axes_ratio == 1:
            tick_ratio = (ymax-ymin)/(xmax-xmin)
        else:
            tick_ratio = self._axes_ratio

        self._axes_height = self._axes_width * tick_ratio

        if self._axes_height > 7:
            self._axes_height = 7
            self._axes_width = self._axes_height / tick_ratio
        axes = Axes(
            y_range=(y_label_min, ymax, (ymax - ymin) / n_y),
            x_range=(xmin, xmax, (xmax - xmin) / n_x),
            height=self._axes_height,
            width=self._axes_width,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "numbers_to_exclude": [],
                "stroke_color": GREY_A,
                "stroke_width": 1,
            },
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config={
                "include_tip": True,
            }
        )
        axes.add_coordinate_labels(
            x_values=set(np.linspace(x_label_min - EPSILON, x_label_max, 10)).add(0),
            y_values=set(np.linspace(y_label_min, y_label_max, 7)).add(0),
            font_size=20,
            num_decimal_places=1,
        )

        self._unit_y = axes.c2p(0, 1)[1] - axes.c2p(0, 0)[1]
        self._unit_x = axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]

        axes.x_axis.shift(UP * self._unit_y * y_label_min)
        axes.y_axis.shift(RIGHT * self._unit_x * x_label_min)

        self._axes = axes
        
    def get_axes(self):
        return self._axes

    def get_axes_lines(self):
        return self._axes_line_list

    def gen_axes_lines(self):
        self.create_axes(x_label_min=self._xmin, x_label_max=self._xmax,
                         y_label_min=self._ymin, y_label_max=self._ymax)
        # midx = (self._xmin + self._xmax) / 2
        # midy = (self._ymin + self._ymax) / 2
        # frame = scene.camera.frame
        # frame.move_to(self._axes.c2p(midx, midy))
        for x, y, color, width in zip(self._xdata, self._ydata, self._color_list, self._width_list):
            line = m_line(x, y, color=color, width=width, axes=self._axes)
            axes_line = VGroup(line, self._axes) if self._show_axes else line
            line.shift(-self._unit_x * self._xmin * RIGHT)
            self._axes_line_list.append(axes_line)

    def plot(self, x, y, color=None, width=None, axes_ratio=0.618, show_axes=True):
        self._show_axes = show_axes
        self._xmin = min(self._xmin, min(x))
        self._xmax = max(self._xmax, max(x))
        self._ymin = min(self._ymin, min(y))
        self._ymax = max(self._ymax, max(y))

        self._xdata.append(x)
        self._ydata.append(y)
        self._color_list.append(color)
        self._width_list.append(width)

        self._axes_width = 10
        self._axes_height = 0.62 * self._axes_width
        self._axes_ratio = axes_ratio

