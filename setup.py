from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob
import sys

source_files = ["enet.pyx"]

_enet_files = glob.glob("enet/*.c")

if not _enet_files:
    print("latest enet source developed for growtopia")
    print("download it from: https://github.com/GTPSHAX/how-to-fix-growtopia-5.15")
    print("credit: GTPSHAX, ikazu, and other contributors")
    sys.exit(1)

source_files.extend(_enet_files)

define_macros = [('HAS_POLL', None),
                 ('HAS_FCNTL', None),
                 ('HAS_MSGHDR_FLAGS', None),
                 ('HAS_SOCKLEN_T', None) ]

libraries = []

if sys.platform == 'win32':
    define_macros.extend([('WIN32', None)])
    libraries.extend(['ws2_32', 'Winmm'])

if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None), ('HAS_GETHOSTBYADDR_R', None)])

ext_modules = [
    Extension(
        "enet",
        extra_compile_args=["-O3"],
        sources=source_files,
        include_dirs=["enet/include/"],
        define_macros=define_macros,
        libraries=libraries)]

setup(
  name = 'enet',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
