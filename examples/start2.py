from manimlib import *
import os

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()
        # self.play(ReplacementTransform(square, circle))
        self.play(Transform(square, circle))
        self.wait()


if __name__ == "__main__":
    os.system('manimgl start2.py ')