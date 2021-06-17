from manimlib.utils.tex_file_writing import tex_hash
from manimlib.utils.directories import get_tex_dir
import requests
import urllib
from fake_headers import Headers
import os
import re
# from helium import *
# import pyperclip


def tex_to_svg_file_online(tex_file_content):
    """ Using the online latex compiler: https://www.quicklatex.com/latex3.f
    https://latexonline.cc/
    """
    svg_file_path = os.path.join(
        get_tex_dir(), tex_hash(tex_file_content) + ".svg"
    )
    tex_file = svg_file_path.replace(".svg", ".tex")

    if os.path.exists(svg_file_path):
        pass
    else:
        idx = re.search("begin{document}", tex_file_content, flags=0).span()[0] - 2
        preamble, expression = tex_file_content[:idx], tex_file_content[idx:]

        expression = expression.\
            replace("\\begin{document}", '').\
            replace("\\end{document}", '').\
            strip('\n')

        with open(tex_file, "w", encoding="utf-8") as outfile:
            outfile.write(tex_file_content)

        def quick_latex():
            params = {
                "formula": expression,
                "preamble": preamble,
                "out": 2,  # 2 For SVG output
            }
            payload = urllib.parse.urlencode(
                params, quote_via=urllib.parse.quote
            )
            response = requests.post("https://www.quicklatex.com/latex3.f", data=payload)

            if not response.text.startswith("0"):
                error = "\n".join(
                    response.text.split("\r\n")[2:]
                )
                raise ResourceWarning(error)
            else:
                svgurl = response.text.split("\n")[-1].split(" ")[0].replace("png", "svg")
                headers = Headers(os="mac", headers=True).generate()
                content = requests.get(svgurl, headers=headers).text
                return content

        # def chrome_helium():
        #     url = "https://viereck.ch/latex-to-svg/"
        #     driver = start_chrome(url, headless=False)
        #     e1 = driver.find_element_by_tag_name("textarea")
        #     write(expression, into=e1)
        #     #     driver.find_element_by_id("environment") # to choice align? It doesn't seem necessary..
        #     e2 = driver.find_element_by_id("svgSourceCodeButton")
        #     e2.click()
        #     e3 = driver.find_element_by_id("svgSourceCode")
        #     e3.send_keys(Keys.CONTROL, 'a')
        #     e3.send_keys(Keys.CONTROL, 'c')
        #     content = pyperclip.paste()
        #     return content

        # svg_content = chrome_helium()
        svg_content = quick_latex()
        with open(svg_file_path, "w", encoding="utf-8") as fo:
            fo.write(svg_content)

    # Remove tex files (not svg files)
    tex_dir, name = os.path.split(svg_file_path)
    stem, end = name.split(".")
    for file in filter(lambda s: s.startswith(stem), os.listdir(tex_dir)):
        if not file.endswith(end):
            os.remove(os.path.join(tex_dir, file))

    return svg_file_path
