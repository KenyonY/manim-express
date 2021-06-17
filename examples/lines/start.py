from examples.example_imports import *
scene = EagerModeScene()

num_line1 = NumberLine(x_range=[0, 5, 1], include_numbers=True, include_tip=True,
                       tip_config={"width": 0.25, "length": 0.35},
)
scene.play(Write(num_line1))

num_line2 = num_line1.copy().rotate(45*DEGREES, [0, 0, 1]).move_to(UR*3)
scene.play(Write(num_line2))

num_line3 = num_line1.copy().rotate(90*DEGREES, OUT)
scene.play(Write(num_line3))

num_line4 = num_line1.copy().rotate(90*DEGREES, DOWN)
scene.play(Write(num_line4))


scene.hold_on()