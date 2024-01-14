import cv2
from manimlib import *
from itertools import product
import numpy as np
from .coordinate_sys import SciAxes, SciAxes3D


class Scatter:
    def __init__(self):
        self._color_choice_list = [
            GREEN_C, BLUE_C, RED_C, YELLOW_C, ORANGE, GOLD_C, MAROON_C, TEAL_C
        ]
        self.ax_width = FRAME_WIDTH - 2
        self.ax_height = FRAME_HEIGHT - 2
        self.ax = None

    @staticmethod
    def get_min_max(a: np.ndarray, a_range):
        if a_range is None:
            amin, amax = a.min(), a.max()
        else:
            amin, amax = a_range
        # a_shift = (amax - amin) / 7
        # amin -= a_shift
        # amax += a_shift
        return amin, amax

    def from_dotcloud(self, x: np.ndarray, y: np.ndarray, size=0.05, color=BLUE,
                      ratio=0.618,
                      x_range=None, y_range=None,
                      ax_width=None, ax_height=None):

        if ax_height is None:
            ax_height = self.ax_height
        if ax_width is None:
            ax_width = ax_height * (1/ratio)

        assert len(x) == len(y)
        x, y = np.array(x), np.array(y)

        x_range = self.get_min_max(x, x_range)
        y_range = self.get_min_max(y, y_range)

        if self.ax is None:
            self.ax = SciAxes(x_range=x_range, y_range=y_range, width=ax_width, height=ax_height)
        points = [self.ax.c2p(i, j) for i, j in zip(x, y)]
        image_obj = DotCloud(points, radius=size, opacity=0.8).set_color(color)  # .set_color_by_rgba_func(rgba_func)
        return image_obj

    def from_dot_cloud_3d(self, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                          size=0.05, color=BLUE,
                          x_range=None, y_range=None, z_range=None,
                          ax_width=None, ax_height=None):
        if ax_width is None:
            ax_width = self.ax_width
        if ax_height is None:
            ax_height = self.ax_height

        assert len(x) == len(y)
        assert len(x) == len(z)
        x, y, z = np.array(x), np.array(y), np.array(z)
        x_range = self.get_min_max(x, x_range)
        y_range = self.get_min_max(y, y_range)
        z_range = self.get_min_max(z, z_range)
        if self.ax is None:
            self.ax = ThreeDAxes(x_range=x_range, y_range=y_range, z_range=z_range,
                                 width=ax_width, height=ax_height)
            labels = VGroup(
                self.ax.get_x_axis_label("x"),
                self.ax.get_y_axis_label("y"),
                self.ax.get_axis_label("z", self.ax.get_z_axis(),
                                       edge=OUT,
                                       direction=DOWN).rotate(90 * DEGREES, RIGHT),
            )
            self.ax.add(labels)
        points = [self.ax.c2p(i, j, k) for i, j, k in zip(x, y, z)]
        scatters = DotCloud(points, radius=size).set_color(color)
        return scatters

    def from_vobj(self):
        pass


def image_arr_obj(arr: np.ndarray, style=0, scale_factor=None):
    """
    使用DotCloud (shader上直接渲染) 性能较好, 但因为每个像素是点, 所以经常出现摩尔纹
    """

    def rgb2gray(R, G, B):
        return 0.2989 * R + 0.5870 * G + 0.1140 * B

    if arr.ndim == 2:
        arr = cv2.cvtColor(arr, cv2.COLOR_GRAY2RGB)
    row, col = arr.shape[:2]
    if scale_factor is None:
        scale_factor = max(6 / min(row, col), 0.007)
    xy = np.array(list(product(np.arange(col), np.arange(row))))

    color_dim = len(arr[0, 0])
    if color_dim >= 3 and style == 0:
        points = [(*i * scale_factor, 2 * rgb2gray(*arr[i[0], i[1]][:3])) for i in xy]
    else:
        points = [(*i * scale_factor, 0) for i in xy]

    def rgba_func(point):
        """因为set_color_by_rgba_func传入的必须是point参数, 或者说
        因为DotCloud目前的缩小是通过降采样实现, 那么原本如果以index作为位置时, 在降采样时会导致十分稀疏的有效颜色选中,
         所以要缩小只能通过在最开始时缩放points的坐标来实现.
        所以才有了这里scale_factor的相关诡异操作.
        """
        x, y = round(point[0] / scale_factor), round(point[1] / scale_factor)
        if color_dim == 3:
            return [*arr[y, x], 1]
        else:  # dim=4
            return arr[y, x]

    image_obj = DotCloud(points, radius=scale_factor / 2).set_color_by_rgba_func(rgba_func)
    image_obj.flip(RIGHT).move_to(ORIGIN)
    return image_obj


def imobj_square(img: np.ndarray):
    """
    性能很低, 使用Square对img矩阵中每个点进行填充
    """
    height, width = img.shape[:2]
    if np.any(img > 1):
        img = img / 255
    pixel_array = VGroup(*[
        Square(fill_color=rgb_to_hex(img[i, j]), fill_opacity=1)
        for i in range(height)
        for j in range(width)
    ])
    pixel_array.arrange_in_grid(height, width, buff=0)
    pixel_array.set_height(6)
    pixel_array.set_stroke(WHITE, 0)
    return pixel_array
