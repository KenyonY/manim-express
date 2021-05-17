from manim_express import EagerModeScene
from manimlib import *
from manim_express.utils import m_line, m_scatter

scene = EagerModeScene()

theta = np.linspace(0, 2 * PI, 200)
x = np.cos(theta)
y = np.sin(theta)
z = np.sin(theta*3)
axes = ThreeDAxes()
line = m_line(x, y, z, axes=axes)
scene.add(axes)
scene.play(ShowCreation(line, run_time=1))

c = ParametricCurve(
    lambda theta: [np.cos(theta), np.sin(theta), 0], [0, 2 * PI])

c2 = ParametricCurve(lambda x: [x, np.sin(x), 0], [-2, 5])

scene.play(*map(ShowCreation, VGroup(c, c2)))
now = scene.time
c.add_updater(lambda c: c.set_y(math.sin(3 * (scene.time - now))))
scene.wait(5)

# scene.tear_down()
scene.hold_on()
