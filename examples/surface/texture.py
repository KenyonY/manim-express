from examples.example_imports import *


scene = EagerModeScene(screen_size=Size.bigger)

surface_text = Text("For 3d scenes, try using surfaces")
texText = TexText("\\LaTeX kasdflkalsdkfj "
                  " $\\sum_{n=1}^\\infty$")

scene.add(texText)

surface_text.fix_in_frame()
surface_text.to_edge(UP)
scene.add(surface_text)
scene.wait(0.1)

torus1 = Torus(r1=1, r2=1)
torus2 = Torus(r1=3, r2=1)
sphere = Sphere(radius=3, resolution=torus1.resolution)

# 你可以使用最多两个图像对曲面进行纹理处理，
# 这两个图像将被解释为朝向灯光的一侧和远离灯光的一侧。
# 这些可以是URL，也可以是指向本地文件的路径
day_texture = "../load_pictures/Whole_world_land_and_oceans.jpg"
night_texture = "../load_pictures/The_earth_at_night.jpg"
surfaces = [
    TexturedSurface(surface, day_texture, night_texture)
    for surface in [sphere, torus1, torus2]
]

for mob in surfaces:
    # mob.shift(IN)
    mob.mesh = SurfaceMesh(mob)
    mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

# 设置视角
frame = scene.camera.frame
frame.set_euler_angles(
    theta=-30 * DEGREES,
    phi=70 * DEGREES,
)

surface = surfaces[0]

scene.play(
    FadeIn(surface),
    ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
)
for mob in surfaces:
    mob.add(mob.mesh)
surface.save_state()
scene.play(Rotate(surface, PI / 2), run_time=2)
for mob in surfaces[1:]:
    mob.rotate(PI / 2)

scene.play(
    Transform(surface, surfaces[1]),
    run_time=3
)

scene.play(
    Transform(surface, surfaces[2]),
    # 在过渡期间移动相机帧
    frame.increment_phi, -10 * DEGREES,
    frame.increment_theta, -20 * DEGREES,
    run_time=3
)
# 添加自动旋转相机帧
frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

# 移动光源
light_text = Text("You can move around the light source")
light_text.move_to(surface_text)
light_text.fix_in_frame()

scene.play(FadeTransform(surface_text, light_text))
light = scene.camera.light_source
scene.add(light)
light.save_state()
scene.play(light.move_to, 3 * IN, run_time=5)
scene.play(light.shift, 10 * OUT, run_time=5)

drag_text = Text("Try moving the mouse while pressing d or s")
drag_text.move_to(light_text)
drag_text.fix_in_frame()

scene.play(FadeTransform(light_text, drag_text))
scene.wait()

scene.hold_on()