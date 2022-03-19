from examples.example_imports import *

scene = EagerModeScene()

grid = NumberPlane((-10, 10), (-5, 5))


# scene.play(grid.animate.apply_matrix(matrix), run_time=1)
def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))


circle = Circle().set_color(RED).scale(2).move_to(DR)
triangle = Triangle().set_color(GREEN).scale(2).move_to(UL)
line1 = Line(ORIGIN, [5, 0, 0]).set_color(RED)
grid.add(circle)
grid.add(triangle)
grid.add(line1)
scene.play(ShowCreation(grid), run_time=1)
scene.wait(1)

grid.prepare_for_nonlinear_transform()
# scene.wait(1)
# scene.play(
#     grid.animate.apply_complex_function(sigmoid),
#     run_time=6,
# )

factor = 0.2
scene.play(
    circle.animate.apply_function(
        lambda p: [
            p[0] + np.random.rand() * factor,
            p[1] + np.random.rand() * factor,
            p[2]
        ]
    ),
    run_time=5,
)

theta = 90 * DEGREES


def apply_func(point):
    x, y, z = point[0], point[1], point[2]
    newx = x * np.cos(theta) - y * np.sin(theta)
    newy = x * np.sin(theta) + y * np.cos(theta)
    newz = z
    return [newx, newy, newz]


scene.play(
    grid.animate.apply_function(
        apply_func
        # lambda p: [
        # p[0] + 0.5 * math.cos(p[1]),
        # p[1] + 0.5 * math.sin(p[0]),
        # p[2]
        # p[0] * np.cos(theta) - p[1] * np.sin(theta),
        # p[0] * np.sin(theta) + p[1] * np.cos(theta),
        # p[2] ,
        # ]
    ),
    run_time=3,
)

scene.hold_on()
