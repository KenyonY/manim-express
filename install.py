from sparrow.version_ops import VersionControl
from tools import update_setup_cfg

pkgname = "manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
update_setup_cfg()
vc.install()
