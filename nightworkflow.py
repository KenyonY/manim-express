from sparrow.version_ops import VersionControl
pkgname = "manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
# os.system("yapf -i -r ./manim_express")
vc.install(pkgname)
