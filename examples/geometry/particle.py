from examples.geometry.utils import *
from examples.example_imports import *

CONFIG.use_online_tex=1
class ParticleMultiRay(EagerModeScene):

    def clip1(self):
        origin, R = ORIGIN, 1.2
        particle = circ(origin, R)

        # TEXT = Text("Hello manim~ ")
        # TEXT.scale(0.2)
        # TEXT.set_color(BLUE)
        # TEXT.shift([-2, 2, 0])
        # self.play(ShowCreation(TEXT))

        self.play(ShowCreation(particle))

        def thetai2thetaPoint(theta_i):
            return PI - theta_i

        # theta_i1 = 30 * np.pi/180
        # self.add_rays(thetai2thetaPoint(theta_i1), particle, 2, 0.75)
        # self.add_rays(thetai2thetaPoint(45 * np.pi/180), particle, 2, 0.75)

        for theta in np.linspace(thetai2thetaPoint(PI/2), thetai2thetaPoint(PI/5), 20):
            self.add_rays(theta, particle, 3, 1.33)

        axes = ThreeDAxes()
        frame = self.camera.frame
        self.play(ShowCreation(axes))
        self.play(frame.animate.increment_theta(-30*DEGREES),
                  frame.animate.increment_phi(70 * DEGREES),
                  run_time = 1)

        # frame.set_euler_angles(
        #     theta=-30 * DEGREES,
        #     phi=70 * DEGREES,
        # )

        self.play(
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=2
        )

    def add_rays(self, theta1, particle, p=3, rm=1.33):
        point1 = particle.get_point_from_function(theta1)
        print(point1)
        point0 = np.array([-5, point1[1], point1[2]])

        ray1 = Arrow(point0, point1,buff=0, thickness=0.001)
        # ray1.set_opacity(0.1)
        ray1.set_color(WHITE)
        self.play(GrowArrow(ray1), run_time=0.3)

        theta_i = PI - theta1
        theta_r = calc_theta_r(theta_i, 1, rm)

        add_in_out_rays(self, point1, theta_i, theta_r, theta1, particle, pn=p,
                     show_in_rays=True, show_out_rays=True,
                     color_out=GREEN)

def add_in_out_rays(obj, point1, theta_i, theta_r, theta0, particle, pn,
                 show_in_rays=True, show_out_rays=True,
                 color_in=None, color_out=None):
    rays = []
    for p in range(pn):
        # theta_def = get_theta_def(theta_i, theta_r, p)
        if show_out_rays:
            out_ray, title = add_out_rays_title(theta_i, theta_r, p, point1, color=color_out)
            rays.append(out_ray)

        theta = theta0 - (PI - 2 * theta_r)
        point2 = particle.get_point_from_function(theta)

        if show_in_rays:
            in_ray = add_in_rays(point1, point2, color=color_in)
            rays.append(in_ray)

        point1 = point2
        theta0 = theta

    obj.play(*[GrowArrow(i) for i in rays], run_time=0.2)


class ParticleSimgleRay(EagerModeScene):

    def clip1(self):
        origin, R = np.array([0, 0, 0]), 1.2
        particle = circ(origin, R)
        self.play(ShowCreation(particle))

        for theta in np.linspace(PI/1.2, PI/1.2, 1):
            self.add_rays(theta, particle, p=3)

        axes = ThreeDAxes()
        frame = self.camera.frame
        # self.play(ShowCreation(axes))
        # self.play(frame.animate.increment_theta(-30*DEGREES),
        #           frame.animate.increment_phi(70 * DEGREES),
        #           run_time = 1)
        #
        #
        # self.play(
        #     frame.animate.increment_phi(-10 * DEGREES),
        #     frame.animate.increment_theta(-20 * DEGREES),
        #     run_time=2
        # )

    def add_rays(self, theta1, particle, p=3):
        point1 = particle.get_point_from_function(theta1)
        point0 = np.array([-5, point1[1], point1[2]])

        ray1 = Arrow(point0, point1,buff=0, thickness=0.01)
        ray1.set_opacity(1)
        ray1.set_color(GREEN)
        self.play(GrowArrow(ray1, run_time=0.3))

        theta_i = PI - theta1
        theta_r = calc_theta_r(theta_i, 1, 1.33)

        add_ray(self, point1, theta_i, theta_r, theta1, particle,
                pn=p,
                show_in_rays=True, show_out_rays=True,
                color_out=GREEN)

def add_ray(obj, point1, theta_i, theta_r, theta0, particle, pn,
                    show_in_rays=True, show_out_rays=True, show_text=True,
                    run_time = 0.4,
                    color_in=None, color_out=None):

    for p in range(pn):
        rays = []

        if show_out_rays:
            out_ray, title = add_out_rays_title(theta_i, theta_r, p, point1, color=color_out, show_text=show_text)
            rays.append(out_ray)
            obj.play(GrowArrow(out_ray), run_time=run_time)
            if show_out_rays and show_text:
                obj.play(ShowCreation(title))

        theta = theta0 - (PI - 2 * theta_r)
        point2 = particle.get_point_from_function(theta)

        if show_in_rays:
            in_ray = add_in_rays(point1, point2, color=color_in)
            if p != pn-1:
                rays.append(in_ray)
                obj.play(GrowArrow(in_ray), run_time=run_time)

        point1 = point2
        theta0 = theta


if __name__ == "__main__":
    ParticleMultiRay().render()
