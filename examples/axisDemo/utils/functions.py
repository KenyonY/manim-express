import numpy as np
from sympy import symbols, linsolve, nonlinsolve, core, sin, cos, solveset
import sympy

import warnings
# from guang.sci.scattering import
# from manimlib.mobject.coordinate_systems import
from manimlib.utils.space_ops import rotate_vector, line_intersection
from manimlib.utils.space_ops import angle_of_vector, normalize, get_unit_normal, angle_between_vectors


class SolveSystem:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z', real=True)
        self.epsilon = 1e-5

    def solve1(self, sfunc, x=None, y=None, precision=5):
        if y == None:
            roots = solveset(sfunc.subs(self.x, x), self.y)
        else:
            roots = solveset(sfunc.subs(self.y, y), self.x)
        print(roots)
        res = [i.evalf(precision) for i in roots]
        return res

    def solve2(self, eq1, eq2, precision=5):
        system = [eq1, eq2]
        solve_result = nonlinsolve(system, [self.x, self.y])
        intersections = []
        for i in solve_result:
            coord = [j.evalf(precision) for j in i if j.is_real]
            if coord == []: continue
            intersections.append(coord)
        if intersections == []:
            warnings.warn("There is No root!")

        return intersections

    def get_circle_sfunc(self, origin, r):
        return (self.x - origin[0])**2 + (self.y-origin[1])**2 - r**2

    def line_func(self, p0, direction):
        p0 = np.array(p0)
        direction = np.array(direction)
        if direction[0] != 0:
            k = direction[1] / direction[0]
            return lambda x, y:(y - p0[1]) - k * (x - p0[0])
        elif direction[1] != 0:
            k = direction[0] / direction[1]
            return lambda x, y: k * (y - p0[1]) - (x - p0[0])
        else:
            raise ValueError("point's x and y cann't be both zero!")


    def get_line_sfunc(self, p0, p1=None, direction=None):
        p0 = np.array(p0)

        if p1 is not None:
            p1 = np.array(p1)
            n = p1.size
            if n == 2:
                return (self.x - p0[0])/(p1[0]-p0[0]) - (self.y - p0[1])/(p1[1] - p0[1])
            elif n == 3:
                # needs be test
                return [(self.x - p0[0])/(p1[0]-p0[0]) - (self.y - p0[1])/(p1[1] - p0[1]),
                        (self.x - p0[0])/(p1[0]-p0[0]) - (self.z - p0[2])/(p1[2] - p0[2]),
                        (self.y - p0[1])/(p1[1]-p0[1]) - (self.z - p0[2])/(p1[2] - p0[2])]

        elif direction is not None:
            # 2d
            direction = np.array(direction)
            if direction[0] != 0:
                k = direction[1]/direction[0]
                return (self.y - p0[1]) - k*(self.x - p0[0])
            elif direction[1] != 0:
                k = direction[0]/direction[1]
                return k*(self.y - p0[1]) - (self.x - p0[0])
            else:
                raise ZeroDivisionError
        else:
            ValueError("One of `p1` and `direction` must be given.")

    def sym2numerical(self, func, x=None, y=None, z=None):
        return func.subs([(self.x, x), (self.y, y), (self.z, z)])


    def calc_tangent(self, point, sfunc, root_index=1):
        # method1
        point = np.array(point)
        x0, y0 = point[0], point[1]
        x1 = x0+ self.epsilon
        y1_list = self.solve1(sfunc, x=x1)
        print(y1_list)
        y1 = y1_list[root_index]
        tangent1 = (y1- y0) /(x1-x0)

        # method2 直接求导（但是对于参数函数不是太好求...）

        return tangent1

    def get_circ_normal(self, point, origin):
        '''3d inputs'''
        print(point, origin, 'point and origin')
        point, origin = np.array(point), np.array(origin)
        normal = np.array([point[0]-origin[0], point[1] - origin[1], point[2] - origin[2] ])
        return normalize(normal)

    def reflect(self, direction, normal, p):
        direction = np.array(direction)
        normal = np.array(normal)
        angle = angle_between_vectors( direction, normal)
        if p == 0:
            angle = angle if np.pi - angle > angle else np.pi - angle
            angle = -angle
        # else:
        #     angle = -angle
        reflect_direction = rotate_vector(normal, angle)
        return reflect_direction

    def in_reflect(self, direction, normal):
        direction = np.array(direction)
        normal = np.array(normal)
        angle = angle_between_vectors( direction, normal)
        # angle = angle if np.pi - angle > angle else np.pi - angle
        reflect_direction = rotate_vector(normal, -angle)
        return reflect_direction

    def get_incident_angle(self, direction, normal):
        direction, normal = np.array(direction), np.array(normal)
        angle = angle_between_vectors(direction, normal)
        angle = angle if np.pi - angle > angle else np.pi - angle
        return angle

    def get_refraction_direction(self, direction, normal, n_from, n_to, p=0):
        theta_i = self.get_incident_angle(direction, normal)
        # snell_law
        # n1* np.sin(theta1) = n2 * np.sin(theta2)
        theta_r = np.arcsin(n_from / n_to * np.sin(theta_i))

        if p == 0:
            refraction_direction = normalize(rotate_vector(-normal, theta_r))
        else:
            refraction_direction = normalize(rotate_vector(normal, -theta_r))

        return refraction_direction




if __name__ == "__main__":
    ss = SolveSystem()
    eq1 = ss.get_line_sfunc([1, 1], direction=[1, -1])
    eq2 = ss.get_circle_sfunc([0, 1], 1)
    print(eq2)
    print(ss.sym2numerical(eq2, x=1, y=2))
    # number = eq2.subs([(ss.x,1), (ss.y, 2)])
    # n2 = eq2.evalf(5, subs={ss.x: 1, ss.y: 2})
    # print(ss.calc_tangent(eq2, x=1, y=2))
    # print(ss.solve2(eq1, eq2))

    # print('emmm', ss.solve1(eq2, x=0.5))
    ss.calc_tangent([0., 0.999], eq2)
    print(ss.get_circ_normal([1, 1, 0], [0, 0, 0]))
    (ss.reflect(np.array([1, 0, 0]), [-1, 1, 0]))