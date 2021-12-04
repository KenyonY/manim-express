from examples.example_imports import *

scene = EagerModeScene(screen_size=Size.bigger)

day_texture = "../load_pictures/Whole_world_land_and_oceans.jpg"
night_texture = "../load_pictures/The_earth_at_night.jpg"
r, h = 7, 5
surface = CustomSurface()
circle_surface = surface.circle(2).move_to(LEFT*2)
square_surface = surface.square(12, 7)
square_surface.move_to(ORIGIN)

sphere_surface = Sphere(radius=3)


surfaces = [
    TexturedSurface(surface, day_texture,
                    night_texture  # optional
                    )
    for surface in [sphere_surface, square_surface, circle_surface]
]

for mob in surfaces:
    mob.shift(IN)
    mob.mesh = SurfaceMesh(mob)
    mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

scene.play(
    FadeIn(surfaces[0]),
    # ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
)

torus1 = Torus(r1=3, r2=1)
torus2 = surface.torus(3, 1).move_to(RIGHT*3)


# scene.play(FadeIn(torus1))
# scene.play(FadeIn(torus2))
vec1 = np.array([1, 2, 0]).reshape(1, -1)
vec2 = np.array([3, 4, 0]).reshape(1, -1)
# v3 = np.kron(vec1, vec2)
# v3 = np.outer(vec1, vec2)
v3 = np.cross(vec1, vec2)
unit = 1
# for i in range(2):
#     for j in range(2):
#         if j>i:
#
#         print(v3[i][j])
print(v3)

scene.hold_on()