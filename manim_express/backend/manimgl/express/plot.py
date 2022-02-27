from manimlib import *
from ....utils.tools import calc_number_step
from ...tick import Ticker
from .coordinate_sys import NewAxes


def m_line(x,
           y,
           z=None,
           axes=None,
           color=None,
           width=None,
           optacity=None,
           background=None):
    """point data to line"""
    x, y = np.array(x), np.array(y)
    line = PlotObj(x, y, z, axes).set_stroke(
        color=color,
        width=width,
        opacity=optacity,
        background=background
    )
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
        self.num = 0
        self._axes: Axes = None
        self._axes_labels = []
        self._xmin = np.Inf
        self._xmax = -np.inf
        self._ymin = np.Inf
        self._ymax = -np.inf
        self._unit_x = 0
        self._unit_y = 0
        self._xdata = []
        self._ydata = []
        self._color_list = []
        self._color_choice_list = [
            GREEN_C, BLUE_C, RED_C, YELLOW_C, ORANGE, GOLD_C, MAROON_C, TEAL_C
        ]
        self._width_list = []
        self._axes_line_list = []
        self._axes_width = 10
        self._axes_height = 6.2
        self._axes_ratio = 0.62
        self._scale_ratio = None
        self._num_decimal_places = None
        self._show_axes = True
        self._include_tip = True
        self._x_label = 'x'
        self._y_label = 'y'

    def create_axes(self, x_label_min, x_label_max, y_label_min, y_label_max):

        x_length = x_label_max - x_label_min
        y_length = y_label_max - y_label_min
        x_ticker = Ticker(x_label_max, x_label_min, steps_range=(5, 9))
        y_ticker = Ticker(y_label_max, y_label_min, steps_range=(5, 8))

        """
         * 确定x, y轴比例
         * 当前轴在屏幕中的长度是多少: L
         * 这个长度适合显示多少个刻度标签: N
         * 如何分配这N个标签, 即N个具体数值
         * 每个数值应显示的有效位数 可通过小数点末位的零来判断 
        """

        # n_x = 10
        # n_y = n_x * tick_ratio
        # x_step = x_length / n_x
        # y_step = y_length / n_y
        n_step_x, x_step = calc_number_step(x_length)
        n_step_y, y_step = calc_number_step(y_length)

        def adjust_axes_ratio(x_length, y_length):
            if self._scale_ratio is not None:
                tick_ratio = self._scale_ratio * y_length / x_length
            else:
                tick_ratio = self._axes_ratio

            self._axes_height = self._axes_width * tick_ratio

            if self._axes_height > 7:
                self._axes_height = 7
                self._axes_width = self._axes_height / tick_ratio
            return tick_ratio

        tick_ratio = adjust_axes_ratio(x_length, y_length)
        # FIXME: stupid here
        if n_step_y / n_step_x > tick_ratio + 0.3:
            y_step *= 5
        xmin, xmax = x_label_min - EPSILON, x_label_max + x_step / 2
        ymin, ymax = y_label_min - EPSILON, y_label_max + y_step / 2
        adjust_axes_ratio(xmax - xmin, ymax - ymin)

        def get_exponent_num(number):
            def get_error_remain(num, n):
                approx_num = round(num, n)
                return abs(approx_num - num)

            if get_error_remain(number, 0) < 1e-2:
                return 0
            if get_error_remain(number, 1) < 1e-2:
                return 1
            else:
                return 2

        if self._num_decimal_places is not None:
            x_num_decimal_place = self._num_decimal_places[0]
            y_num_decimal_place = self._num_decimal_places[1]
        else:
            x_num_decimal_place = min(max(get_exponent_num(x_label_min), get_exponent_num(x_step)), 2)
            y_num_decimal_place = min(max(get_exponent_num(y_label_min), get_exponent_num(y_step)), 2)

        axes = NewAxes(
            x_range=(xmin, xmax, x_step),
            y_range=(y_label_min, ymax, y_step),
            height=self._axes_height,
            width=self._axes_width,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config={
                "numbers_to_exclude": [],
                "stroke_color": GREY_A,
                "stroke_width": 0.3,
                "include_tip": self._include_tip,
            },
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            x_axis_config={
                "tip_config": {"width": 0.1, "length": 0.25},
                "decimal_number_config": {
                    "num_decimal_places": x_num_decimal_place,
                    "font_size": 15,
                },
            },
            y_axis_config={
                "tip_config": {"width": 0.15, "length": 0.3},
                "decimal_number_config": {
                    "num_decimal_places": y_num_decimal_place,
                    "font_size": 15,
                },
            },

        )

        axes.add_coordinate_labels()

        self._unit_y = axes.c2p(0, 1)[1] - axes.c2p(0, 0)[1]
        self._unit_x = axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]

        axes.x_axis.shift(UP * self._unit_y * y_label_min)
        axes.y_axis.shift(RIGHT * self._unit_x * x_label_min)

        self._axes = axes

    def get_axes(self):
        return self._axes

    def get_axes_lines(self):
        return {"line": self._axes_line_list, "axes": self._axes_labels}

    def gen_axes_lines(self):
        self.create_axes(x_label_min=self._xmin,
                         x_label_max=self._xmax,
                         y_label_min=self._ymin,
                         y_label_max=self._ymax)
        # midx = (self._xmin + self._xmax) / 2
        # midy = (self._ymin + self._ymax) / 2
        # frame = scene.camera.frame
        # frame.move_to(self._axes.c2p(midx, midy))
        for x, y, color, width in zip(self._xdata, self._ydata,
                                      self._color_list, self._width_list):
            line = m_line(x, y, color=color, width=width, axes=self._axes)

            labels = VGroup(
                self._axes.get_axis_label(self._x_label,
                                          self._axes.get_x_axis(),
                                          edge=RIGHT,
                                          direction=RIGHT).scale(0.8),
                self._axes.get_axis_label(self._y_label,
                                          self._axes.get_y_axis(),
                                          edge=UP,
                                          direction=UP).scale(0.8),
            )
            self._axes_labels = VGroup(self._axes,
                                       labels) if self._show_axes else []
            self._axes_line_list.append(line)

            line.shift(-self._unit_x * self._xmin * RIGHT)

    def plot(
            self,
            x,
            y,
            color=None,
            width=None,
            axes_ratio=0.618,
            scale_ratio=None,
            show_axes=True,
            include_tip=True,
            num_decimal_places=None,
            x_label='x',
            y_label='y',
    ):
        self.num += 1
        self._show_axes = show_axes
        self._xmin = min(self._xmin, min(x))
        self._xmax = max(self._xmax, max(x))
        self._ymin = min(self._ymin, min(y))
        self._ymax = max(self._ymax, max(y))

        self._xdata.append(x)
        self._ydata.append(y)
        if color is None:
            color = self._color_choice_list[self.num %
                                            len(self._color_choice_list) - 1]
        self._color_list.append(color)
        self._width_list.append(width)

        self._num_decimal_places = num_decimal_places
        self._axes_ratio = axes_ratio
        self._scale_ratio = scale_ratio
        self._include_tip = include_tip
        self._x_label = x_label
        self._y_label = y_label


class PlotObj(VMobject):
    InstantCount = 0
    CONFIG = {
        "epsilon": 1e-8,
        "discontinuities": [],
        "use_smoothing": True,
    }

    def __init__(self, x, y, z=None, axes=None, **kwargs):
        PlotObj.InstantCount += 1
        digest_config(self, kwargs)
        self.points = xyz_to_points(x, y, z, axes)
        VMobject.__init__(self, **kwargs)

    def init_points(self):
        x = self.points[:, 0]
        t_min, t_max = x.min(), x.max()

        jumps = np.array(self.discontinuities)
        jumps = jumps[(jumps > t_min) & (jumps < t_max)]
        boundary_times = [t_min, t_max, *(jumps - self.epsilon), *(jumps + self.epsilon)]
        boundary_times.sort()
        for t1, t2 in zip(boundary_times[0::2], boundary_times[1::2]):
            points = self.points
            self.start_new_path(points[0])
            self.add_points_as_corners(points[1:])
        if self.use_smoothing:
            self.make_approximately_smooth()
        return self


def xyz_to_points(x, y, z=None, axes=None):
    """Generalized c2p"""
    assert len(x) == len(y)
    if z is None:
        z = np.zeros(len(x))
    if axes is not None:
        if type(axes) is NewAxes:
            # axes: Axes
            points = np.array([axes.c2p(i, j) for i, j in zip(x, y)])
        else:
            axes: ThreeDAxes
            points = np.array([axes.c2p(i, j, k) for i, j, k in zip(x, y, z)])
    else:
        points = np.stack([x, y, z], 1)
    return points
