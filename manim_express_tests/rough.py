from manim_express_tests.tests_import import *
from manim_express.rough import *

CONFIG.preview = True


class TestRough(EagerModeScene):
    def clip1(self):
        # sline = SketchLine(r=0.2).get_graph(YELLOW).move_to(UP*2)
        # self.add(sline)
        striangle = SketchTriangle(stroke_times=3, r=0.2).get_graph().move_to(UP*2+LEFT*2)
        self.add(striangle)
        rect = SketchRectangle(width=2, height=2, stroke_times=2).get_graph(GREEN).move_to(UP*2)
        self.add(rect)

        self.add(SketchPolygon(n=5, r=0.1, stroke_times=3).get_graph(RED).move_to(UP*2 + RIGHT*2))

        self.add(SketchArc().get_graph())
        # CubicBezier()

TestRough().render()
