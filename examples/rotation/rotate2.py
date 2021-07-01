from examples.example_imports import *


scene = EagerModeScene()
axis = np.array([1, 1,1 ])
angle = 39*DEGREES

q1 = Quaternion().set_from_axis_angle(axis, angle)
q2 = Quaternion().set_from_axis_angle(axis, 20*DEGREES)

print(Quaternion.multiply_quat(q1, q2))
print(Quaternion.multiply_quat_2(q1, q2))

axes = ThreeDAxes()
scene.play(ShowCreation(axes))

labels = VGroup(axes.get_axis_label('x', axes.get_x_axis(), edge=RIGHT, direction=DR),
                axes.get_axis_label('y', axes.get_y_axis(), edge=UP, direction=DR),
                axes.get_axis_label('z', axes.get_z_axis(), edge=[0, 0, 1], direction=DR).rotate(PI/4, [1, 0, 0])
                )
scene.add(labels)

scene.hold_on()