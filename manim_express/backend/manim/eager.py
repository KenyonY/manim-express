# from manim import Scene
from manim import *


class EagerScene(Scene):
    def render(self,
               preview=True,
               save_as_gif=True,
               frame_rate=60,
               pixel_height=1080,
               pixel_width=1920,
               use_opengl_renderer=False):
        super(EagerScene, self).render(preview)


class SquareToCircle(EagerScene):
    def construct(self):
        circle = Circle()
        square = Square()
        # square.flip(RIGHT)
        # square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(Uncreate(square))


if __name__ == "__main__":
    SquareToCircle().render(True, frame_rate=120)
