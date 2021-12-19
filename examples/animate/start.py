from examples.example_imports import *

CONFIG.preview = True

scene = EagerModeScene(screen_size=Size.biggest
                       )
sq1 = Square()
scene.play(ShowCreation(sq1))
scene.play(sq1.animate.shift(RIGHT * 3))

scene.play(sq1.animate.rotate(DEGREES * 90))
# The above is equal to the follow:
scene.play(Transform(sq1, sq1.copy().rotate(90 * DEGREES)))

# 有时我们需要不经过缩放的旋转, 如可使用Rotate:
scene.play(Rotate(sq1, angle=990 * DEGREES), run_time=10, rate_func=linear)
# 或者使用add_updater
sq1.add_updater(lambda x, dt: x.rotate(dt * PI / 20))
scene.wait(3)

scene.hold_on()
