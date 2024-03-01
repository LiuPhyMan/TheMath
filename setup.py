# -*- coding: utf-8 -*-

# from setuptools import setup, find_packages
# from

# setup(
#     name = "mymath",
#     packages = find_packages(),
#     version = "0.1.0",
#     install_requires=[
#         "numpy",
#         "scipy"
#     ]
# )
from distutils.core import setup

from Cython.Build import cythonize
import numpy

ext = cythonize("mymath/*.pyx",
                include_path=[numpy.get_include()],
                compiler_directives={'language_level': '3'})
for i in range(len(ext)):
  ext[i].extra_compile_args.append("-Xpreprocessor")
  ext[i].extra_compile_args.append("-fopenmp")
setup(ext_modules=ext)
