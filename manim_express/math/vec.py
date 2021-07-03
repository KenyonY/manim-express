import numpy as np
from manimlib import *
from .quaternion import Quaternion
from abc import ABCMeta, abstractmethod


class Vec(metaclass=ABCMeta):
    @abstractmethod
    def _set_vec(self, *args, **kwargs):
        pass

    @abstractmethod
    def _set_xy_and_more(self, *args, **kwargs):
        pass

    @abstractmethod
    def to_array(self, *args, **kwargs):
        pass

    @abstractmethod
    def normalise(self):
        pass


class Vec2(Vec):
    _x, _y = None, None
    _vector = None

    def __init__(self, sub_class):
        self._subclass = sub_class

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _set_vec(self):
        self._vector = np.array([self._x, self._y])

    def to_array(self):
        return self._vector

    def _set_xy(self):
        self._x = self._vector[0]
        self._y = self._vector[1]

    def _set_xy_and_more(self, *args, **kwargs):
        self._set_xy()

    def norm(self):
        return np.linalg.norm(self._vector)

    def __str__(self):
        return self._vector.__str__()

    def _new(self, *args, **kwargs):
        return self._subclass(*args, **kwargs)
    # def _new(self, *args, **kwargs):
    #     pass

    def normalise(self):
        L = self.norm()
        self._x /= L
        self._y /= L
        self._set_vec()
        return self

    def dot(self, vec):
        if isinstance(vec, self._subclass):
            vec = vec.to_array()
        res = self._vector.dot(vec)
        return res

    def __add__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        return self._new(*(self._vector + other))

    # 当实现了 __add__, 即使不手动实现__iadd__也是安全的，
    # python会自动为其分配调用实例， 即可以使用 += 操作。
    # __sub__, __mul__同理。
    def __iadd__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        self._vector = self.to_array() + other
        self._set_xy_and_more()
        return self

    # 反向add, 如 2 + Vec()
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        return self._new(*(self.to_array() - other))

    def __isub__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        self._vector = self.to_array() - other
        self._set_xy_and_more()
        return self

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        return self._new(*(self.to_array() * other))

    def __imul__(self, other):
        if isinstance(other, self._subclass):
            other = other.to_array()
        self._vector = self.to_array() * other
        self._set_xy_and_more()
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __getitem__(self, item):
        return self._vector[item]


class Vec3(Vec2):

    def __init__(self, x=None, y=1, z=1):
        super().__init__(Vec3)
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
    def z(self):
        return self._z

    def _set_vec(self):
        self._vector = np.array([self._x, self._y, self._z])

    def _set_xy_and_more(self, *args, **kwargs):
        self._x = self._vector[0]
        self._y = self._vector[1]
        self._z = self._vector[2]

    def to_array(self):
        return self._vector

    def normalise(self):
        L = self.norm()
        self._x /= L
        self._y /= L
        self._z /= L
        self._set_vec()
        return self

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



    def rotate(self, angle, axis=(0, 0, 1)):
        q = Quaternion().set_from_axis_angle(axis, angle)
        self.apply_quaternion(q)
        return self

    @classmethod
    def _new(cls, x, y, z):
        obj = object.__new__(Vec3)
        obj.__init__(x, y, z)
        return obj

    def copy(self):
        obj = object.__new__(Vec3)
        obj.__init__(*self._vector)
        return obj




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
