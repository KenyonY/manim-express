from manimlib import *
import os


class A(Scene):
    def construct(self):
        arrow = Arrow(ORIGIN, UR)
        # self.play(ShowCreation(arrow))
        # self.wait(2)
        test_axis = np.array([1, 1, 1])

        vector_arrow = Arrow(ORIGIN, test_axis)
        self.play(ShowCreation(vector_arrow))
        self.wait()


if __name__ == "__main__":
    os.system("manimgl test.py")
