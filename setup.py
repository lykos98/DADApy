import os

from setuptools import Extension, setup 
from setuptools.command.install import install


class get_numpy_include(object):
    """Defer numpy.get_include() until after numpy is installed.
    From: https://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
    """

    def __str__(self):
        import numpy

        return numpy.get_include()


ext_modules = []

ext_modules += [
    Extension(
        "dadapy._cython.cython_clustering",
        sources=["dadapy/_cython/cython_clustering.c"],
        include_dirs=[get_numpy_include()],
    )
]

ext_modules += [
    Extension(
        "dadapy._cython.cython_clustering_v2",
        sources=["dadapy/_cython/cython_clustering_v2.c"],
        include_dirs=[get_numpy_include()],
    )
]

ext_modules += [
    Extension(
        "dadapy._cython.cython_maximum_likelihood_opt",
        sources=["dadapy/_cython/cython_maximum_likelihood_opt.c"],
        include_dirs=[get_numpy_include()],
    )
]

ext_modules += [
    Extension(
        "dadapy._cython.cython_maximum_likelihood_opt_full",
        sources=["dadapy/_cython/cython_maximum_likelihood_opt_full.c"],
        include_dirs=[get_numpy_include()],
    )
]


ext_modules += [
    Extension(
        "dadapy._cython.cython_density",
        sources=["dadapy/_cython/cython_density.c"],
        include_dirs=[get_numpy_include()],
    )
]

ext_modules += [
    Extension(
        "dadapy._cython.cython_overlap",
        sources=["dadapy/_cython/cython_overlap.c"],
        include_dirs=[get_numpy_include()],
    )
]


ext_parallel = Extension(
    "dadapy._cython.cython_distances",
    sources=["dadapy/_cython/cython_distances.c"],
    include_dirs=[get_numpy_include()],
)


extra_compile_args = (["-fopenmp"],)
extra_link_args = (["-fopenmp"],)

# Check if the '-fopenmp' flag is supported
command = 'gcc -fopenmp -E - < /dev/null > /dev/null 2>&1 && echo "OpenMP supported" || echo "OpenMP not supported"'

if os.system(command) == "OpenMP supported":
    # If '-fopenmp' is supported, add the extra compile and link arguments
    # Installing cython_distances using OpenMP
    ext_parallel.extra_compile_args.append("-fopenmp")
    ext_parallel.extra_link_args.append("-fopenmp")

# If OpenMP is not available, the C extension to compute distances in discrete spaces will not run in parallel.

ext_modules += [ext_parallel]

#compile dadac


EXT_DIR = os.path.join(os.path.dirname(__file__), 'dadapy/dadac')
class RunMake(install):
    """Makefile on setuptools install."""
    def run(self):
        old_dir = os.getcwd()
        try:
            os.chdir(EXT_DIR)
            print("Building C library ...")
            os.system("make lib")
            #self.spawn(['make'])
        finally:
            os.chdir(old_dir)
        install.run(self)

setup(
    packages=["dadapy", "dadapy._utils","dadapy.dadac"],
    cmdclass=
    {
        'install': RunMake
        },
    ext_modules=ext_modules,
    include_package_data=True,
    package_data={"dadapy":["dadac/bin/*.so","_utils/discrete_volumes/*.dat"],
                  },


)
