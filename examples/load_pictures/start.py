from examples.example_imports import *
SceneArgs.color = "#ffffff"
scene = EagerModeScene()
image = ImageMobject("logo1.jpg")
image2 = ImageMobject("logo1.png").set_opacity(1).scale(1.5).rotate(30*DEGREES)



image.move_to(LEFT*2)
# scene.add(image)
scene.add(image2)

scene.hold_on()

