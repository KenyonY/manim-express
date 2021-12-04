from manimlib import *


class Quaternion:
    def __init__(self, x=0, y=0, z=0, w=1):
        """Quaternion style [x, y, z, w]"""
        self._q = np.array([x, y, z, w], dtype=float)

    @property
    def _vec(self):
        return self._q[:3]

    @_vec.setter
    def _vec(self, value):
        self._q[:3] = value

    @property
    def _x(self):
        return self._q[0]

    @_x.setter
    def _x(self, value):
        self._q[0] = value

    @property
    def _y(self):
        return self._q[1]

    @_y.setter
    def _y(self, value):
        self._q[1] = value

    @property
    def _z(self):
        return self._q[2]

    @_z.setter
    def _z(self, value):
        self._q[2] = value

    @property
    def _w(self):
        return self._q[3]

    @_w.setter
    def _w(self, value):
        self._q[3] = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w

    @property
    def vec(self):
        return self._vec

    @property
    def q(self):
        return self._q

    def set_q(self, x, y, z, w):
        self._q[0] = x
        self._q[1] = y
        self._q[2] = z
        self._q[3] = w

    def to_array(self):
        return self.q

    def norm(self):
        return np.linalg.norm(self._q)

    def normalise(self):
        L = self.norm()
        self._q = self._q / L
        return self

    def slerp(self):
        """TODO"""
        pass

    def multi(self, *quats):
        q = self
        for qi in quats:
            q = self.multiply_quat_2(q, qi)
        self.set_q(*q._q)
        return q

    @staticmethod
    def multiply_quat(q1, q2):
        """reference 
        https://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/code/index.htm"""
        x = q1.x * q2.w + q1.y * q2.z - q1.z * q2.y + q1.w * q2.x
        y = -q1.x * q2.z + q1.y * q2.w + q1.z * q2.x + q1.w * q2.y
        z = q1.x * q2.y - q1.y * q2.x + q1.z * q2.w + q1.w * q2.z
        w = -q1.x * q2.x - q1.y * q2.y - q1.z * q2.z + q1.w * q2.w
        new_q = object.__new__(Quaternion)
        new_q.__init__(x, y, z, w)
        return new_q

    @classmethod
    def multiply_quat_2(cls, q1, q2):
        """Graßmann Product"""
        q1: cls
        q2: cls
        v1, v2 = q1.vec, q2.vec
        w1, w2 = q1.w, q2.w
        vec = w1 * v2 + w2 * v1 + np.cross(v1, v2)
        w = w1 * w2 - v1.dot(v2)

        new_q = object.__new__(Quaternion)
        new_q.__init__(*vec, w)
        return new_q

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def copy(self):
        obj = object.__new__(Quaternion)
        obj.__init__(*self._q)
        return obj

    def set_from_euler(self):
        """TODO"""

    def to_euler(self):
        """TODO"""

    def set_from_axis_angle(self, axis, angle):
        axis = normalize(np.array(axis))
        half_angle = angle / 2
        s = np.sin(half_angle)

        self._vec = axis * s
        self._w = np.cos(half_angle)
        return self

    def set_from_unit_vectors(self, v_from, v_to):
        """Assumes direction vectors vec1 and vec2 are normalized."""
        r = 1 + v_from.dot(v_to)
        if r < EPSILON:
            r = 0
            if abs(v_from.x) > abs(v_from.z):
                self._x = -v_from.y
                self._y = v_from.x
                self._z = 0
                self._w = r
            else:
                self._x = 0
                self._y = -v_from.z
                self._z = v_from.y
                self._w = r
        else:
            self._x = v_from.y * v_to.z - v_from.z * v_to.y
            self._y = v_from.z * v_to.x - v_from.x * v_to.z
            self._z = v_from.x * v_to.y - v_from.y * v_to.x
            self._w = r
            # self._vec = np.cross(v_from.to_array(), v_to.to_array())
            # self._q[3] = r

        return self.normalise()

    def to_axis_angle(self):
        angle = 2 * math.acos(self.w)
        axis = self.vec / math.sqrt(1 - self.w ** 2)
        return axis, angle

    def conjugate(self, in_place=True):
        if in_place:
            self._vec = -1 * self._vec
            return self
        else:
            q = self.copy()
            q._vec = -1 * q._vec
            return q

    def invert(self):
        return self.conjugate()

    def dot(self, q):
        return self._q.dot(q)

    def __str__(self):
        return self._q.__str__()

    def __repr__(self):
        return self._q.__str__()

    def __len__(self):
        return 4

    def __getitem__(self, item: int):
        return self._q[item]

    def __setitem__(self, item: int, value):
        self._q[item] = value

    def __iter__(self):
        for value in self._q:
            yield value


if __name__ == "__main__":
    from .. import *
    from .vec import Vec3
    import sys
    sys.path.extend([plan_root_path])
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
