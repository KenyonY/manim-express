from sparrow.version_ops import VersionControl
from tools import update_requirements

pkgname = "manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
vc.update_version(1)
# To keep manimlib latest.
update_requirements()
vc.update_readme(readme_path="./README.md", license="MIT")
vc.update_readme(readme_path="./README_zh.md", license="MIT")
# os.system("yapf -i -r ./manim_express")
vc.upload_pypi(pkgname)
