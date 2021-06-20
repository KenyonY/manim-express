from examples.example_imports import *
# SceneArgs.color = "#ffffff"
scene = EagerModeScene()
image = ImageMobject("logo1.png").set_opacity(1).scale(1.5)


class AnimateAbc:

    def scale(self):
        return self

    def shift(self):
        return self


c = Circle()
print(dir(c))

c2 = Circle()
c2.animate.scale(2)
scene.play(c.animate.scale(2).add(c2))
scene.play(FadeOut(c))

scene.play(ShowCreation(c))
scene.hold_on()

