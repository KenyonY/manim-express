import numpy as np

from examples.example_imports import *


class Animations(EagerModeScene):
    def __init__(self):
        super(Animations, self).__init__(screen_size=Size.biggest)

    def clip0(self):
        theta = np.linspace(0, TAU, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        z = np.zeros(len(x))


        points = []
        for (i, j, k) in zip(x, y, z):
            points.append(np.array([i, j, k]))

        dotcloud = DotCloud(points).set_color(GREEN_C)
        self.add(dotcloud)
        po = (np.random.rand(20000, 3)-1/2)*42
        pmax = np.max(po)
        print(pmax)
        dc = DotCloud(po).set_color_by_rgb_func(lambda x: x/22+0.5).scale(0.5)
        # set_color_by_gradient(GREY_A, GREEN_C, BLUE_C, RED_C, YELLOW_A).
        self.add(dc)

        vc = ValueTracker(0)
        def update_camera(x: CameraFrame):
            x.set_theta(vc.get_value())
            x.set_phi(vc.get_value())

        self.camera.frame.add_updater(update_camera)
        self.play(vc.increment_value, 20, run_time=3)

        anyform = Text("Ling", font="Kaiti")
        # self.play(Write(anyform))
        # self.play(anyform.animate.move_to(RIGHT*3))
        # self.play(anyform.animate.become(Dot()))
        yao = Text("冻结的光", font="Kaiti").move_to(RIGHT*3)
        # self.play(anyform.animate.become(yao))
        # print(yao.get_stroke_shader_data())
        # x = yao.get_all_points()[:, 0]
        # y = yao.get_all_points()[:, 1]
        # self.plot(x, y, axes_ratio=1)
        # self.show_plot()

        # text = Text(
        #     'Google',
        #     t2c={
        #         '[:1]': '#3174f0', '[1:2]': '#e53125',
        #         '[2:3]': '#fbb003', '[3:4]': '#3174f0',
        #         '[4:5]': '#269a43', '[5:]': '#e53125',
        #     }
        # ).scale(5)
        # self.play(Write(text), run_time=3)

        # cube = Cube()
        # self.add(cube)
        # sphere = Sphere().move_to(RIGHT*2)
        # self.add(sphere)
        #
        # self.play(Rotate(cube, 900*DEGREES), run_time=10, rate_func=linear)


    def clip1(self):
        picture = ImageMobject("../../data/pic/code0.png").set_opacity(0.8).scale(2)
        self.add(picture)

Animations().render()
# Animations()