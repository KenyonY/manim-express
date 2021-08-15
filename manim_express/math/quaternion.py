from manimlib import *


class Quaternion:
    def __init__(self, x=None, y=0, z=0, w=1):
        """Quaternion style [x, y, z, w]"""
        if issubclass(type(x), (np.ndarray, list, tuple)):
            self._x = x[0]
            self._y = x[1]
            self._z = x[2]
            self._w = x[3]
        else:
            if x is None:
                x = 0
            self._x = x
            self._y = y
            self._z = z
            self._w = w

        self._q = np.array([self._x, self._y, self._z, self._w], dtype=float)
        self._vec = self._q[:3]

    def set_q(self, x, y, z, w):
        self._q[0] = x
        self._q[0] = y
        self._q[0] = z
        self._q[0] = w

    def _xyzw_to_q(self):
        self._q[0] = self._x
        self._q[1] = self._y
        self._q[2] = self._z
        self._q[3] = self._w

    def _xyz_to_vec(self):
        self._vec[0] = self._x
        self._vec[1] = self._y
        self._vec[2] = self._z

    def _q_to_xyzw(self):
        self._x, self._y, self._z, self._w = self._q[0], self._q[1], self._q[2], self._q[3]

    def _vec_to_xyz(self):
        self._x, self._y, self._z = self._vec[0], self._vec[1], self._vec[2]

    def to_array(self):
        return self._q

    def get_axis_vec(self):
        return self._q[:3]

    def norm(self):
        return np.linalg.norm(self._q)

    def normalise(self):
        L = self.norm()
        # self._q /= L
        self._x /= L
        self._y /= L
        self._z /= L
        self._w /= L
        self._xyzw_to_q()
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

    @staticmethod
    def multiply_quat_2(q1, q2):
        """Graßmann Product"""
        v1 = q1.get_axis_vec()
        v2 = q2.get_axis_vec()
        w1 = q1.w
        w2 = q2.w
        vec = w1 * v2 + w2 * v1 + np.cross(v1, v2)
        w = w1 * w2 - v1.dot(v2)

        new_q = object.__new__(Quaternion)
        new_q.__init__([*vec, w])
        return new_q

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def copy(self):
        obj = object.__new__(Quaternion)
        obj.__init__(*self._q)
        return obj

    def set_x(self, value):
        self._x = value
        self._xyzw_to_q()

    def set_y(self, value):
        self._y = value
        self._xyzw_to_q()

    def set_z(self, value):
        self._z = value
        self._xyzw_to_q()

    def set_w(self, value):
        self._w = value
        self._xyzw_to_q()

    def set_from_euler(self):
        """TODO"""
        pass

    def set_from_axis_angle(self, axis, angle):
        axis = normalize(np.array(axis))
        half_angle = angle / 2
        s = np.sin(half_angle)

        self._x = axis[0] * s
        self._y = axis[1] * s
        self._z = axis[2] * s
        self._w = np.cos(half_angle)
        self._xyzw_to_q()

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
            self._xyzw_to_q()
        else:
            self._x = v_from.y * v_to.z - v_from.z * v_to.y
            self._y = v_from.z * v_to.x - v_from.x * v_to.z
            self._z = v_from.x * v_to.y - v_from.y * v_to.x
            self._w = r
            self._xyzw_to_q()
            # vec = np.cross(v_from.to_array(), v_to.to_array())
            # self._q[0], self._q[1], self._q[2] = vec[0], vec[1], vec[2]
            # self._q[3] = r
            # self._q_to_xyzw()

        return self.normalise()

    def to_axis_angle(self):
        angle = 2 * math.acos(self.w)
        axis = self._vec / math.sqrt(1 - self.w ** 2)
        return axis, angle

    def conjugate(self, in_place=True):
        if in_place:
            self._vec *= -1
            return self
        else:
            q = self.copy()
            q._vec *= -1
            return q

    def invert(self):
        return self.conjugate()

    def dot(self, v):
        return self._q.dot(v)

    def __str__(self):
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

    @property
    def x(self):
        return self._q[0]

    @property
    def y(self):
        return self._q[1]

    @property
    def z(self):
        return self._q[2]

    @property
    def w(self):
        return self._q[3]
