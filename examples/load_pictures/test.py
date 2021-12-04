import numpy as np
from manimlib import *


class Test(Scene):
    def construct(self):
        image = ImageMobject("logo1.jpg")
        image2 = ImageMobject("logo1.png").set_opacity(1).scale(1.5).rotate(30 * DEGREES)

        image.move_to(LEFT * 2)
        # self.add(image)
        self.add(image2)


if __name__ == "__main__":
    import os

    os.system("manimgl test.py Test")
