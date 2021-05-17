from manim_imports_ext import *

LOGO_LIST = [
    'LOGO/use_ppt_create_svg/yao1.svg',
    'LOGO/USST_logo.svg',
    'LOGO/couple.svg',
    'LOGO/demo2.svg',
    'https://svgshare.com/i/7c5.svg',
    'https://upload.wikimedia.org/wikipedia/zh/2/2b/USST_logo.svg',
]
class Medal(Scene):

    def construct(self):

        mob = SVGMobject(
            LOGO_LIST[0],
            color=RED,
            # stroke_width=0
        )

        # mob1 = ImageMobject(
        #     'logo1.jpg',
        # )
        self.play(ShowCreation(mob))
        # self.play(ShowCreation(mob1.scale(1.2).move_to([2, 0, 0]), run_time=2))
        self.wait(1)
