from examples.example_imports import *
scene = EagerModeScene()

scene.add(Triangle().scale(3).move_to(LEFT*5))
scene.add(FullScreenRectangle())
screen = ScreenRectangle()

screen.set_height(6.0)
screen.set_stroke(WHITE, 2)
screen.set_fill(BLACK, 1)
screen.to_edge(DOWN)

screen.add(Triangle())
animated_screen = AnimatedBoundary(screen)
scene.add(screen, animated_screen)
scene.wait(16)

scene.hold_on()