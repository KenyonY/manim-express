from manim_imports_ext import *
from manimlib.utils.config_ops import digest_config
from utils.functions import SolveSystem


class ParticleSystem:
    def __init__(self) -> None:

        self.axes = Axes(
            x_range=[-6, 6], y_range=[-6, 6],
            height=8, width=8,
            axis_config={
                # "include_tip": False,
                "numbers_to_exclude": [],
            }
        )
        for axis in self.axes:
            axis.add_numbers(range(-4, 6, 2), color=GREY_B)
            # axis.numbers[4].set_opacity(0)

        self.particles_params = []
        self.particles = []
        self.lights = []
        

    def get_axes(self):
        return self.axes

    def get_particles(self):
        return {'particle': self.particles,
                'params': self.particles_params}
    
    def get_lights(self):
        return self.lights

    def create_particle(self, origin, r, color=RED):
        self.particles_params.append({'origin': origin, 'r':r})
        self.particles.append(self.circ(origin, r, color))
        
    def create_lights(self, n=10, orient='x', unit=1):

        sr= SimgleRay()
        for i in range(5):
            ray = sr.create_ray([-10, 2.5 -0.2*i, 0], RIGHT, self.get_particles()['params'])
            self.lights.append(ray)



    def circ(self, origin, r, color=RED):
        circle = ParametricCurve(
            lambda theta: self.axes.c2p(*np.array([
                r * np.cos(theta) + origin[0],
                r * np.sin(theta) + origin[1],
                origin[2]
            ])),
            [0, 2*TAU],
            color=color
        )
        return circle


class SimgleRay(ParticleSystem):
    CONFIG = {
        "range": [0, 1, 0.222]
    }

    def __init__(self,
                 coord=np.array([-4, 0, 0]),
                 wavelength=632,
                 rm=1,
                 orientation=RIGHT,
                 **kwargs
                 ):
        super(SimgleRay, self).__init__()
        digest_config(self, kwargs)
        self.c = 2.9979
        self.rm = rm  # refractive index real part
        self.im = 0  # refractive index image part (unused)
        self.wavelength = wavelength  # wavelength
        self.v = self.c  # light speed
        self.frequency = self.v / self.wavelength

        self.orientation = orientation
        self.current_coord = coord

        self.need_update_v = False
        self.need_update_orientation = False

        self.ss = SolveSystem()

        # print(self.__dict__)
        # print(self.range)

    def set_m(self, rm, im):
        self.rm = rm
        self.im = im

    def get_v(self):
        return self.v

    def update_v(self):
        self.v = self.c / self.rm
        self.need_update_v = False

    def update_orientation(self):
        # update from refrective index
        self.need_update_orientation = False

    def update_status(self):
        if self.need_update_v:
            self.update_v()

        if self.need_update_orientation:
            self.update_oritation()



    def line_circ_intersect(self,p0, direction, r, origin):
        line_eq = self.ss.get_line_sfunc(p0, direction=direction)
        circ_eq = self.ss.get_circle_sfunc(origin=origin, r=r)
        # print(line_eq, '\n', circ_eq)
        result_points = self.ss.solve2(line_eq, circ_eq, precision=5)
        if direction[0] > 0:
            pass
        if result_points[0] == p0:
            p1 = result_points[1]
        else:
            p1 = result_points[0]
        return p1

    def out_ray(self, start, direction, color=RED, ray_length=3):
        start = np.array(start)
        if len(start) == 2:
            start = np.array([*start, 0])
        end = start + direction * ray_length
        arrow = Arrow(
            self.axes.c2p(*np.array([start[0], start[1], 0])),
            self.axes.c2p(*np.array([end[0], end[1], 0])),
            buff=0,
            thickness=0.04
        )
        arrow.set_color(color)
        return arrow

    def segment_ray(self,p0, p1, color=RED):
        ray = Arrow(
            self.axes.c2p(*np.array([p0[0], p0[1], 0])),
            self.axes.c2p(*np.array([p1[0], p1[1], 0])),
            buff=0,
            thickness=0.03
        )
        ray.set_color(color)
        # rays[-1].set_stroke(width=0.1, opacity=1)
        return ray

    def create_ray(self, start, direction, particles_params, color=GREEN):
        """
        start: 2d point coordinate
        end: 2d point coordinate
        """
        rays = []

        for particle_param in particles_params:

            p0 = start
            r = particle_param['r']
            origin = particle_param['origin']
            p1 = self.line_circ_intersect(p0, direction, r, origin)
            # 第一部分光线段
            rays.append(self.segment_ray(p0, p1, color=BLUE))
            p0 = p1

            # 从这里开始 光线每一次碰到颗粒边界将分为两部分：反射和折射
            p = 0
            for _ in range(3):
                normal = self.ss.get_circ_normal([*p0, 0], [*particle_param['origin'], 0])

                reflect_direction = self.ss.reflect(direction, normal, p)
                if p == 0:
                    refraction_direction = self.ss.get_refraction_direction(direction, normal, n_from=1, n_to=1.33, p=p)
                    p1 = self.line_circ_intersect(p0, refraction_direction, r, origin)
                    rays.append(self.out_ray(p0, reflect_direction, color=GREEN))
                    rays.append(self.segment_ray(p0, p1, color=RED))
                else:
                    refraction_direction = self.ss.get_refraction_direction(direction, normal, n_from=1.33, n_to=1, p=p)
                    p1 = self.line_circ_intersect(p0, reflect_direction, r, origin)
                    rays.append(self.out_ray(p0, refraction_direction, color=GREEN))
                    rays.append(self.segment_ray(p0, p1, color=RED))



                print('normal', normal)
                print('reflect', f'p={p}', reflect_direction)


                direction = refraction_direction if p == 0 else reflect_direction
                p += 1
                p0 = p1

        return rays


    # def sphere(origin, r):
#     sphere0 = ParametricSurface(
#         lambda u, v: np.array([
#             r * np.cos(u) * np.cos(v) - origin[0],
#             r * np.cos(u) * np.sin(v) - origin[1],
#             r * np.sin(u) - origin[2]
#         ]),
#         v_min=0, v_max=TAU, u_min=-PI / 2, u_max=PI / 2,
#         # checkerboard_colors=[RED_D, RED_E],
#         # resolution=(15, 32)
#     )
#     return sphere0

