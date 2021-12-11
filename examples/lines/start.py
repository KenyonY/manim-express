from examples.example_imports import *

num_line1 = NumberLine(x_range=[0, 5, 1], include_numbers=True, include_tip=True,
                       tip_config={"width": 0.25, "length": 0.35},
                       )


class A1(EagerModeScene):
    def __init__(self):
        super(A1, self).__init__(screen_size=Size.bigger)

    def clip1(self):
        self.anyform = Triangle().set_color(BLUE_C).move_to(LEFT * 2)
        self.play(Write(self.anyform))
        self.play(Transform(self.anyform, self.anyform.copy().set_fill(GREEN_A).scale(3)))
        self.square = Square().move_to(RIGHT)
        self.play(Transform(self.anyform, self.square))
        self.play(FadeOut(self.anyform))
        self.play(FadeIn(self.anyform))

        # dot = Circle().scale(2).set_fill(WHITE)
        # self.play(ShowCreation(dot))

    def clip2(self):
        num_line2 = num_line1.copy().rotate(45 * DEGREES, [0, 0, 1]).move_to(UR * 3)
        self.play(Write(num_line2))
        dot = Circle().scale(2).set_fill(WHITE).move_to(RIGHT * 3)
        self.play(ShowCreation(dot))

    def clip3(self):
        c = ParametricCurve(
            lambda theta: [np.cos(theta), np.sin(theta), 0], [0, 2 * PI])
        c2 = ParametricCurve(lambda x: [x, np.sin(x), 0], [-2, 5])
        self.play(*map(ShowCreation, (c, c2)))
        now = self.time
        c.add_updater(lambda c: c.set_y(math.sin(3 * (self.time - now))))
        self.wait(2)

        dot = Dot()
        dot.move_to(c.get_start())
        self.add(dot)
        self.play(MoveAlongPath(dot, c))
        # self.wait(10)


# scene.hold_on()
d1 = A1()
d1.clip1()
d1.clip3()
# d1.render()
# d1.replay(1)
# d1.loop_clip(1)
