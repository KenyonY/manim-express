from manim_express_tests.tests_import import *


if __name__ == "__main__":
    vec_list = [2, 1, 1]

    vec3 = Vec3(*vec_list)
    m_vec = Arrow(ORIGIN, vec_list, buff=0)

    axis = [1, 2, 1]
    angle = 45 * DEGREES

    m_vec.rotate(angle, axis)

    # print(quat_conjugate(np.array(Q), style=1))
    # print(quaternion_conjugate(Q))
    q = Quaternion().set_from_axis_angle([1, 1, 1], 45 * DEGREES)
    print(q, 'q')
    print(vec3.apply_quaternion(q))
    print(m_vec.get_end())