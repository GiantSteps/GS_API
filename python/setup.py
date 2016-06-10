
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob

pySource = "gsPackage/"

modules = [f for f in glob.glob(pySource+"*py")]

print modules


setup(name='gsapi',
      version=1.0,
      description='Python symbolic music manipulation tools',
      long_description="",
      author='MTG / GiantSteps',
      author_email='',
      url='https://github.com/Giantsteps',
      license='BSD, CC BY-NC-SA',
      packages=find_packages(exclude=['tests', 'docs']),
      # ext_modules=extensions,
      # package_data={'gsapi': package_data},
      exclude_package_data={'': ['tests', 'docs']},
      # scripts=scripts,
      cmdclass={'build_ext': build_ext},
      test_suite='nose.collector',
      # classifiers=classifiers
      )



