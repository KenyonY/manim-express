from manim_imports_ext import *
from scatter import ParticleSystem, SimgleRay


class ScatteringModel(Scene):
    def construct(self):
        p1 = ParticleSystem()
        self.play(ShowCreation(p1.get_axes()))
        R = 3

        p1.create_particle(LEFT*2, R, GREEN)
        # p1.create_particle(RIGHT*2, 3, WHITE)

        p1.create_lights()

        for i in p1.get_particles()['particle']:
            self.play(ShowCreation(i),  run_time=0.1)
            # self.add(i)

        for rays in p1.get_lights():
            for i in rays:
               self.play(ShowCreation(i),  run_time=0.2)




        

