import numpy as np
from examples.example_imports import *


class Animations(EagerModeScene):

    def clip8(self):
        # theta = np.linspace(0, 2*PI, 100)
        x = np.arange(100)
        y = np.cos(x / 5) * 9.8
        axes = Axes(x_range=[x.min(), x.max()], y_range=(y.min(), y.max()))
        self.add(axes)
        obj = PlotObj(x, y, axes=axes)
        self.add(obj)
        obj2 = PlotObj(x, x, axes=axes)
        self.add(obj2)
        # frame = self.camera.frame
        # self.play(frame.scale, 2)
        # self.play(frame.scale, 2)
        # self.play(frame.scale, 2)

        # self.plot(x, x)
        # self.show_plot()


        self.plot(y, y, show_axes=True)
        # self.show_plot(reset=False)
        axes_mobj, lines_mobj = self.get_plot_mobj()
        print(len(axes_mobj))
        self.play(ShowCreation(axes_mobj.add(lines_mobj)))
        self.play(axes_mobj.move_to, RIGHT*3)
        # self.plot(x, y)
        # self.show_plot()

    def clip9(self):
        cube = Cube().set_color_by_gradient([BLUE_C, GREEN_A]).scale(2)
        self.play(ShowCreation(cube))
        # axes = ThreeDAxes()
        frame = self.camera.frame

        # self.play(Rotate(cube, PI), run_time=3)

        self.play(self.camera.frame.move_to, RIGHT * 3, run_time=2)
        cube2 = Cube().move_to(RIGHT * 4)
        self.play(ShowCreation(cube2))

        vter = ValueTracker(0)

        def update_frame(x: CameraFrame):
            x.set_phi(vter.get_value())
            x.set_theta(vter.get_value())

        frame.add_updater(update_frame)
        self.play(vter.increment_value, 10, run_time=5)

        #
        # self.play(
        #     frame.animate.increment_phi(-10 * DEGREES),
        #     frame.animate.increment_theta(-20 * DEGREES),
        #     run_time=2
        # )
    # def clip2(self):
    #
    #     dot = Sphere(radius=0.05, fill_color=BLUE).move_to(0 * RIGHT + 0.1 * UP + 0.105 * OUT)
    #
    #     self.camera.frame.set_phi(65*DEGREES)
    #     self.camera.frame.set_theta(30*DEGREES)
    #     self.camera.frame.set_gamma(90*DEGREES)
    # self.begin_ambient_camera_rotation(rate=0.05)  # Start move camera
    # self.camera.frame


Animations().render()
