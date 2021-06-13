import numpy as np
from manimlib import *


class Quaternion:
    def __init__(self, x=None, y=0, z=0, w=1):
        if issubclass(type(x), (np.ndarray, list, tuple)):
            self._x = x[0]
            self._y = x[1]
            self._z = x[2]
            self._w = x[3]
        else:
            if x is None:
                x = 1
            self._x = x
            self._y = y
            self._z = z
            self._w = w

        self._vec = np.array([self._x, self._y, self._z])
        self._q = np.array([*self._vec, self._w])

    def _set_q(self):
        self._vec = np.array([self._x, self._y, self._z])
        self._q = np.array([*self._vec, self._w])

    def get_array(self):
        return self._q

    def normalise(self):
        L = np.linalg.norm(self._vec)
        # self._q /= L
        self._x /= L
        self._y /= L
        self._z /= L
        self._w /= L
        self._set_q()

    def slerp(self):
        """TODO"""
        pass

    def multi(self, *quats):
        q = self
        for qi in quats:
            q = self.multiply_quat_2(q, qi)
        return q

    @staticmethod
    def multiply_quat(q1, q2):
        """reference http://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/code/index.htm"""
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
        v1 = q1._vec
        v2 = q2._vec
        w1 = q1._w
        w2 = q2._w
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
        self._set_q()

    def set_y(self, value):
        self._y = value
        self._set_q()

    def set_z(self, value):
        self._z = value
        self._set_q()

    def set_w(self, value):
        self._w = value
        self._set_q()

    def set_from_euler(self):
        """TODO"""
        pass

    def set_from_axis_angle(self, axis: np.ndarray, angle):
        axis = normalize(np.array(axis))
        half_angle = angle / 2
        s = np.sin(half_angle)

        self._x = axis[0] * s
        self._y = axis[1] * s
        self._z = axis[2] * s
        self._w = np.cos(half_angle)
        self._set_q()

        return self

    def conjugate(self, in_place=True):
        if in_place:
            self._vec *= -1
            self._set_q()
            return self
        else:
            q = self.copy()
            q._vec *= -1
            q._set_q()
            return q

    def invert(self):
        return self.conjugate()

    def dot(self, v):
        return self._q.dot(v)

    def __str__(self):
        return self._q.__str__()

    @property
    def x(self):
        return self._vec[0]

    @property
    def y(self):
        return self._vec[1]

    @property
    def z(self):
        return self._vec[2]

    @property
    def w(self):
        return self._w


if __name__ == "__main__":
    axis = np.array([1, 1, 1])
    q1 = Quaternion().set_from_axis_angle(axis, 20 * DEGREES)
    q2 = Quaternion().set_from_axis_angle(axis, 30 * DEGREES)
    print(Quaternion.multiply_quat(q1, q2))
    print(Quaternion.multiply_quat_2(q1, q2))
