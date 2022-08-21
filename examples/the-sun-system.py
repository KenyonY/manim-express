from example_imports import *


class TheSunSystem(EagerModeScene):
    def __init__(self):
        super().__init__()
        self._earth_orbit_radius = 5
        self._moon_orbit_radius = 1

        self.sun = self.create_sun(center=ORIGIN)
        self.ertch_orbit = Circle(radius=self._earth_orbit_radius, color=YELLOW).move_to(ORIGIN)
        self.earth = self.create_earth(center=self.ertch_orbit.point_at_angle(30 * DEGREES))
        self.moon_orbit = Circle(radius=self._moon_orbit_radius, color=BLUE).move_to(self.earth.get_center())
        self.moon = self.create_moon(center=self.moon_orbit.point_at_angle(60 * DEGREES))

        self.add(self.ertch_orbit, self.earth, self.moon_orbit, self.moon)

        self.add(self.sun, self.earth, self.moon)

    def create_orbits(self, earth):
        pass

    def create_sun(self, center=ORIGIN):
        sun = Sphere(radius=0.5, color=YELLOW).move_to(center)
        return sun

    def create_earth(self, center=RIGHT * 2):
        earth = Sphere(radius=0.2, color=BLUE).move_to(center)
        return earth

    def create_moon(self, center=RIGHT * 2):
        moon = Sphere(radius=0.1, color=WHITE).move_to(center)
        return moon

    def start(self):
        self.earth.add_updater(lambda e, dt: e.rotate(dt, about_point=ORIGIN))
        self.moon.add_updater(lambda m, dt: m.rotate(dt*3, about_point=self.earth.get_center()))

    def clip_1(self):
        self.start()


TheSunSystem().render()
