import time

from manimlib import *


def gen_points(n_points=1, x_range=(-1, 1), y_range=(-1, 1), z_range=(0, 0), color_list=None, size=1):
    np.random.seed(int(time.time()))
    dx = x_range[1] - x_range[0]
    dy = y_range[1] - y_range[0]
    dz = z_range[1] - z_range[0]
    x = x_range[0] + dx * np.random.random(n_points)
    y = y_range[0] + dy * np.random.random(n_points)
    z = z_range[0] + dz * np.random.random(n_points)
    if color_list is None:
        color_list = it.cycle([RED, GREEN, BLUE, GOLD, MAROON_E, TEAL_E, PURPLE_C])
    else:
        color_list = it.cycle(color_list)

    return VGroup(*[Dot([i, j, k]).scale(size).set_color(color) for i, j, k, color in zip(x, y, z, color_list)])


def sphere2cart(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


def gen_sphere_points(n_points=1, r_range=(0, 1), theta_range=(0,  PI), phi_range=(0, 2*PI),
                      size=0.05, color_list=None, resolution=(10, 10)):
    dr = r_range[1] - r_range[0]
    dtheta = theta_range[1] - theta_range[0]
    dphi = phi_range[1] - phi_range[0]

    # TODO: For `r`, here is not uniform distribution
    R = r_range[0] + dr * np.random.random(n_points)
    THETA = theta_range[0] + dtheta * np.random.random(n_points)
    PHI = phi_range[0] + dphi * np.random.random(n_points)
    if color_list is None:
        color_list = it.cycle([RED, GREEN, BLUE, GOLD, MAROON_E, TEAL_E, PURPLE_C])
    else:
        color_list = it.cycle(color_list)
    points = Group()
    for r, theta, phi, color in zip(R, THETA, PHI, color_list):
        x, y, z = sphere2cart(r, theta, phi)
        points.add(Sphere(radius=size, resolution=resolution, color=color).move_to([x, y, z]))
    return points
