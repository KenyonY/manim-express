from manim_express_tests.tests_import import *

scene = EagerModeScene(screen_size=Size.medium)
test_axis = np.array([1, 1, 1])
vector_arrow = Arrow(ORIGIN, test_axis)
scene.play(ShowCreation(vector_arrow))
scene.hold_on()


q_1 = Quaternion().set_from_axis_angle(test_axis, 20 * DEGREES)
q_2 = Quaternion().set_from_axis_angle(test_axis, 30 * DEGREES)
print(Quaternion.multiply_quat(q_1, q_2))
print(Quaternion.multiply_quat_2(q_1, q_2))

vec1 = Vec3(1, 1, 1).normalise()
vec2 = Vec3(2, 3, 4).normalise()
print("-------------------")
print(vec1, vec2)
q = Quaternion().set_from_unit_vectors(vec1, vec2)

print(vec1.apply_quaternion(q))

