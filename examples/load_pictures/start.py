from examples.example_imports import *
# SceneArgs.color = "#ffffff"
scene = EagerModeScene()
image = ImageMobject("logo1.png").set_opacity(1).scale(1.5)


c = Circle()
print(dir(c))

c2 = Circle()
scene.write(c2)
# c2.animate.scale(2)
scene.play(c2.scale, 2)
scene.fade_out(c2)
# scene.play(c.animate.scale(2).add(c2))
# scene.play(FadeOut(c))


