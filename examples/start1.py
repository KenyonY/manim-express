from manim_express import EagerModeScene, Size, CONFIG
from manimlib import *
from manim_express.plot import m_line, m_scatter

# SceneArgs.color = rgb_to_hex([0., 0, 0])
CONFIG.color = "#222222"

CONFIG.full_screen = True
CONFIG.preview = True
# SceneArgs.frame_rate = 30
# SceneArgs.gif = True

scene = EagerModeScene(screen_size=Size.big)
axes = ThreeDAxes()
tri = Triangle().scale(2)
scene.play(ShowCreation(tri))

dots = []
for i in tri.get_all_points():
    dot = Dot(i)
    dot.shift([0, 0, np.random.random()])
    dot.set_color(rgb_to_hex(np.random.randint(100, 254, size=(3))))
    dots.append(dot)

dots = VGroup(*dots)
scene.play(Write(dots))
scene.play(dots.move_to, UL*2)

scene.play(FadeOut(tri))
#
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
print(circle.point_at_angle(PI))
#
square = Square()

scene.play(ReplacementTransform(circle, square))

scene.play(square.shift, DOWN*2)
scene.play(FadeOut(square))

theta = np.linspace(0, 2 * PI, 200)
x = np.cos(theta)
y = np.sin(theta)
z = theta * 3

line = m_line(x, y, z, axes=axes)
scene.add(axes)
scene.play(ShowCreation(line, run_time=1))

c = ParametricCurve(
    lambda theta: [np.cos(theta), np.sin(theta), 0], [0, 2 * PI])

c2 = ParametricCurve(lambda x: [x, np.sin(x), 0], [-2, 5])

scene.play(*map(ShowCreation, (c, c2)))
now = scene.time
c.add_updater(lambda c: c.set_y(math.sin(3 * (scene.time - now))))
scene.wait(1)
scene.play(Indicate(line))
dot = Dot()
dot.move_to(c.get_start())
scene.add(dot)
scene.play(MoveAlongPath(dot, c))

scene.play(ShowCreation(Circle()))


# scene.play(WiggleOutThenIn(line))

# image = scene.get_image()

# import matplotlib.pyplot as plt
# image.show()

# plt.imshow(np.array((image))
# plt.show()


scene.hold_on()