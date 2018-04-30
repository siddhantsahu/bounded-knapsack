from distutils.core import setup
from Cython.Build import cythonize

setup(name="bkp_cython",
      ext_modules=cythonize("bkp_cython.pyx"))