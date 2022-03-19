import numpy as np

from examples.example_imports import *
from einops import rearrange, reduce, repeat


class Transform2d(EagerModeScene):
    def clip_1(self):
        number_plane = NumberPlane()
        # number_plane = ComplexPlane()
        number_plane.add(Line(ORIGIN, [1, 1, 1]).scale(2))
        self.show_creation(number_plane)
        tri = Triangle().move_to(LEFT)
        square = Square().move_to(RIGHT)
        number_plane.add(tri, square)
        theta = 45 * DEGREES
        matrix = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        # self.play(number_plane.animate.apply_matrix(matrix), run_time=3)
        # tri_all_points = tri.get_all_points()
        self.wait()
        tri.move_to(ORIGIN)
        tri.apply_matrix(matrix)
        tri.move_to(LEFT)
        self.play(
        number_plane.animate.apply_complex_function(lambda z: z**2),
            run_time=3
        )
        # tri.set_points(tri_all_points)

        # self.play(tri.animate.apply_matrix(matrix), run_time=3)
        # self.fade_out(number_plane)

        # self.show_creation(complex_plane)

    def clip_none(self):
        axes = ThreeDAxes().set_stroke(opacity=0.3)
        self.add(axes)
        text_e = Text("e")
        text_i = Text("i")
        text_a = Text("a")
        points_e = text_e.get_all_points()
        points_a = text_a.get_all_points()
        # print(points_e, points_e.shape)
        # dc_e = DotCloud(color=GREEN, points=points_e, radius=0.005).scale(5)
        # dc_a = DotCloud(color=BLUE, points=points_a, radius=0.005).scale(5).move_to(RIGHT*2)
        # self.add(dc_e, dc_a)

        dot_e = VGroup()
        dot_a = VGroup()
        [dot_e.add(Dot(i, radius=0.003, color=GREEN)) for i in points_e]
        [dot_a.add(Dot(i, radius=0.003, color=BLUE)) for i in points_a]

        self.add(dot_e.scale(5).move_to(RIGHT), dot_a.scale(5).move_to(LEFT))
        self.wait()
        # self.fade_out(dot_a)

        points_a_vec3 = [Vec3(i) for i in points_a]
        [i.rotate(90 * DEGREES) for i in points_a_vec3]

        dot_a_new = VGroup()
        [dot_a_new.add(Dot(i, radius=0.003, color=BLUE)) for i in points_a_vec3]
        dot_a_new.scale(5).move_to(LEFT)
        self.play(Transform(dot_a, dot_a_new))

        # self.write()
        # dot_e.animate.rotate(50, )


Transform2d().render()

