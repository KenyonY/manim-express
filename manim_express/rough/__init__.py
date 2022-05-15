from __future__ import annotations

import math
import numpy as np
from manim_express.math.vec import Vec3
import time
from manimlib import Line, CubicBezier, RED, GREEN, BLUE, WHITE, BLACK, VGroup, Dot, YELLOW
from manimlib import LEFT, RIGHT, UP, DOWN, UL, UR, DL, DR, ORIGIN, TAU
from manimlib import Arc as ManimArc
from manimlib.utils.space_ops import rotate_vector, compass_directions


# reference https://github.com/rough-stuff/rough/blob/master/src/fillers/dot-filler.ts
# theory: https://openaccess.city.ac.uk/id/eprint/1274/1/wood_sketchy_2012.pdf


class Sampler:
    def __init__(self, x, y, z=None, distance=None):
        self.x = x
        self.y = y
        if z is None:
            z = 0
        self.z = z

        self.distance = distance
        if self.distance is None:
            self.distance = 1

    def sample(self, r=None):
        r = self.distance * 0.1 if r is None else r
        offsets = np.random.uniform(-r / 2, r / 2, size=2)
        return np.array([self.x + offsets[0],
                         self.y + offsets[1],
                         self.z])


class VSampler:
    def __init__(self, points):
        np.random.seed(int(time.time()))
        self.points = points

    def sample(self, r=None):
        new_points = []
        for point in self.points:
            new_point = Sampler(*point).sample(r)
            new_points.append(new_point)
        return np.array(new_points)


class CurveVSampler(VSampler):
    def __init__(self, points):
        super().__init__(points)

    def sample(self, r=None):
        new_points = []
        for idx, point in enumerate(self.points):
            if idx != 0 and idx % 3 == 0:
                new_points.append(new_points[-1])
                continue
            new_point = Sampler(*point).sample(r)
            new_points.append(new_point)
        return np.array(new_points)


class LineFilter:
    def __init__(self, point1, point2, r=0.1):
        np.random.seed(int(time.time()))
        self.point1 = np.array(point1)
        self.point2 = np.array(point2)
        self.vec = Vec3(self.point2 - self.point1)
        self.vec_array = self.vec.to_array()
        self.orthogonal_array = self.vec.copy().rotate(math.radians(90)).to_array()
        self.distance = np.linalg.norm(self.point1 - self.point2)
        self.interp_point = self.point1 + (self.point2 - self.point1) * 0.75
        self.interp_offset = self.distance * 0.1
        self.mid_point = (self.point1 + self.point2) / 2
        self.mid_offset = self.distance / 200
        self.r = r

    def gen_mid_point(self):
        return self.mid_point + np.random.uniform(-self.mid_offset / 2, self.mid_offset / 2, size=1)[
            0] * self.orthogonal_array

    def gen_interp_point(self):
        dx = np.random.uniform(-self.interp_offset / 2, self.interp_offset / 2, size=1)[
                 0] * self.vec_array / self.distance
        dy = np.random.uniform(-self.r / 2, self.r / 2, size=1)[0] * self.orthogonal_array
        return np.array(self.interp_point + dx + dy)

    def sample(self, sample_times=1):
        sample_lines = []
        for i in range(sample_times):
            point1 = Sampler(*self.point1).sample()
            interp_point = self.gen_interp_point()
            mid_point = self.gen_mid_point()
            point2 = Sampler(*self.point2).sample()

            sample_lines.append(np.array([point1, mid_point, interp_point, point2]))

        return sample_lines


class SketchLine:
    def __init__(self, start=None, end=None, r=0.1, stroke_times=1):
        if start is None:
            start = np.array([0, 0, 0])
        if end is None:
            end = np.array([1, 0, 0])
        self.lf = LineFilter(start, end, r).sample(sample_times=stroke_times)

    def get_graph(self, color=WHITE):
        group = VGroup()
        [group.add(CubicBezier(*lf).set_color(color).set_stroke(width=1)) for lf in self.lf]
        return group


class SketchPolygon:
    def __init__(self, n=6, r=0.1, stroke_times=1, vertices=None, start_angle=None, **kwargs):
        if vertices is None:
            if start_angle is None:
                # 0 for odd, 90 for even
                self.start_angle = (n % 2) * math.radians(90)
            start_vect = rotate_vector(RIGHT, self.start_angle)
            vertices = compass_directions(n, start_vect)
        self.filterd_lines = []
        for idx in range(len(vertices) - 1):
            self.filterd_lines.append(SketchLine(vertices[idx], vertices[idx + 1], r=r, stroke_times=stroke_times))
        self.filterd_lines.append(SketchLine(vertices[-1], vertices[0], r=r, stroke_times=stroke_times))

    def get_graph(self, color=WHITE):
        polygon_group = VGroup()
        for line in self.filterd_lines:
            polygon_group.add(line.get_graph(color))
        return polygon_group


class SketchTriangle(SketchPolygon):
    def __init__(self, vertices=None, start_angle=None, r=0.1, stroke_times=1, **kwargs):
        super().__init__(n=3, r=r, start_angle=start_angle, vertices=vertices, stroke_times=stroke_times, **kwargs)


class SketchRectangle(SketchPolygon):
    width = 4.
    height = 3.

    def __init__(self, vertices=None, width: float | None = None, height: float | None = None,
                 r=0.1, stroke_times=1, **kwargs):
        if vertices is None:
            if width is None:
                width = self.width
            if height is None:
                height = self.height
            vertices = np.array([[width / 2, height / 2, 0],
                                 [-width / 2, height / 2, 0],
                                 [-width / 2, -height / 2, 0],
                                 [width / 2, -height / 2, 0]])
        else:
            pass

        super().__init__(vertices=vertices, r=r, stroke_times=stroke_times, **kwargs)


class SketchArc:
    radius = 1.
    n_components = 3
    arc_center = ORIGIN

    def __init__(self, start_angle: float = 0,
                 angle: float = TAU / 4, r=0.07, stroke_times=1, **kwargs):
        points = ManimArc.create_quadratic_bezier_points(
            angle=angle,
            n_components=self.n_components,
            start_angle=start_angle,
        )
        # print(points)
        self.vertices_list = []
        for idx in range(stroke_times):
            self.vertices_list.append(CurveVSampler(points).sample(r=r))

    def get_graph(self, color=WHITE):
        vertices = [j for i in self.vertices_list for j in i]
        # point_group = VGroup(*[Dot(i, radius=0.05).set_color(YELLOW) for i in vertices])
        arc = ManimArc()
        arc.set_points(vertices)
        arc.scale(self.radius).shift(self.arc_center).set_color(color)
        # return point_group.add(arc)
        return arc

#
# class Rect:
#     pass
#
#
# class Elipse:
#     pass
#
