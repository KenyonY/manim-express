from example_imports import *
scene = EagerModeScene()

triangle = Triangle().scale(2)
square = Square().scale(2)

scene.play(Transform(triangle, triangle.copy().move_to(RIGHT*3)), run_time=2)

scene.play(Transform(triangle, triangle.copy().shift(UP*3)),run_time=3)
scene.hold_on()


