from manim_imports_ext import *


def createRay(start, end):
    """
    start: 2d point coordinate
    end: 2d point coordinate
    """
    ray = Arrow(
        np.array([start[0], start[1], 0]),
        np.array([end[0], end[1], 0]),
        buff=0
    )
    ray.set_stroke(color=BLACK, width=1, opacity=1)
    return ray


def getCircPos(R, Origin, x=None, y=None, unit=1):
    if x is not None:
        root = abs(R ** 2 - (x - Origin[0]) ** 2) ** 0.5
        y = unit * root + Origin[1]  # unit=1,上侧的根
        return x, y
    elif y is not None:
        root = abs(R ** 2 - (y - Origin[1]) ** 2) ** 0.5

        x = unit * root + Origin[0]  # unit=1,右侧的根
        return x, y

    else:
        return ValueError


def sphere(origin, r):
    sphere0 = ParametricSurface(
        lambda u, v: np.array([
            r * np.cos(u) * np.cos(v) - origin[0],
            r * np.cos(u) * np.sin(v) - origin[1],
            r * np.sin(u) - origin[2]
        ]),
        v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
        # checkerboard_colors=[RED_D, RED_E],
        # resolution=(15, 32)
    )
    return sphere0


def circ(origin, r):
    circle = ParametricCurve(
        lambda theta: np.array([
            r * np.cos(theta) + origin[0],
            r * np.sin(theta) + origin[1],
            origin[2]
        ]),
        [0, 2 * TAU],
        color=RED
    )
    return circle


def get_circ_normal(point, origin):
    '''3d inputs'''
    print(point, origin, 'point and origin')
    point, origin = np.array(point), np.array(origin)
    normal = np.array([point[0] - origin[0], point[1] - origin[1], point[2] - origin[2]])
    return normalize(normal)


def reflect(direction, normal, p):
    direction = np.array(direction)
    normal = np.array(normal)
    angle = angle_between_vectors(direction, normal)
    if p == 0:
        angle = angle if np.pi - angle > angle else np.pi - angle
        angle = -angle
    # else:
    #     angle = -angle
    reflect_direction = rotate_vector(normal, angle)
    return reflect_direction


def in_reflect(direction, normal):
    direction = np.array(direction)
    normal = np.array(normal)
    angle = angle_between_vectors(direction, normal)
    # angle = angle if np.pi - angle > angle else np.pi - angle
    reflect_direction = rotate_vector(normal, -angle)
    return reflect_direction


def get_incident_angle(direction, normal):
    direction, normal = np.array(direction), np.array(normal)
    angle = angle_between_vectors(direction, normal)
    angle = angle if np.pi - angle > angle else np.pi - angle
    return angle


def get_refraction_direction(direction, normal, n_from, n_to, p=0):
    theta_i = get_incident_angle(direction, normal)
    # snell_law
    # n1* np.sin(theta1) = n2 * np.sin(theta2)
    theta_r = np.arcsin(n_from / n_to * np.sin(theta_i))

    if p == 0:
        refraction_direction = normalize(rotate_vector(-normal, theta_r))
    else:
        refraction_direction = normalize(rotate_vector(normal, -theta_r))

    return refraction_direction


def get_theta_def(theta_i, theta_r, p):
    return 2 * p * theta_r - 2 * theta_i - (p - 1) * PI


def theta_def_to_sca(theta_def):
    """本函数已正确实施"""
    kp = int((PI - theta_def) / (2 * PI))
    var = theta_def % (2 * PI)
    if abs(var) < PI:
        q = 1
    else:
        q = -1
    theta_sca = (theta_def + 2 * np.pi * kp) / q
    return theta_sca, q


def add_in_rays(point1, point2, color=GREEN):
    ray = Arrow(point1, point2, buff=0, thickness=0.01)
    ray.set_color(color)
    ray.set_opacity(0.2)
    return ray


def add_out_rays_title(theta_i, theta_r, p, point1, color=None, show_text=True):
    theta_def = get_theta_def(theta_i, theta_r, p)
    theta_sca, q = theta_def_to_sca(theta_def)
    dx = 1 if theta_sca < PI / 2 else -1  # 散射角小于90°，右半部出射，大于90°左半部出射
    dy = abs(np.tan(theta_sca)) * q  # q =1 表示上半部出射， -1表示下半部出射

    norm_vec = normalize(np.array([dx, dy, 0]))
    point_out = point1 + 1.6 * norm_vec
    ray = Arrow(point1, point_out, buff=0, thickness=0.02)
    ray.set_color(color)

    if show_text:
        title = Tex(f"p={p}").scale(0.7).move_to(point1 + 2 * norm_vec)

    return ray, title


def calc_theta_r(theta_i, n1, n2):
    theta_r = np.arcsin(n1 / n2 * np.sin(theta_i))
    return theta_r
