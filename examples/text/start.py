from examples.example_imports import *
import manimpango

print(manimpango.list_fonts())

scene = EagerModeScene()

texts = [
    Text("云腾致雨，露结为霜。", font="DFKai-SB").move_to(LEFT*2 + UP*3),
    Text("云腾致雨，露结为霜。", font="KaiTi").move_to(LEFT*2 + UP*2),
    Text("云腾致雨，露结为霜。", font="HGXC_CNKI", weight=NORMAL).move_to(LEFT*2 +UP),
    Text("云腾致雨，露结为霜。", font="YouYuan").move_to(LEFT*2),

    Text("Hello World", font="Freestyle Script").move_to(RIGHT*3),
    Text("hello manim", font="Ink Draft").move_to(UP+ RIGHT*3),
    Text("hello manim", font="Ink Free").move_to(UP*2+RIGHT*3),
    Text("hello manim", font="Segoe Script").move_to(UP*3+RIGHT*4).scale(0.8),

    Text("hello manim").move_to(DOWN),
]
for t in texts:
    scene.play(Write(t), run_time=0.5)

scene.hold_on()