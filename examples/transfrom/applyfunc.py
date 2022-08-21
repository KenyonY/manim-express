from examples.example_imports import *


class ApplyDemo(GlEagerScene):
    def clip1(self):
        grid = NumberPlane((-PI, PI), (-PI, PI)).set_stroke(opacity=0.)
        self.show_creation(grid)
        text = Text("sss").scale(3).set_color(BLUE)
        self.write(text)
        grid.add(text)
        grid.prepare_for_nonlinear_transform()

        # self.play(grid.animate.apply_complex_function(
        #     lambda x: np.exp(x+1j*x)), run_time = 5)
        factor = 0.1
        grid.apply_function(
            lambda p: [
                p[0] + np.random.rand() * factor,
                p[1] + np.random.rand() * factor,
                p[2]
            ]
        )
        grid.apply_complex_function(
            lambda x: np.exp(0.3 * x)
        )
        # self.play(
        #     grid.animate.apply_function(
        #         lambda p: [
        #             p[0] + np.random.rand() * factor,
        #             p[1] + np.random.rand() * factor,
        #             p[2]
        #         ]
        #     ),
        #     run_time=1,
        # )

    def clip10(self):
        grid = NumberPlane((-PI, PI), (-PI, PI))

        # self.play(grid.animate.apply_matrix(matrix), run_time=1)
        def sigmoid(x):
            return 1 / (1 + np.exp(-1 * x))

        circle = Circle().set_color(RED).scale(2).move_to(DR)
        triangle = Triangle().set_color(GREEN).scale(2).move_to(UL)
        line1 = Line(ORIGIN, [-6.5, 6.5, 0]).set_color(RED)
        self.play(ShowCreation(grid), run_time=1)

        # grid.add(circle)
        # grid.add(triangle)
        grid.add(line1)
        self.wait(1)

        grid.prepare_for_nonlinear_transform()
        # self.wait(1)
        # self.play(
        #     grid.animate.apply_complex_function(sigmoid),
        #     run_time=6,
        # )

        factor = 0.1

        self.play(
            grid.animate.apply_function(
                lambda p: [
                    np.cos(p[0]),
                    # np.sin(p[1]),
                    p[1],
                    # p[0],
                    # p[1] + math.exp(p[0]),
                    p[2]
                ]
            )
        )
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0],
                    np.sin(p[1]),
                    p[2]
                ]
            )
        )
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + np.random.rand() * factor,
                    p[1] + np.random.rand() * factor,
                    p[2]
                ]
            ),
            run_time=5,
        )

        theta = 90 * DEGREES

        def apply_func(point):
            x, y, z = point[0], point[1], point[2]
            newx = x * np.cos(theta) - y * np.sin(theta)
            newy = x * np.sin(theta) + y * np.cos(theta)
            newz = z
            return [newx, newy, newz]

        # self.play(
        #     grid.animate.apply_function(
        #         apply_func
        #         # lambda p: [
        #         # p[0] + 0.5 * math.cos(p[1]),
        #         # p[1] + 0.5 * math.sin(p[0]),
        #         # p[2]
        #         # p[0] * np.cos(theta) - p[1] * np.sin(theta),
        #         # p[0] * np.sin(theta) + p[1] * np.cos(theta),
        #         # p[2] ,
        #         # ]
        #     ),
        #     run_time=3,
        # )
        self.wait(1.5)


ApplyDemo().render()
