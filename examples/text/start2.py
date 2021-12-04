from examples.example_imports import *


def setup(self):
    self.textbox = Textbox()
    self.checkbox = Checkbox()
    self.color_picker = ColorSliders()
    self.panel = ControlPanel(
        Text("Text", size=0.5), self.textbox, Line(),
        Text("Show/Hide Text", size=0.5), self.checkbox, Line(),
        Text("Color of Text", size=0.5), self.color_picker
    )
    self.add(self.panel)


scene = EagerModeScene()
setup(scene)
text = Text("text")

def text_updater(old_text):
    assert (isinstance(old_text, Text))
    new_text = Text(scene.textbox.get_value(), size=old_text.size)
    # new_text.align_data_and_family(old_text)
    new_text.move_to(old_text)
    if scene.checkbox.get_value():
        new_text.set_fill(
            color=scene.color_picker.get_picked_color(),
            opacity=scene.color_picker.get_picked_opacity()
        )
    else:
        new_text.set_opacity(0)
    old_text.become(new_text)

# text.add_updater(text_updater)
scene.add(MotionMobject(text))
scene.add(MotionMobject(Square3D()))
scene.textbox.set_value("Manim")


scene.hold_on()
