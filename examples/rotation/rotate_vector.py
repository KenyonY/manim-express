from examples.example_imports import *

from manimlib import *

CONFIG.use_online_tex = True

scene = EagerModeScene(screen_size=Size.bigger)

theta = np.linspace(0, 2*np.pi, 100)
x = np.cos(theta)
y = np.sin(theta)
scene.plot(x, y, axes_ratio=1)
scene.show_plot()

scene.play(ShowCreation(ThreeDAxes()))
frame = scene.camera.frame

# scene.play(
#     # frame.animate.increment_theta(-30 * DEGREES),
#     frame.animate.rotate(70 * DEGREES, [1, 0, 0]),
#     run_time=2)
#
# scene.play(
#     frame.animate.rotate(70 * DEGREES, [0, 0, 1]),
#     run_time=2)

# scene.play(
    # frame.animate.increment_theta(70*DEGREES),
#     frame.animate.increment_phi(70 * DEGREES),
    # frame.animate.increment_gamma(70 * DEGREES)
# )

m_vec = Arrow(ORIGIN, RIGHT * 3, buff=0).set_fill(color=RED_D, opacity=0.8).set_stroke(color=RED_C, width=2)
vec = Vec3([3, 0, 0])


angle = 55 * DEGREES
angle2 = 30*DEGREES
axis = [2, 1, 1]
axis = [0, 0, 1]

# quaternion = quaternion_from_angle_axis(angle, axis)

q1 = Quaternion().set_from_axis_angle(axis, angle)
q2 = Quaternion().set_from_axis_angle(axis, angle2)


# angle_axis = angle_axis_from_quaternion(quaternion)
# matrix = rotation_matrix_from_quaternion(quaternion)
# matrix2 = rotation_matrix_transpose_from_quaternion(quaternion)
# scene.play(Transform(m_vec, m_vec.copy().apply_matrix(matrix)), run_time=3)

scene.play(ShowCreation(m_vec))
scene.play(Transform(m_vec, m_vec.copy().rotate_about_origin(angle, axis)))
scene.play(Transform(m_vec, m_vec.copy().rotate_about_origin(angle2, axis)))


a1 = Arrow(ORIGIN, vec.to_array(), buff=0).set_fill(color=GREEN)
scene.play(ShowCreation(a1))
vec.apply_quaternion(q1)
a2 = Arrow(ORIGIN, vec.to_array(), buff=0).set_fill(color=GREEN)

scene.play(Transform(a1, a2))

vec = Vec3([3, 0, 0]).apply_quaternion(q1.multi(q2))
a3 =  Arrow(ORIGIN, vec.to_array(), buff=0).set_fill(color=GREEN)
scene.play(Transform(a1, a3))

scene.hold_on()
