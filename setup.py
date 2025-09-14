from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob, sys

source_files = ["enet.pyx"] + glob.glob("enet/*.c")

if len(source_files) == 1:
    sys.exit(
        "ENet source files not found.\n"
        "Download: https://github.com/GTPSHAX/how-to-fix-growtopia-5.15\n"
        "Credit: GTPSHAX, ikazu and others."
    )

define_macros = [
    ('HAS_POLL', None),
    ('HAS_FCNTL', None),
    ('HAS_MSGHDR_FLAGS', None),
    ('HAS_SOCKLEN_T', None)
]
libraries = []

if sys.platform == "win32":
    define_macros.append(('WIN32', None))
    libraries += ['ws2_32', 'Winmm']
elif sys.platform != "darwin":
    define_macros += [
        ('HAS_GETHOSTBYNAME_R', None),
        ('HAS_GETHOSTBYADDR_R', None)
    ]

ext_modules = [
    Extension(
        "enet",
        sources=source_files,
        include_dirs=["enet/include/"],
        define_macros=define_macros,
        libraries=libraries,
        extra_compile_args=["-O3"],
    )
]

setup(
    name="enet",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
)