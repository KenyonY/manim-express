from examples.example_imports import *


class Demo(EagerModeScene):
    def __init__(self):
        super().__init__()

    def clip_1(self):
        c1 = Circle()
        self.add(c1)


Demo().render()
