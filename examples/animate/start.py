from examples.example_imports import *
scene = EagerModeScene()
sq1 = Square()
scene.play(ShowCreation(sq1))
scene.play(sq1.animate.shift(RIGHT*3))

scene.play(sq1.animate.rotate(DEGREES*90))
# The above is equal to the follow:
scene.play(Transform(sq1, sq1.copy().rotate(90*DEGREES)))

# 有时我们需要不经过缩放的旋转, 如可使用Rotate:
scene.play(Rotate(sq1, angle=90*DEGREES))
# 或者使用add_updater
sq1.add_updater(lambda x, dt: x.rotate(dt*PI/2))
scene.wait(3)


scene.hold_on()

