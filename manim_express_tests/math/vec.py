from manim_express_tests.tests_import import *


class A(EagerModeScene):
    def clip9(self):
        vector_from = Vec3(0, 0, 1)
        vec_arrow = Arrow(ORIGIN, vector_from.to_array(), buff=0)

        def plane_surface(u, v):
            x = u
            y = v
            z = 1
            return [x, y, z]

        plane = ParametricSurface(
            plane_surface,
            u_range=(-1, 1),
            v_range=(-1, 1),

        )
        self.camera.frame.set_euler_angles(
            45 * DEGREES,
            45 * DEGREES
        )
        self.add(ThreeDAxes())
        self.add(vec_arrow)
        self.play(ShowCreation(plane))
        vector_to = Vec3(1, 1, 1)
        self.add(Arrow(ORIGIN, vector_to.to_array(), buff=0).set_color(RED))
        quat = Quaternion().set_from_unit_vectors(vector_from.copy().normalise(),
                                                  vector_to.copy().normalise())
        axis, angle = quat.to_axis_angle()
        q_2 = Quaternion().set_from_axis_angle(axis, angle)
        print(f"{vector_from}, {vector_to}")
        vector_from.apply_quaternion(q_2)
        print(f"after apply quat: {vector_from}")

        # self.play(vec_arrow.animate.rotate(angle, axis))
        # self.play(plane.animate.rotate(angle, axis))
        self.play(vec_arrow.animate.rotate_about_origin(angle, axis))
        self.play(plane.animate.rotate_about_origin(angle, axis))


A().render()

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
