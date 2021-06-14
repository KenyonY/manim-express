from examples.example_imports import *
scene = EagerModeScene(screen_size=Size.bigger)

surface = CustomSurface()
sphere = surface.sphere(r=2, origin=LEFT*2).set_color_by_gradient((BLUE_E, YELLOW_D, RED_E))

# ellipsoid = surface.ellipsoid(1, 2, 3)
# cylinder = surface.cylinder(1).move_to(RIGHT*2)
# random_surface = surface.para_hyp().move_to(DL*3)

scene.play(ShowCreation(sphere))
s = Sphere()
s.move_to(RIGHT * 3).set_color_by_gradient((BLUE_E, YELLOW_D, RED_E))
scene.play(ShowCreation(s), run_time=2)
# scene.play(ShowCreation(ellipsoid))
# scene.play(ShowCreation(cylinder))
# scene.play(ShowCreation(random_surface))



scene.hold_on()

