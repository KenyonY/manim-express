import random

import numpy as np

from examples.example_imports import *

scene = EagerModeScene()

grid = NumberPlane((-10, 10), (-5, 5))
matrix = [[1, 1], [0, 1]]

c_grid = ComplexPlane()
# moving_c_grid = c_grid.copy()
# moving_c_grid.prepare_for_nonlinear_transform()
# scene.play(ShowCreation(c_grid))
# c_grid.prepare_for_nonlinear_transform()
# c_grid.set_stroke(BLUE_E, 1)
# c_grid.add_coordinate_labels(font_size=24)


be_applyed_arrow = Arrow(buff=0).scale(3).move_to(UP).set_color(RED)
grid.add(be_applyed_arrow)
grid.prepare_for_nonlinear_transform()

# scene.play(ShowCreation(grid))
# scene.wait(1)

# scene.play(
#     grid.animate.apply_function(
#         lambda p: [
#             p[0] + 0.5 * math.cos(p[1]),
#             p[1] + 0.5 * math.sin(p[0]),
#             p[2]
#         ]
#     ),
#     run_time=2,
# )


def complex2real_image(complex_xy):
    real, image = [], []
    for xy in complex_xy:
        real.append(xy.real)
        image.append(xy.imag)
    return real, image


def xy2complex(x, y):
    complex_xy = []
    for i, j in zip(x, y):
        complex_xy.append(complex(i, j))
    return complex_xy




# def random_trigonometric(x, n=5, w_min=1, w_max=20, intensity=0.003):
#     # theta = np.linspace(0, np.pi * 2, N)
#     N = len(x)
#     delta_w = w_max - w_min
#     wave = np.array([0.] * N)
#     for i in range(n):
#         w = w_min + random.random() * delta_w
#         phi = np.random.rand() * 2*np.pi * w
#         pth_pwave = np.sin(w * x + phi) * intensity
#         wave += pth_pwave
#     return wave


def apply_func(x, y, **kwargs):
    x, y = np.array(x), np.array(y)
    # res_x = [i + np.random.rand() for i in x]
    # res_y = [j + np.random.rand() for j in y]
    # res_x = x + np.sin(y)
    # res_y = y + np.sin(x)
    res_x = x + random_trigonometric(y, **kwargs)
    res_y = y + random_trigonometric(x, **kwargs)
    return res_x, res_y
theta = np.linspace(0, 2 * PI, 100)
x = np.cos(theta)
y = np.sin(theta)
scene.plot(*apply_func(x, y, intensity=0.01),
           axes_ratio=1
           )
# scene.plot(theta, random_trigonometric(theta, 5, intensity=0.002))
scene.show_plot()

scene.hold_on()
