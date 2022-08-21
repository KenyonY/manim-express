from examples.example_imports import *
from sparrow.path import rel_to_abs


class PPtScene(EagerModeScene):
    def clip1(self):
        # code = get_code_by_read(rel_to_abs('./start.py'), language='python',
        #                         # font='Segoe Script'
        #                         )

        # self.show_creation(code, run_time=1)
        pipf = PictureInPictureFrame().scale(0.5)
        # screen_a = ScreenRectangle(height=2)
        # text1 = Text("我爱我中国看as刀法撒地方看见道法").scale(0.3).move_to(RIGHT)
        # screen_a.add(text1)
        # self.add(AnimatedBoundary(screen_a))
        triangle = Triangle()
        pipf.add(triangle)
        self.add(pipf)
        self.play(pipf.move_to, RIGHT*2, run_time=1)
        self.add(AnimatedBoundary(pipf))
        self.play(Transform(triangle, Rectangle()), run_time=3)

        # self.wait(10)


# CONFIG.preview = False
PPtScene().render()
#

