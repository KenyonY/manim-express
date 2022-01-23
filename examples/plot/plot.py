from examples.example_imports import *

# SceneArgs.color = "#222222"

scene = EagerModeScene()
theta = np.linspace(-10, 2*PI, 500)
x = np.cos(theta)
y = np.sin(theta)

test1 = 1
if test1:
    # scene.plot(theta, x, width=1)
    scene.plot(theta, x)
    scene.plot(theta, x+0.25)
    scene.plot(theta, x+0.5)
    scene.plot(theta, x+0.75)
    scene.plot(theta, x+1)
    scene.plot(theta, x+1.25)
    scene.plot(theta, x+1.5)
    scene.plot(theta, x+1.75)

    # scene.plot(theta, y)
    # mob = scene.get_plot_mobj().move_to(UR*3)
    # scene.add(mob)
    scene.show_plot()

test2 = 1
if test2:
    COL_COLORS = [MAROON_B, MAROON_C]
    EIGEN_COLORS = [TEAL_A, TEAL_D]
    kw = {
        "tex_to_color_map": {
            "\\lambda_1": EIGEN_COLORS[0],
            "\\lambda_2": EIGEN_COLORS[1],
            "=": WHITE,
        }
    }
    equation = VGroup(
        Tex("x^2 - 10x + 9", **kw)[0],
        Tex("=").rotate(PI / 2),
        Tex("x^2 - (\\lambda_1 + \\lambda_2)x + \\lambda_1 \\lambda_2", **kw),
        Tex("=").rotate(PI / 2),
        Tex("(x - \\lambda_1)(x - \\lambda_2)", **kw),
    )
    equation.arrange(DOWN)
    equation.to_edge(LEFT)
    line1, eq1, line2, eq2, line3 = equation

    axes = Axes(
        (-5, 10),
        (-20, 20),
        height=7,
        width=FRAME_WIDTH / 2,
    )
    axes.y_axis.stretch(0.5, 0)
    axes.x_axis.stretch(0.76, 1)
    axes.to_edge(RIGHT)
    graph = axes.get_graph(lambda x: x ** 2 - 10 * x+9)
    graph.set_color(BLUE)
    graph_label = line1.copy()
    graph_label.set_color(BLUE)
    graph_label.next_to(graph.get_end(), UP)
    graph_label.to_edge(RIGHT)

    root_dots = VGroup()
    root_labels = VGroup()
    for i, n, vect in zip((0, 1), (1, 9), (RIGHT, LEFT)):
        dot = Dot(axes.c2p(n, 0), color=EIGEN_COLORS[i])
        label = Tex(f"\\lambda_{i + 1}")
        label.match_color(dot)
        label.next_to(dot, UP + vect, buff=0.05)
        root_dots.add(dot)
        root_labels.add(label)
    root_dots.set_stroke(BLACK, 5, background=True)

    scene.play(Write(axes))
    scene.play(
        ShowCreation(graph, run_time=3),
        FadeIn(graph_label, UP)
    )
    scene.play(
        LaggedStartMap(GrowFromCenter, root_dots),
        LaggedStart(
            GrowFromPoint(root_labels[0], root_dots[0].get_center()),
            GrowFromPoint(root_labels[1], root_dots[1].get_center()),
        )
    )

scene.hold_on()
