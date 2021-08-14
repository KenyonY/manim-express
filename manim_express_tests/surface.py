from manim_express_tests.tests_import import *


class HyperSlinky(EagerModeScene):
    def clip9(self):
        self.play(
            ApplyPointwiseFunction(
                lambda x_y_z: (1 + x_y_z[1]) * np.array((
                    np.cos(2 * np.pi * x_y_z[0]),
                    np.sin(2 * np.pi * x_y_z[0]),
                    x_y_z[2]
                )),
                NumberPlane().prepare_for_nonlinear_transform(),
            ),
            rate_func=there_and_back,
            run_time=10,
        )


HyperSlinky().render()
