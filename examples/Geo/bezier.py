from examples.example_imports import *
import sparrow


def bezier1():
    scene = EagerModeScene()
    d0 = Dot([-3, 2, 0]).set_color(GREEN)
    d1 = Dot([0, 0, 0]).set_color(GREEN)

    line1 = Line(d0, d1).set_color(GREY)

    t = ValueTracker(0)
    vec_L = d1.get_center() - d0.get_center()
    point = Dot(color=RED).add_updater(lambda x: x.move_to(vec_L * t.get_value() + d0.get_center()))
    path = TracedPath(point.get_center, stroke_width=7, stroke_color=RED)

    scene.add(d0, d1, line1, point, path)
    scene.play(t.increment_value, 1, run_time=5, rate_func=linear)
    scene.hold_on()


def bezier2():
    scene = EagerModeScene()
    d0 = Dot([-3, 0, 0])
    d1 = Dot([0, 0, 0])
    d2 = Dot([-3, 2, 0])

    d_s = VGroup(d0, d1, d2).set_color(GREY_A)

    line1 = Line(d0, d1).set_color(GREY)
    line2 = Line(d1, d2).set_color(GREY)

    t = ValueTracker(0)

    def dot_updater_with_line(line: Line):
        return lambda x: x.move_to(line.get_start() + (line.get_end() - line.get_start()) * t.get_value())

    def updater_with_dots(dot1: Dot, dot2: Dot, rate_func=linear):
        return lambda x: x.move_to(
            dot1.get_center() + (dot2.get_center() - dot1.get_center()) * rate_func(t.get_value()))

    d2.add_updater(updater_with_dots(d2.copy(), Dot().move_to([2, 2, 0]), rate_func=there_and_back))
    line2.add_updater(lambda x: x.put_start_and_end_on(d1.get_center(), d2.get_center()))
    dd0 = Dot(color=RED).add_updater(dot_updater_with_line(line1))
    dd1 = Dot(color=RED).add_updater(dot_updater_with_line(line2))

    line3 = Line().set_color(GREY_B).add_updater(lambda x: x.put_start_and_end_on(dd0.get_center(), dd1.get_center()))
    dd3 = Dot(color=RED).add_updater(dot_updater_with_line(line3))
    path = TracedPath(dd3.get_center).set_stroke(color=RED, width=7)

    scene.add(d2, d_s, line1, line2, line3, dd0, dd1, dd3, path)
    scene.play(t.increment_value, 1, run_time=7, rate_func=linear)

    # scene.hold_on()


class Bazier(EagerModeScene):
    def __init__(self):
        super().__init__()
        # self._value_tracker = None
        self._value_tracker = ValueTracker()

    def updater_with_line(self, line: Line):
        return lambda x: x.move_to(
            line.get_start() + (line.get_end() - line.get_start()) * self._value_tracker.get_value())

    @staticmethod
    def line_updater_with_dots(dot1: Dot, dot2: Dot):
        return lambda x: x.put_start_and_end_on(dot1.get_center(), dot2.get_center())

    def updater_with_dots(self, dot_start: Dot, dot_end: Dot, rate_func=linear):
        return lambda x: x.move_to(
            dot_start.get_center() + (dot_end.get_center() - dot_start.get_center()) * rate_func(
                self._value_tracker.get_value()))

    def clip3(self):
        scale = 2
        x_shift = -1
        y_shift = -0.2
        dot1 = Dot(scale * np.array([0 + x_shift, 0 + y_shift, 0])).set_stroke(color=GREEN_A, width=5)
        dot2 = Dot(scale * np.array([1 + x_shift, 1.8 + y_shift, 0])).set_stroke(color=GREEN_A, width=5)
        dot3 = Dot(scale * np.array([2 + x_shift, 1 + y_shift, 0])).set_stroke(color=GREEN_A, width=5)
        dot4 = Dot(scale * np.array([1.5 + x_shift, -1 + y_shift, 0])).set_stroke(color=GREEN_A, width=5)
        dot_group = VGroup(dot1, dot2, dot3, dot4)

        line_12 = Line(dot1, dot2).set_stroke(color=GREY, width=5)
        line_23 = Line(dot2, dot3).set_stroke(color=GREY, width=5)
        line_34 = Line(dot3, dot4).set_stroke(color=GREY, width=5)

        d1 = Dot([0, 0, 0]).set_color(RED)
        d2 = Dot().set_color(GREEN).next_to(d1, UP)
        d3 = Dot().set_color(BLUE).next_to(d1, RIGHT)
        d4 = Dot().set_color(GREY).next_to(d1, UR)
        d_groups = VGroup(d1, d2, d3, d4).to_edge(UP)
        self.play(Write(d_groups))
        self.wait(0.5)

        self.play(d1.move_to, dot1.get_center(),
                  d2.move_to, dot2.get_center(),
                  d3.move_to, dot3.get_center(),
                  d4.move_to, dot4.get_center(),
                  )
        self.wait(0.3)
        self.play(*[Write(i)for i in [dot_group, line_12, line_23, line_34]], run_time=0.5)

        d1.add_updater(self.updater_with_line(line_12))
        d2.add_updater(self.updater_with_line(line_23))
        d3.add_updater(self.updater_with_line(line_34))
        line_d12 = Line(d1, d2).set_color(RED)
        line_d23 = Line(d2, d3).set_color(GREEN)
        self.play(*[FadeIn(i) for i in [line_d12, line_d23]], run_time=0.3)
        # self.play(FadeIn(line_d12))
        # self.play(FadeIn(line_d23))

        line_d12.add_updater(self.line_updater_with_dots(d1, d2))
        line_d23.add_updater(self.line_updater_with_dots(d2, d3))

        d_d12 = Dot(color=BLUE).scale(0.5).add_updater(self.updater_with_line(line_d12))
        d_d23 = Dot(color=BLUE).scale(0.5).add_updater(self.updater_with_line(line_d23))
        self.add(d_d12, d_d23)

        target_line = Line().set_stroke(color=GREEN, width=2).add_updater(self.line_updater_with_dots(d_d12, d_d23))
        self.add(target_line)

        target_dot = Dot(color=RED).scale(0.7).add_updater(self.updater_with_line(target_line))
        path = TracedPath(target_dot.get_center).set_stroke(RED, 3)
        self.add(target_dot, path)

        self.play(self._value_tracker.increment_value, 1, run_time=5)
        self.wait(0.5)
        # self.hold_on()


# CONFIG.write_file = True
# CONFIG.gif = True
CONFIG.color = WHITE

bezier = Bazier()
# bezier.clip3()

bezier.render()
# bezier1()
# bezier2()
