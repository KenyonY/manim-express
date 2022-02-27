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

    def set_from_axis_angle(self, axis, angle):
        axis = normalize(np.array(axis))
        half_angle = angle / 2
        s = np.sin(half_angle)

        self._vec = axis * s
        self._w = np.cos(half_angle)
        return self

    def to_axis_angle(self):
        angle = 2 * math.acos(self.w)
        axis = self.vec / math.sqrt(1 - self.w ** 2)
        return axis, angle

    # def from_axis_angle(cls, vec):
    #     """Convert 3-vector in axis-angle representation to unit quaternion.
    #     Parameters
    #     ----------
    #     vec : (...N, 3) float array
    #         Each vector represents the axis of the rotation, with norm
    #         proportional to the angle of the rotation in radians.
    #     Returns
    #     -------
    #     q : array of quaternions
    #         Unit quaternions resulting in rotations corresponding to input
    #         rotations.  Output shape is rot.shape[:-1].
    #     """
    #     vec = np.asarray(vec)
    #     dtype = np.result_type(0.5, vec)
    #     quats = np.zeros(vec.shape[:-1] + (4,), dtype=dtype)
    #     quats[..., 1:] = 0.5 * vec[...]
    #     return np.exp(cls(quats))

    def to_euler_angles(self):
        """Open Pandora's Box.
        If somebody is trying to make you use Euler angles, tell them no, and
        walk away, and go and tell your mum.
        You don't want to use Euler angles.  They are awful.  Stay away.  It's
        one thing to convert from Euler angles to quaternions; at least you're
        moving in the right direction.  But to go the other way?!  It's just not
        right.
        Assumes the Euler angles correspond to the quaternion R via
            R = exp(alpha*z/2) * exp(beta*y/2) * exp(gamma*z/2)
        The angles are naturally in radians.
        NOTE: Before opening an issue reporting something "wrong" with this
        function, be sure to read all of the following page, *especially* the
        very last section about opening issues or pull requests.
        <https://github.com/moble/quaternion/wiki/Euler-angles-are-horrible>
        Returns
        -------
        alpha_beta_gamma : float array
            Output shape is q.shape+(3,).  These represent the angles (alpha,
            beta, gamma) in radians, where the normalized input quaternion
            represents `exp(alpha*z/2) * exp(beta*y/2) * exp(gamma*z/2)`.
        Raises
        ------
        AllHell
            ...if you try to actually use Euler angles, when you could have
            been using quaternions like a sensible person.
        """
        s = self.reshape((-1, 4))
        alpha_beta_gamma = np.empty((s.shape[0], 3), dtype=self.dtype)
        for i in range(s.shape[0]):
            n = s[i, 0] ** 2 + s[i, 1] ** 2 + s[i, 2] ** 2 + s[i, 3] ** 2
            alpha_beta_gamma[i, 0] = np.arctan2(s[i, 3], s[i, 0]) + np.arctan2(-s[i, 1], s[i, 2])
            alpha_beta_gamma[i, 1] = 2 * np.arccos(np.sqrt((s[i, 0] ** 2 + s[i, 3] ** 2) / n))
            alpha_beta_gamma[i, 2] = np.arctan2(s[i, 3], s[i, 0]) - np.arctan2(-s[i, 1], s[i, 2])
        return alpha_beta_gamma.reshape(self.shape[:-1] + (3,))

    def from_euler_angles(self, alpha_beta_gamma, beta=None, gamma=None):
        """Improve your life drastically.
        Assumes the Euler angles correspond to the quaternion R via
            R = exp(alpha*z/2) * exp(beta*y/2) * exp(gamma*z/2)
        The angles naturally must be in radians for this to make any sense.
        NOTE: Before opening an issue reporting something "wrong" with this
        function, be sure to read all of the following page, *especially* the
        very last section about opening issues or pull requests.
        <https://github.com/moble/quaternion/wiki/Euler-angles-are-horrible>
        Parameters
        ----------
        alpha_beta_gamma : float or array of floats
            This argument may either contain an array with last dimension of
            size 3, where those three elements describe the (alpha, beta, gamma)
            radian values for each rotation; or it may contain just the alpha
            values, in which case the next two arguments must also be given.
        beta : None, float, or array of floats
            If this array is given, it must be able to broadcast against the
            first and third arguments.
        gamma : None, float, or array of floats
            If this array is given, it must be able to broadcast against the
            first and second arguments.
        Returns
        -------
        R : quaternionic.array
            The shape of this array will be the same as the input, except that
            the last dimension will be removed.
        """
        # Figure out the input angles from either type of input
        if gamma is None:
            alpha_beta_gamma = np.asarray(alpha_beta_gamma)
            alpha = alpha_beta_gamma[..., 0]
            beta = alpha_beta_gamma[..., 1]
            gamma = alpha_beta_gamma[..., 2]
        else:
            alpha = np.asarray(alpha_beta_gamma)
            beta = np.asarray(beta)
            gamma = np.asarray(gamma)

        # Pre-compute trig
        cosβover2 = np.cos(beta / 2)
        sinβover2 = np.sin(beta / 2)

        # Set up the output array
        R = np.empty(np.broadcast(alpha, beta, gamma).shape + (4,), dtype=cosβover2.dtype)

        # Compute the actual values of the quaternion components
        R[..., 0] = cosβover2 * np.cos((alpha + gamma) / 2)  # scalar quaternion components
        R[..., 1] = -sinβover2 * np.sin((alpha - gamma) / 2)  # x quaternion components
        R[..., 2] = sinβover2 * np.cos((alpha - gamma) / 2)  # y quaternion components
        R[..., 3] = cosβover2 * np.sin((alpha + gamma) / 2)  # z quaternion components

        return self

    def from_spherical_coordinates(self, theta_phi, phi=None):
        """Return the quaternion corresponding to these spherical coordinates.
        Assumes the spherical coordinates correspond to the quaternion R via
            R = exp(phi*z/2) * exp(theta*y/2)
        The angles naturally must be in radians for this to make any sense.
        Note that this quaternion rotates `z` onto the point with the given
        spherical coordinates, but also rotates `x` and `y` onto the usual basis
        vectors (theta and phi, respectively) at that point.
        Parameters
        ----------
        theta_phi : float or array of floats
            This argument may either contain an array with last dimension of
            size 2, where those two elements describe the (theta, phi) values in
            radians for each point; or it may contain just the theta values in
            radians, in which case the next argument must also be given.
        phi : None, float, or array of floats
            If this array is given, it must be able to broadcast against the
            first argument.
        Returns
        -------
        R : quaternion array
            If the second argument is not given to this function, the shape
            will be the same as the input shape except for the last dimension,
            which will be removed.  If the second argument is given, this
            output array will have the shape resulting from broadcasting the
            two input arrays against each other.
        """
        # Figure out the input angles from either type of input
        if phi is None:
            theta_phi = np.asarray(theta_phi)
            theta = theta_phi[..., 0]
            phi = theta_phi[..., 1]
        else:
            theta = np.asarray(theta_phi)
            phi = np.asarray(phi)

        # Pre-compute trig
        cp = np.cos(phi / 2)
        ct = np.cos(theta / 2)
        sp = np.sin(phi / 2)
        st = np.sin(theta / 2)

        # Set up the output array
        R = np.empty(np.broadcast(theta, phi).shape + (4,), dtype=cp.dtype)

        # Compute the actual values of the quaternion components
        R[..., 0] = cp * ct  # scalar quaternion components
        R[..., 1] = -sp * st  # x quaternion components
        R[..., 2] = cp * st  # y quaternion components
        R[..., 3] = sp * ct  # z quaternion components

        return self

    def to_angular_velocity(self, t, t_new=None, axis=0):
        """Compute the angular velocity of quaternion timeseries with respect to `t`
        Note that this is the angular velocity of a rotating frame given by the
        quaternionic array, assuming that the quaternions take inertial vectors in the
        current frame to vectors in the rotating frame.
        Parameters
        ----------
        t : array-like of float
            This array represents the times at which the quaternions are measured, and
            with respect to which the derivative will be taken.  Note that these times
            must be real, finite and in strictly increasing order.
        t_new : array-like of float, optional
            If present, the output is interpolated to this set of times.  Defaults to
            None, meaning that the original set of times will be used.
        axis : int, optional
            Axis along which this array is assumed to be varying with `t`. Meaning that
            for t[i] the corresponding quaternions are `np.take(self, i, axis=axis)`.
            Defaults to 0.
        Notes
        -----
        For both unit and non-unit quaternions `Q`, we define the angular velocity as
            ω = 2 * dQ/dt * Q⁻¹
        This agress with the standard definition when `Q` is a unit quaternion and we
        rotate a vector `v` according to
            v' = Q * v * Q̄ = Q * v * Q⁻¹,
        in which case ω is a "pure vector" quaternion, and we have the usual
            dv'/dt = ω × v'.
        It also generalizes this to the case where `Q` is not a unit quaternion, which
        means that it also rescales the vector by the amount Q*Q̄.  In this case, ω also
        has a scalar component encoding twice the logarithmic time-derivative of this
        rescaling, and we have
            dv'/dt = ω * v' + v' * ω̄.
        """
        from scipy.interpolate import CubicSpline
        spline = CubicSpline(t, self, axis=axis)
        if t_new is None:
            Q = self  # shortcut
        else:
            Q = type(self)(spline(t_new))
        t_new = t if t_new is None else t_new
        Q̇ = type(self)(spline.derivative()(t_new))
        return (2 * Q̇ / Q).vector

    def from_angular_velocity(self, omega, t):
        pass

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
