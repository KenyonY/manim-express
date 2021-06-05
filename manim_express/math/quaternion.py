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
        self._q = None
        self._vec = None
        self._set_q()

    def _set_q(self):
        self._vec = np.array([self._x, self._y, self._z])
        self._q = np.array([*self._vec, self._w])

    def get_array(self):
        return self._q

    def slerp(self):
        """TODO"""
        pass

    def multi(self, *quats):
        q = self
        for qi in quats:
            print(q)
            q = self.multiply_quat(q, qi)
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


if __name__ == "__main__":
    q = Quaternion()
