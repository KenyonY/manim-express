import numpy as np

from examples.example_imports import *
from manim_express import *
from hilbert import decode, encode #$ pip install numpy-hilbert-curve
import cv2


def get_hilbert_1d_array(image: np.ndarray):
    num_dims = 2
    num_bits = np.log2(image.shape[0] * image.shape[1]) / num_dims
    num_bits = int(num_bits)
    max_hil = 2 ** (num_bits * num_dims)
    hilberts = np.arange(max_hil)
    locs = decode(hilberts, num_dims, num_bits)

    image1d = []
    for coord in locs:
        image1d.append(image[coord[0], coord[1]])
    return np.array(image1d)[None, ...]


class HilbertScene(EagerModeScene):
    def __init__(self):
        super().__init__()

    def clip1(self):
        # theta = np.linspace(0, 2 * PI, 50)
        # x = np.cos(theta)
        # y = np.sin(theta)
        # points = xyz_to_points(x, y)
        # dc = DotCloud(points, color=GREEN_C)
        # self.add(dc)
        import cv2
        # image = imageio.imread("../../data/pic/code0.png")
        # image_path = rel_to_abs("../../data/pic/USST_logo.svg.png", return_str=True)
        image_path = rel_to_abs("../../data/pic/hilbert_0.jpg", return_str=True)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (32, 32))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image1d = get_hilbert_1d_array(image)
        image_obj = imobj_square(image1d).scale(0.002).move_to(DOWN*2)
        image_obj.apply_complex_function(lambda x: np.sin(x))
        # image_obj.apply_function(lambda p:[
        #     p[0] + 0.5 * np.sin(p[1]),
        #     p[1] + 0.5 * np.sin(p[0]),
        #     p[2]
        # ] )
        self.add(image_obj)
        self.add(ImageMobject(image_path).scale(0.5))



HilbertScene().render()
