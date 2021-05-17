from manim_express import EagerModeScene, Size, Config
from manimlib import *
from manim_express.utils import m_line, m_scatter

Config.color = rgb_to_hex([0., 0, 0])
Config.full_screen = True


scene = EagerModeScene(screen_size=Size.bigger, Config=Config)

# scene.window =  Window(scene=scene, **scene.window_config)

circle = Circle(stroke=0.1)
circle.move_to(LEFT*3)
# circle.set_stroke(color=BLUE_D, width=0.1)

# scene.camera.background_rgba =[0.3, 0.4, 0.5, 1]

scene.play(ShowCreation(circle))
scene.play(
    circle.scale, 2,
    circle.shift, RIGHT*5,
    run_time=2
)

#
# theta = np.linspace(0, 2 * PI, 200)
# x = np.cos(theta)
# y = np.sin(theta)
# z = np.sin(theta*3)
# axes = ThreeDAxes()
# line = m_line(x, y, z, axes=axes)
# scene.add(axes)
# scene.play(ShowCreation(line, run_time=1))
#
# c = ParametricCurve(
#     lambda theta: [np.cos(theta), np.sin(theta), 0], [0, 2 * PI])
#
# c2 = ParametricCurve(lambda x: [x, np.sin(x), 0], [-2, 5])
#
# scene.play(*map(ShowCreation, VGroup(c, c2)))
# now = scene.time
# c.add_updater(lambda c: c.set_y(math.sin(3 * (scene.time - now))))
# scene.wait(1)
# scene.play(Indicate(line))
# dot = Dot()
# dot.move_to(c.get_start())
# scene.add(dot)
# scene.play(MoveAlongPath(dot, c))


# scene.play(WiggleOutThenIn(line))

scene.hold_on()

# image = scene.get_image()

# import matplotlib.pyplot as plt
# image.show()

# plt.imshow(np.array((image))
# plt.show()