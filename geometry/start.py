# from manim_imports_ext import *
from manimlib import *
# from utils import *

class Demo1(Scene):
    def construct(self):
        # https://www.bilibili.com/video/BV1kA411b7kq/?spm_id_from=333.788.recommend_more_video.-1

        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait(0.3)

        circle.move_to(np.array((0, 1, 0)))

        self.play(ReplacementTransform(square, circle))

        self.play(FadeOut(circle), run_time=2)

        arc = Arc(start_angle=0,
                  arc_center=3*LEFT,
                  angle=90*DEGREES,
                  color=RED,
                  )
        self.play(ShowCreation(arc))


        curveArrow = CurvedArrow(
            start_point=np.array((0, 2, 0)),
            end_point=np.array((1, -2, 0)),
            angle=180*DEGREES
        )
        self.play(ShowCreation(curveArrow))

def to_point(func, x):
    return 

def get_graph(axes, func, color):
    pass




class RemoveAllObjectsInScreen(Scene):
    def construct(self):
        self.play(
            ShowCreation(
                VGroup(*[
                    VGroup(*[Dot() for i in range(30)]).arrange(RIGHT)
                    for j in range(10)
                ]).arrange(DOWN)))
        self.play(*[FadeOut(mob) for mob in self.mobjects]
                  # All mobjects in the screen are saved in self.mobjects
                  )

        self.wait()