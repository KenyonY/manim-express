from manimlib import *
from itertools import product


def image_arr_obj(arr, style=0, scale_factor=None):
    """
    使用DotCloud (shader上直接渲染) 性能较好, 但因为每个像素是点, 所以经常出现摩尔纹
    """

    def rgb2gray(R, G, B):
        return 0.2989 * R + 0.5870 * G + 0.1140 * B

    row, col = arr.shape[:2]
    if scale_factor is None:
        scale_factor = max(6 / min(row, col), 0.007)
    xy = np.array(list(product(np.arange(col), np.arange(row))))

    if len(arr[0, 0]) >= 3 and style == 0:
        points = [(*i * scale_factor, 2 * rgb2gray(*arr[i[0], i[1]][:3])) for i in xy]
    else:
        points = [(*i * scale_factor, 0) for i in xy]

    color_dim = len(arr[0, 0])

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
