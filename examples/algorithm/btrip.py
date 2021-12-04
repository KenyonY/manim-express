from examples.example_imports import *
from manimlib import there_and_back
import textdistance
from sparrow.log import Logger

room_name_list1 = ["标间", "豪华大床房", "豪华圆床房", "3人间"]
room_name_list2 = ["标准间", "豪华圆床房", "豪华大床房", "三人房"]
room_name_list3 = ["标准间", "豪华大床房", "三人房"]

texts1 = VGroup()
texts2 = VGroup()
texts3 = VGroup()
[texts1.add(Text(i, font='KaiTi').move_to(RIGHT * (3 * idx - 5) + UP * 3)) for idx, i in enumerate(room_name_list1)]
[texts2.add(Text(i, font='KaiTi').move_to(RIGHT * (3 * idx - 5))) for idx, i in enumerate(room_name_list2)]
[texts3.add(Text(i, font='KaiTi').move_to(RIGHT * (3 * idx - 5) + DOWN * 3)) for idx, i in enumerate(room_name_list3)]

all_texts = VGroup(texts1, texts2, texts3)


def similarity(s1, s2):
    return textdistance.levenshtein.normalized_similarity(s1, s2)


def check_if_the_same_set(name1, name2):
    score = similarity(name1, name2)
    if 1 - score < 0.1:
        return {name1, name2}
    else:
        return set()


def check_if_in_set_list(name, lst):
    if lst:
        for i_set in list(lst):
            if name in i_set:
                return True
    return False


class Clips(EagerModeScene):
    def __init__(self):
        super().__init__(screen_size=Size.bigger)

    def clip1(self):
        self.add(all_texts.scale(0.7))
        self.one_layer_match(texts1, texts2)

    def clip2(self):
        self.one_layer_match(texts2, texts3)

    def show_set_right(self, set_list):
        set_mobj = VGroup()
        for set_item in set_list:
            for text_item in set_item:
                set_mobj.add(Text(text_item, font='KaiTi').set_color(GREEN))
        set_mobj.arrange(DOWN, buff=0.5).scale(0.5).to_edge(RIGHT + UP)
        self.add(set_mobj)

    def one_layer_match(self, layer1, layer2):
        res_list = []
        for item1 in layer1.submobjects:
            item1: Text
            for item2 in layer2.submobjects:
                item2: Text
                if not check_if_in_set_list(item2.text, res_list):
                    arrow = Arrow(item1.get_center(), item2.get_center(), buff=.25, ).set_color(YELLOW)
                    self.play(GrowArrow(arrow),
                              run_time=0.2)
                    temp_set = check_if_the_same_set(item1.text, item2.text)
                    if temp_set:
                        res_list.append(temp_set)
                        self.play(*[Indicate(i) for i in (item1, item2)], run_time=0.3, rate_func=there_and_back)
                        break
                    else:
                        self.play(FadeOut(arrow), run_time=0.3)
        self.show_set_right(res_list)


clips = Clips()
# clips.render()

clips.clip1()
clips.hold_on()
