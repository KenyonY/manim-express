from examples.example_imports import *

scene = EagerModeScene()

dot = Dot(LEFT*3 + DOWN*2)
text = Text("This is some text.").next_to(dot, RIGHT)
# 让text动态跟随dot旁边
text.add_updater(lambda x: x.next_to(dot, RIGHT))

envelope = VGroup()
# 保留轨迹
# envelope.add_updater(lambda x: x.add(text.copy().clear_updaters().set_opacity(0.2)))

scene.add(dot, text, envelope)
scene.play(dot.shift, UP*4, rate_func=there_and_back, run_time=2)


# def anim(obj):
#     obj.next_to(dot, RIGHT)
# text.add_updater(anim)

# scene.play(dot.shift, UP*4, run_time=2)
# 使用remove_updater 移除确定的动态函数更新
# text.remove_updater(anim)
# 使用clear_updaters移除对象身上所有动态更新
# text.clear_updaters()

# scene.play(dot.shift, UP*4, rate_func=there_and_back, run_time=2)
