from examples.example_imports import *

scene = EagerModeScene()

fixed_point = Sphere(radius=0.08).move_to(ORIGIN).set_color(GREEN_D)
scene.add(fixed_point)

start_rod = Vec3(*UP*3)
end_rod = Vec3(-3, 3, 0)
L = (end_rod - start_rod).norm()
# rod = Line3D(start_rod, end_rod, width=0.08).set_color(RED_D)
fine_line = Line3D(start_rod.to_array(), end_rod.to_array(), width=0.02).set_color(RED_D)
scene.add(fine_line)
massive_bob = Sphere(radius=0.12).move_to(end_rod.to_array()).set_color(GREY_D)
m = 1. #kg
g = 9.8
G = Vec3(0, -g, 0)# m/s^2
scene.add(massive_bob)

f = Vec3(0, 0, 0)
tension = Vec3(0, 0, 0)

f_arrow = Arrow(end_rod.to_array(), f.to_array(), buff=0)
mg_arrow = Arrow(end_rod.to_array(), m*G.to_array(), buff=0)
tension_arrow = Arrow(end_rod.to_array(), tension.to_array(), buff=0)
scene.add(f_arrow, mg_arrow, tension_arrow)

v = Vec3(0, 0, 0)

def update_func(obj, dt):
    global v, end_rod, fine_line, f, tension
    rob_vec = end_rod - start_rod
    theta = rob_vec.angle_between(DOWN)
    tension_scalar = m*g*np.cos(theta) + m * (v.norm()**2)/L
    tension = tension_scalar * (-1*rob_vec.normalise())
    f = tension + m*G
    a = f * (1/m)
    v += a * dt
    end_rod += v*dt


    obj.move_to(end_rod.to_array())

def update_line(obj):
    obj.put_start_and_end_on(start_rod.to_array(), end_rod.to_array())

def update_f_arrow(obj):
    obj.put_start_and_end_on(end_rod.to_array(), (end_rod+f*0.1).to_array())

def update_mg_arrow(obj):
    obj.put_start_and_end_on(end_rod.to_array(), (end_rod+m*G*0.1).to_array())

def update_tension_arrow(obj):
    obj.put_start_and_end_on(end_rod.to_array(), (end_rod+tension*0.1).to_array())


fine_line.add_updater(update_line)
massive_bob.add_updater(update_func)
f_arrow.add_updater(update_f_arrow)
mg_arrow.add_updater(update_mg_arrow)
tension_arrow.add_updater(update_tension_arrow)


scene.wait(50)


scene.hold_on()