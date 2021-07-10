from examples.example_imports import *
scene = EagerModeScene()

t = ValueTracker(0)
circle = Circle(radius=2).shift(LEFT*5)
dot_o = Dot(LEFT*5)
dot_a = Dot(LEFT*3)
line_oa = Line(dot_o.get_center(), dot_a.get_center())
dot_p = Dot().add_updater(lambda x:x.move_to(
    np.array([-5+2*np.cos(t.get_value()), 2*np.sin(t.get_value()), 0])
))
line_op = Line().add_updater(lambda x: x.put_start_and_end_on(
    dot_o.get_center(), dot_p.get_center()
))
arc = Arc(angle=0)
arc.add_updater(lambda x: x.become(Arc(start_angle=0, angle=t.get_value()%TAU)).shift(LEFT*5))
scene.add(circle, dot_o, dot_a, dot_p, line_oa, line_op, arc)
scene.play(t.set_value, 2*TAU, run_time=4)