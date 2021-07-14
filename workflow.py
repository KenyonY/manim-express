import os
from sparrow.file_ops import rm
from sparrow.version_ops import VersionControl
from tools import update_requirements

pkgname="manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
vc.update_version(1)
# To keep manimlib latest.
update_requirements()
vc.update_readme(license="MIT")
# os.system("yapf -i -r ./manim_express")
vc.upload_pypi(pkgname)
