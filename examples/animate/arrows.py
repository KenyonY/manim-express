import mpmath

from examples.example_imports import *

scene = EagerModeScene()

# arc = Arc(
#     arc_center=LEFT,
#     radius=3.,
#     stroke_width=20.,
#     start_angle=0 * DEGREES,
#     angle=90 * DEGREES,
#     # color=BLACK
# )
# scene.add(arc)
#
# arcbetween = ArcBetweenPoints(
#     ORIGIN,
#     UR * 3,
#     angle=15 * DEGREES
# )
# scene.add(arcbetween)
#
# c_arrow = CurvedArrow(
#     ORIGIN, UL * 3,
#     angle=45 * DEGREES
# )
# scene.add(c_arrow)

# scene.add(be_applyed_arrow)

grid = NumberPlane((-10, 10), (-5, 5))
# matrix = [[1, 1], [0, 1]]
# linear_transform_words = VGroup(
#     Text("This is what the matrix"),
#     IntegerMatrix(matrix, include_background_rectangle=True),
#     Text("looks like")
# )
# linear_transform_words.arrange(RIGHT)
# linear_transform_words.to_edge(UP)
# linear_transform_words.set_stroke(BLACK, 10, background=True)

# scene.play(ShowCreation(grid))

# scene.play(grid.animate.apply_matrix(matrix), run_time=1)

# c_grid = ComplexPlane()
# moving_c_grid = c_grid.copy()
# moving_c_grid.prepare_for_nonlinear_transform()
# scene.play(ShowCreation(c_grid))
# c_grid.prepare_for_nonlinear_transform()
# c_grid.set_stroke(BLUE_E, 1)
# c_grid.add_coordinate_labels(font_size=24)


# be_applyed_arrow = Arrow(buff=0).scale(3).move_to(UP).set_color(RED)
# grid.add(be_applyed_arrow)



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
# scene.wait(1)
# scene.play(
#     grid.animate.apply_complex_function(sigmoid),
#     run_time=6,
# )
# scene.play(
#     grid.animate.apply_function(
#         lambda p: [
#             p[0] + rand_func(p[0]),
#             p[1] + rand_func(p[1]),
#             p[2]
#         ]
#     ),
#     run_time=5,
# )

grid.prepare_for_nonlinear_transform()

theta = 90 *DEGREES
def apply_func(point):
    x, y, z = point[0], point[1], point[2]
    newx = x * np.cos(theta) - y * np.sin(theta)
    newy = y * np.sin(theta) + y * np.cos(theta)
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
