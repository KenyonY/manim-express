from manim_express_tests.tests_import import *


if __name__ == "__main__":
    test_axis = np.array([1, 1, 1])
    q_1 = Quaternion().set_from_axis_angle(test_axis, 20 * DEGREES)
    q_2 = Quaternion().set_from_axis_angle(test_axis, 30 * DEGREES)
    print(Quaternion.multiply_quat(q_1, q_2))
    print(Quaternion.multiply_quat_2(q_1, q_2))