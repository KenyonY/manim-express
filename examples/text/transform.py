from examples.example_imports import *


class TextTransform(EagerModeScene):
    def clip1(self):
        source = Text("the morse code", height=1)
        source = Text("yao kun yuan", height=1)
        self.play(Write(source))
        self.wait()

        target = Text("here come dots", height=1)
        target = Text("kun yuan yao", height=1)
        kw = {"run_time": 3, "path_arc": PI / 2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()


TextTransform().render()
