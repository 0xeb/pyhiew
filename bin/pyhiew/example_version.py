"""Example: Version info."""
import hiew

v = hiew.VERSION
pv = hiew.PYHIEW_VERSION

lines = [
    f"Hiew: {v['major']}.{v['minor']}",
    f"SDK: {v['sdkmajor']}.{v['sdkminor']}",
    f"PyHiew: {pv['major']}.{pv['minor']}.{pv['build']}",
]

hiew.Window.FromString("Version Info", lines, width=40)
