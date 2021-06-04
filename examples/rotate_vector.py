from manim_express import EagerModeScene, SceneArgs
from manimlib import *

scene = EagerModeScene()
scene.play(ShowCreation(ThreeDAxes()))
frame = scene.camera.frame

# frame.set_euler_angles(
#     # theta=-30 * DEGREES,
#     phi=70 * DEGREES,
# )
scene.play(
    # frame.animate.increment_theta(-30 * DEGREES),
    #       frame.animate.increment_phi(70 * DEGREES),
    frame.animate.rotate(50 * DEGREES, [0, 1, 1]),
    run_time=1)

vector = Arrow(ORIGIN, RIGHT * 3, buff=0)

angle = 55 * DEGREES
quaternion = quaternion_from_angle_axis(angle, [0, 1, 1])
print(quaternion, np.cos(angle / 2), np.sum([i ** 2 for i in quaternion]))

angle_axis = angle_axis_from_quaternion(quaternion)
matrix = rotation_matrix_from_quaternion(quaternion)
matrix2 = rotation_matrix_transpose_from_quaternion(quaternion)

scene.play(ShowCreation(vector))

scene.play(Transform(vector, vector.copy().apply_matrix(matrix)), run_time=3)

scene.hold_on()
