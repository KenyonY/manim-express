from examples.example_imports import *
from manimlib import MTex, MTexText


CONFIG.color = rgb_to_hex([1, 1, 1])  # this will override the `color` option in custom_config.yml
class ApplyDemo(GlEagerScene):
    def clip1(self):
        blue =  "#4285f4"
        red = "#ea4335"
        yellow = "fbbc05"
        green = "34a853"

        color_map = {
            'U': blue,
            "N": red,
            "E": blue,
            "R": green
        }
        color_map = {
            "N": blue,
            "L": green,
            "P": red
        }
        text1 = MTex("NLP", tex_to_color_map=color_map)
        # text2 = MTex("UNER", font="Ink Draft", tex_to_color_map = color_map).move_to(UP + RIGHT * 3)
        # text3 = MTex("UNER", font="Ink Free", tex_to_color_map = color_map).move_to(UP * 2 + RIGHT * 3)
        # text4 = MTex("UNER", font="Segoe Script", tex_to_color_map = color_map).move_to(UP * 3 + RIGHT * 4)



        self.write(text1.scale(5))
        # self.write(text2)
        # self.write(text3)
        # self.write(text4)
        # grid.add(text)
        # grid.prepare_for_nonlinear_transform()
        # self.show_creation(grid)

        # self.play(grid.animate.apply_complex_function(
        #     lambda x: np.exp(x+1j*x)), run_time = 5)
        # factor = 0.1
        # grid.apply_function(
        #     lambda p: [
        #         p[0] + np.random.rand() * factor,
        #         p[1] + np.random.rand() * factor,
        #         p[2]
        #     ]
        # )
        # grid.apply_complex_function(
        #     lambda x: np.exp(0.3 * x)
        # )
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


ApplyDemo().render()
