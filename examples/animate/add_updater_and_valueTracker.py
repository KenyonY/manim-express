from examples.example_imports import *

scene = EagerModeScene()

time = ValueTracker(0)
# scene.play(time.increment_time, 2, rate_func=linear, run_time=3)
number = DecimalNumber(0)
scene.add(number)
number.add_updater(lambda x: x.set_value(time.get_value()))
scene.play(time.increment_value, 2., rate_func=linear, run_time=2)

plane = NumberPlane(x_range=(-7, 7), y_range=(-4, 4))
plane.add_coordinate_labels()
scene.play(Write(plane))
dot = Dot()
dot.move_to(UP)
text = Text("This is a dot")
deci_number = DecimalNumber(0)
deci_number.add_updater(lambda x: x.next_to(dot, UP))
text.next_to(dot)
scene.add(dot)
scene.add(text)
text.add_updater(lambda obj: obj.next_to(dot))
deci_number.add_updater(lambda x: x.set_value(dot.get_center()[1]))

scene.play(dot.move_to, DOWN, rate_function=linear, run_time=5)

scene.hold_on()

