from manimlib.utils.tex_file_writing import tex_hash
from manimlib.utils.directories import get_tex_dir
import requests
import urllib
import os
import re


def tex_to_svg_file_online(tex_file_content):
    """ Using the online latex compiler: https://www.quicklatex.com/latex3.f
    """
    svg_file_path = os.path.join(
        get_tex_dir(), tex_hash(tex_file_content) + ".svg"
    )
    tex_file = svg_file_path.replace(".svg", ".tex")

    if os.path.exists(tex_file):
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

        params = {
            "formula": expression,
            "preamble": preamble,
            "out": 2,  # 2 For SVG output
        }
        payload = urllib.parse.urlencode(
            params, quote_via=urllib.parse.quote
        )
        # print("payload:", payload)
        response = requests.post("https://www.quicklatex.com/latex3.f", data=payload)

        if not response.text.startswith("0"):
            error = "\n".join(
                response.text.split("\r\n")[2:]
            )
            raise ResourceWarning(error)
        else:
            svgurl = response.text.split("\n")[-1].split(" ")[0].replace("png", "svg")
            svgtext = requests.get(svgurl, headers={"Accept-Encoding": "identity"}).text

        with open(svg_file_path, "w") as svgfile:
            svgfile.write(svgtext)

    return svg_file_path
