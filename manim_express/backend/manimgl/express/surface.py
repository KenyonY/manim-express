from manim_express.backend.manimgl.express.eager import EagerModeScene
from manimlib import *


class CustomSurface:
    def __init__(self, axes=None, resolution=(101, 51)):
        if axes is None:
            axes = ThreeDAxes()
            # axes.add_coordinate_labels(
            #     font_size=15,
            # )
        self.axes = axes
        self.resolution = resolution

    def set_default_kwargs(self, kwargs: dict):
        kwargs.setdefault('color', BLUE_E)
        kwargs.setdefault('resolution', self.resolution)

    def get_axes(self):
        return self.axes

    def cylinder(self, r=1, h=3, **kwargs):
        """https://www2.math.uconn.edu/~stein/math210/slides/math210-09notes.pdf"""
        self.set_default_kwargs(kwargs)
        return ParametricSurface(lambda u, v: self.axes.c2p(*np.array(
            [r * np.cos(v), r * np.sin(v), u])),
                                 u_range=[-EPSILON, EPSILON + h],
                                 v_range=[0, TAU],
                                 color=kwargs['color'],
                                 resolution=self.resolution)

    def paraboloid(self, **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(lambda u, v: self.axes.c2p(*np.array(
            [np.cos(v) * u, np.sin(v) * u, u ** 2])),
                                 u_range=[-EPSILON - 2, EPSILON + 2],
                                 v_range=[-2, 2],
                                 color=kwargs['color'],
                                 resolution=self.resolution)

    def para_hyp(self, **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(
            lambda u, v: self.axes.c2p(*np.array([u, v, u ** 2 - v ** 2])),
            v_range=[-2, 2],
            u_range=[-2, 2],
            color=kwargs['color'],
            resolution=self.resolution)

    def cone(self, **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(lambda u, v: self.axes.c2p(*np.array(
            [u * np.cos(v),
             u * np.sin(v),
             u])),
                                 v_range=[0, TAU],
                                 u_range=[-EPSILON - 2, EPSILON + 2],
                                 color=kwargs['color'],
                                 resolution=self.resolution)

    def hip_one_side(self, **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(lambda u, v: self.axes.c2p(*np.array(
            [np.cosh(u) * np.cos(v),
             np.cosh(u) * np.sin(v),
             np.sinh(u)])),
                                 v_range=[0, TAU],
                                 u_range=[-EPSILON - 2, EPSILON + 2],
                                 color=kwargs['color'],
                                 resolution=self.resolution)

    def ellipsoid(self, a, b, c, **kwargs):
        """https://zh.wikipedia.org/wiki/%E6%A4%AD%E7%90%83"""
        return ParametricSurface(lambda u, v: self.axes.c2p(*np.array([
            a * np.cos(u) * np.cos(v),
            b * np.cos(u) * np.sin(v),
            c * np.sin(u)
        ])),
                                 v_range=[0, TAU],
                                 u_range=[-EPSILON - PI / 2, EPSILON + PI / 2],
                                 resolution=self.resolution)

    def sphere(self, r, origin=(0, 0, 0), **kwargs):
        """https://zh.wikipedia.org/wiki/%E7%90%83%E9%9D%A2"""

        self.set_default_kwargs(kwargs)
        return ParametricSurface(
            lambda u, v: self.axes.c2p(*np.array([
                r * np.sin(u) * np.cos(v) + origin[0],
                r * np.sin(u) * np.sin(v) + origin[1],
                r * np.cos(u) + origin[2]
                # r * np.sin(v) * np.cos(u) + origin[0],
                # r * np.sin(v) * np.sin(u) + origin[1],
                # r * np.cos(v) + origin[2]
            ])),
            u_range=[-EPSILON, PI + EPSILON],
            v_range=[0, TAU],
            # v_range=[-EPSILON, PI + EPSILON], u_range=[0, TAU],

            color=kwargs['color'],
            resolution=self.resolution)

    def circle(self, r, origin=(0, 0, 0), **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(
            lambda u, v: self.axes.c2p(*np.array([
                r * np.sin(u) * np.cos(v) + origin[0],
                r * np.sin(u) * np.sin(v) + origin[1],
                origin[2]
            ])),
            u_range=[-EPSILON, PI + EPSILON],
            v_range=[0, TAU],
            # v_range=[-EPSILON, PI + EPSILON], u_range=[0, TAU],
            color=kwargs['color'],
            resolution=self.resolution)

    def square(self, w, h, vertex1=(0, 0, 0), color=BLUE_E):
        return ParametricSurface(
            lambda u, v: self.axes.c2p(*np.array([
                u + vertex1[0],
                v + vertex1[1],
                vertex1[2]

            ])),
            u_range=[0, w],
            v_range=[0, h],
            # v_range=[-EPSILON, PI + EPSILON], u_range=[0, TAU],
            color=color,
            resolution=self.resolution)

    def torus(self, R=3, r=1, **kwargs):
        self.set_default_kwargs(kwargs)
        return ParametricSurface(
            lambda u, v: self.axes.c2p(*np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v)
            ])),
            u_range=[0, TAU],
            v_range=[0, TAU],
            color=kwargs['color'],
            resolution=kwargs['resolution']
        )


if __name__ == "__main__":
    from manim_express.backend.manimgl.express.eager import CONFIG
    CONFIG.preview=True
    s = EagerModeScene()
    # axes = ThreeDAxes()
    surface = CustomSurface()
    axes = surface.get_axes()
    s.add(axes)

    frame = s.camera.frame
    frame.set_euler_angles(
        # theta = -10 * DEGREES
        phi=75 * DEGREES)
    sphere = surface.sphere(2, [3, 0, 0])
    sphere.set_color_by_gradient((BLUE_E, RED_E))

    cylinder = surface.cylinder(2).move_to(axes.c2p(-2, 0, 0))
    cylinder.set_color_by_gradient((YELLOW_D, BLUE_D))

    s.play(ShowCreation(sphere))
    s.play(ShowCreation(cylinder))
    s.hold_on()
