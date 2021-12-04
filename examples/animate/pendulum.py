from examples.example_imports import *


class TimesTable(VMobject):
    CONFIG = {
        "m": 2,  # multiplication factor
        "n": 200,  # number of lines
        "stroke_width": 1.5,  # stroke width of lines, circle
        "radius": 2.5,  # radius of circle
        "colors": [BLUE_D, WHITE, BLUE_D]  # color of lines
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.circle = Circle(
            radius=self.radius,
            stroke_width=self.stroke_width * 2
        )
        self.lines = self.get_lines()

        self.add(self.lines, self.circle)

    def get_lines(self):
        r = self.radius
        cos = np.cos
        sin = np.sin
        m = self.m
        return VGroup(*[
            Line(
                (r * cos(theta), r * sin(theta), 0),
                (r * cos(m * theta), r * sin(m * theta), 0),
                stroke_width=self.stroke_width
            )
            for theta in np.linspace(0, TAU, self.n)
        ]).set_color_by_gradient(*self.colors)


class TimesTableScene(Scene):
    def construct(self):
        max_factor = 10
        axes = Axes()
        axes.set_height(self.camera.get_frame_height())
        labels = axes.get_axis_labels()

        text, factor = factor_is = VGroup(
            TexText("Factor = "),
            DecimalNumber(0, num_decimal_places=0, font_size=30)
        )
        factor_is.arrange(RIGHT)
        factor_is.move_to(np.array([4, 3, 0]))

        self.play(
            ShowCreation(axes),
            Write(labels),
            Write(factor_is)
        )

        factor_tracker = ValueTracker()
        f_always(factor.set_value, factor_tracker.get_value)

        def create_and_remove_lines(lines):
            self.play(*[
                ShowCreation(line) for line in lines
            ], rate_func=linear)
            self.wait()
            self.remove(*[line for line in lines])

        self.table = TimesTable(m=0)
        self.play(ShowCreation(self.table.circle))
        create_and_remove_lines(self.table.lines)

        for i in range(2, max_factor):
            factor_tracker.set_value(i)
            self.table = TimesTable(m=i)
            create_and_remove_lines(self.table.lines)

        self.add(self.table)

        def update_table(table):
            new_table = TimesTable(m=factor_tracker.get_value())
            table.become(new_table)

        factor.num_decimal_places = 2

        self.table.add_updater(update_table)
        self.play(
            factor_tracker.animate.set_value(0),
            run_time=max_factor * 1.5,
            rate_func=linear
        )
        self.wait()
        self.play(*[Uncreate(m) for m in self.mobjects])

class Pendulum(VMobject):
    CONFIG = {
        "g": 9.8,  # acceleration due to gravity
        "origin": ORIGIN,  # hinge location
        "theta": 0,  # initial angle from the vertical
        "omega": 0,  # initial angular velocity
        "rod_config": {
            "length": 2,
            "color": WHITE,
            "stroke_width": 1.5,
        },
        "bob_config": {
            "mass": 0.1,
            "radius": 0.1,
            "color": BLUE,
            "fill_opacity": 1,
        },
        "speed": 0.8,  # speed of the simulation
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        digest_config(self, kwargs)

        bob_position = self.get_bob_position()

        self.rod = Line(
            self.origin,
            bob_position,
            **self.rod_config
        )

        self.bob = Circle(**self.bob_config)
        self.bob.move_to(bob_position)

        self.pendulum = VGroup(self.rod, self.bob)
        self.add(self.rod, self.bob)

    def get_length(self):
        return self.rod_config["length"]

    def get_bob_position(self):
        length = self.get_length()

        x = self.origin[0] - length * np.sin(self.theta)
        y = self.origin[1] - length * np.cos(self.theta)
        return np.array([x, y, 0])

    def _update_pos(self, theta):
        self.theta = theta
        theta = -(theta + PI / 2) % TAU
        self.rod.set_angle(theta)
        self.bob.move_to(self.rod.get_last_point())

    def start_swinging(self):
        self.add_updater(self.update_pendulum)

    def stop_swinging(self):
        self.remove_updater(self.update_pendulum)

    @staticmethod
    def update_pendulum(self, dt):
        theta = self.theta
        length = self.get_length()

        alpha = - self.g * np.sin(theta) / length  # angular acceleration

        self.omega += self.speed * dt * alpha
        self.theta += self.speed * dt * self.omega
        self._update_pos(self.theta)


class PendulumChaos(Scene):
    CONFIG = {
        "num": 1,  # number of pendulums
        "wait_time": 10,  # time of simulation
    }

    def construct(self):
        colors = it.cycle([ORANGE, BLUE, YELLOW, GREEN, RED_B])

        self.pends = VGroup(*[
            Pendulum(
                theta=PI / 2,
                rod_config={"length": i},
                bob_config={"color": next(colors)},
                speed=0.85,
            ) for i in reversed(np.linspace(1.5, 3, self.num))
        ])

        self.play(
            *[ShowCreation(pend) for pend in self.pends]
        )
        self.wait()

        for pend in self.pends:
            pend.start_swinging()
        self.wait(self.wait_time)


class PendulumChaos10(PendulumChaos):
    CONFIG = {
        "num": 10
    }

    def construct(self):
        super().construct()

        for pend in self.pends:
            pend.remove(pend.rod)
        self.wait(self.wait_time)

import os
if __name__ == "__main__":
    os.system("manimgl pendulum.py PendulumChaos10")