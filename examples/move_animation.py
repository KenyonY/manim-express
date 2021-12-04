import math
from example_imports import *
scene = EagerModeScene(screen_size=Size.big)


def episode1():
    """Transform
    """
    triangle = Triangle().scale(2)
    square = Square().scale(2)

    scene.play(Transform(triangle, triangle.copy().move_to(RIGHT*3)), run_time=2)

    scene.play(Transform(triangle, triangle.copy().shift(UP*3)), run_time=3)

    scene.play(Transform(triangle, square), run_time=2)  # This leads to triangle == square
    scene.play(Transform(triangle, triangle.copy().shift(LEFT*2)))  # verification
    scene.play(FadeOut(triangle))

# episode1()

def episode2():
    """
    ParametricCurve, add_updater
    """
    circ = Circle().scale(0.5).move_to(RIGHT*2)
    scene.play(ShowCreation(circ))
    now = scene.time


    def update_circ(g):
        r, w = 2, 2.2
        theta = w * (scene.time - now)
        g.set_x(r*math.cos(theta))
        g.set_y(r*math.sin(theta))

    circ.add_updater(update_circ)

    c1 = ParametricCurve(
        lambda theta: [np.cos(theta), np.sin(theta), 0], [0, 2 * PI]
    )
    c1.add_updater(lambda c: c.set_x(3*math.sin(3 * (scene.time - now))))

    c2 = ParametricCurve(lambda theta: [theta, np.sin(theta), 0], [-2, 5])
    v = 2
    now2 = scene.time
    def update_sin(g):
        w, v = 2, 1
        t = scene.time - now2
        theta = w * t
        g.set_x(v*t)
    c2.add_updater(update_sin)

    scene.play(*map(ShowCreation, (c1, c2)))

# episode2()


def episode3():
    """
    NumberPlane, Transform, MoveAlongPath
    """
    matrix1 = [[1, 1],
               [0, 1]]

    circ = Circle()
    plane = NumberPlane((10, 10), (6, 6))
    scene.play(Write(plane))
    scene.play(Write(circ))
    scene.play(circ.animate.apply_matrix(matrix1), run_time=1)
    # scene.play(Transform(circ, circ.copy().shift(UP*3)))

    theta = 60 * DEGREES
    scene.play(Transform(circ, circ.copy().rotate(theta)), run_time=0.5)

    rotate_matrix = [[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta),  np.cos(theta)]]
    scene.play(Rotate(circ, theta), run_time=1)
    # scene.play(circ.animate.apply_matrix(rotate_matrix), run_time=0.5)

    dot = Dot().move_to(circ.get_end())
    scene.play(MoveAlongPath(dot, circ), run_time=1)

# episode3()


def episode4():
    """

    """
    arrow = Arrow(buff=0)
    line = Line().shift(DOWN)
    scene.add(arrow, line)

    arrow2 = Arrow(buff=0).scale(1).shift(UL*3)
    scene.play(GrowArrow(arrow2))
    arrow3 = arrow2.copy().rotate(-30*DEGREES)
    a3 = Arrow(UL*5, buff=0)

    # a3.set_angle(0)

    scene.play(a3.animate.rotate(30*DEGREES).set_color(RED),
            run_time=2,)

    # scene.play(GrowArrow(arrow3))
# episode4()


def episode5():
    """
    FunctionGraph, MoveAlongPath,
    """
    g1 = FunctionGraph(lambda x: x ** 2 -2, (-2, 2))
    scene.play(ShowCreation(g1))
    dot1 = Dot()
    little_sphere = Sphere(radius=0.2).set_color(LIGHT_PINK)

    path1 = MoveAlongPath(little_sphere, g1)
    path2 = MoveAlongPath(dot1, g1)

    scene.play(path1, run_time=2)
    scene.play(path2, run_time=2)

# episode5()


def episode6():
    """mobject.target   MoveToTarget
    """
    square = Square()
    square.move_to(LEFT*2)
    square.generate_target()
    square.target.shift(RIGHT*3)
    square.target.rotate(PI/4).scale(2)

    scene.play(ShowCreation(square))
    scene.wait(0.3)

    scene.play(MoveToTarget(square))


    scene.play(Transform(square, square.copy().rotate(-PI/4)))
    scene.play(Transform(square, square.copy().rotate(PI/4)))

# episode6()


#
# episode1()
# episode2()
episode3()
# episode4()
#
scene.hold_on()


