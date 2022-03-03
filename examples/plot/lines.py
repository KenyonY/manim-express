from manim_express.eager import PlotObj, Size
from examples.example_imports import *

scene = EagerModeScene(screen_size=Size.bigger)

graph = Line().scale(0.2)
# t0 = time.time()
#
# delta_t = 0.5
# for a in np.linspace(3, 12, 3):
#     graph2 = ParametricCurve(lambda t: [t,
#                                         0.8 * np.abs(t) ** (6 / 7) + 0.9 * np.sqrt(abs(a - t ** 2)) * np.sin(
#                                             a * t + 0.2),
#                                         0],
#                              t_range=(-math.sqrt(a), math.sqrt(a))).scale(0.5)
#     scene.play(Transform(graph, graph2), run_time=3)
ps = np.random.rand(10, 3)
print(ps.shape)
print(ps[:, 0].max())

theta = np.linspace(0, 2 * PI, 100)
x = np.cos(theta)
y = np.sin(theta)

p = PlotObj(x, y)
scene.play(ShowCreation(p))

s = PlotObj(theta, x).set_color(RED)

scene.play(ShowCreation(s))

grid = p.get_grid(3, 3)
scene.add(grid)
scene.play(grid.animate.shift(LEFT))
scene.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN, RED))
scene.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))

# scene.play(grid.animate.apply_complex_function(np.exp), run_time=5)
scene.play(
    grid.animate.apply_function(
        lambda p: [
            p[0] + 0.5 * math.sin(p[1]),
            p[1] + 0.5 * math.sin(p[0]),
            p[2]
        ]
    ),
    run_time=5,
)
scene.hold_on()
