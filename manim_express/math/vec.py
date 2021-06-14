import numpy as np
from manimlib import *
from .quaternion import Quaternion


class Vec3:
    def __init__(self, x=None, y=1, z=1):
        if issubclass(type(x), (np.ndarray, list, tuple)):
            self._x = x[0]
            self._y = x[1]
            self._z = x[2]
        else:
            if x is None:
                x = 1
            self._x = x
            self._y = y
            self._z = z

        self._vector = None
        self._set_vec()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def _set_vec(self):
        self._vector = np.array([self._x, self._y, self._z])

    def apply_quaternion(self, q: Quaternion):
        x, y, z = self._x, self._y, self._z
        # calculate quat * vector
        ix = q.w * x + q.y * z - q.z * y
        iy = q.w * y + q.z * x - q.x * z
        iz = q.w * z + q.x * y - q.y * x
        iw = -q.x * x - q.y * y - q.z * z

        # calculate result * inverse quat
        self._x = ix * q.w + iw * -q.x + iy * -q.z - iz * -q.y
        self._y = iy * q.w + iw * -q.y + iz * -q.x - ix * -q.z
        self._z = iz * q.w + iw * -q.z + ix * -q.y - iy * -q.x

        self._set_vec()
        return self

    def dot(self, vec):
        self._vector.dot(vec)

    def to_array(self):
        return self._vector

    def copy(self):
        obj = object.__new__(Vec3)
        obj.__init__(*self._q)
        return obj

    def __str__(self):
        return self._vector.__str__()


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
