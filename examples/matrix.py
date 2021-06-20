from example_imports import *
# SceneArgs.color ="#222222"
scene = EagerModeScene(screen_size=Size.bigger)

intro_words = Text("""
    The original motivation for manim was to
    better illustrate mathematical functions
    as transformations.
""", font="KaiTi")
intro_words.to_edge(UP)

scene.play(Write(intro_words))
scene.wait(2)

# Linear transform
grid = NumberPlane((-10, 10), (-5, 5))
matrix = [[1, 1], [0, 1]]
linear_transform_words = VGroup(
    Text("This is what the matrix"),
    IntegerMatrix(matrix, include_background_rectangle=True),
    Text("looks like")
)
linear_transform_words.arrange(RIGHT)
linear_transform_words.to_edge(UP)
linear_transform_words.set_stroke(BLACK, 10, background=True)

scene.play(
    ShowCreation(grid),
    FadeTransform(intro_words, linear_transform_words)
)
scene.wait()
scene.play(grid.animate.apply_matrix(matrix), run_time=3)
scene.wait()

# Complex map
c_grid = ComplexPlane()
moving_c_grid = c_grid.copy()
moving_c_grid.prepare_for_nonlinear_transform()
c_grid.set_stroke(BLUE_E, 1)
c_grid.add_coordinate_labels(font_size=24)
complex_map_words = TexText("""
    Or thinking of the plane as $\\mathds{C}$,\\\\
    this is the map $z \\rightarrow z^2$
""")
complex_map_words.to_corner(UR)
complex_map_words.set_stroke(BLACK, 5, background=True)

scene.play(
    FadeOut(grid),
    Write(c_grid, run_time=3),
    FadeIn(moving_c_grid),
    FadeTransform(linear_transform_words, complex_map_words),
)
scene.wait()
scene.play(
    moving_c_grid.animate.apply_complex_function(lambda z: z ** 2),
    run_time=6,
)

scene.wait(2)

scene.hold_on()