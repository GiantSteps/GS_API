
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob

libFolder = "src/"
bindingsFolder = "pythonWrap/generated/"
libSources = [f for f in glob.glob(libFolder+"*.cpp")]
bindingSources = [f for f in glob.glob(bindingsFolder+"*.cpp")]
cppSources = libSources+bindingSources


from pythonWrap.gen import genBindings
genBindings.generate(bindingsFolder)


import distutils.ccompiler
import pythonWrap.Utils.parallelComp
distutils.ccompiler.CCompiler.compile=pythonWrap.Utils.parallelComp.parallelCCompile

if __name__ == '__main__':
      import sys
      toAppend = ['clean','--all']
      # toAppend = ['remove']
      toAppend = ['build']
      # toAppend  = ['install']
      if len(sys.argv)==1:
            for s in toAppend:
                  sys.argv.append(s)
      print sys.argv






gsapiModule = Extension('gsapi',
                    # define_macros = [('MAJOR_VERSION', '1'),
                    #                  ('MINOR_VERSION', '0')],
                    include_dirs = [libFolder,libFolder+"3rdParty/json/"],
                    libraries = [],
                    extra_compile_args=['-std=c++11','-w'],
                    library_dirs = ['/usr/local/lib'],
                    
                    sources = cppSources)

setup(name='gsapi',
      version=1.0,
      description='Python symbolic music manipulation tools',
      long_description="",
      author='MTG / GiantSteps',
      author_email='',
      url='https://github.com/Giantsteps',
      license='',
      packages=find_packages(exclude=['tests', 'docs']),
      ext_modules=[gsapiModule],
      # package_data={'gsapi': package_data},
      exclude_package_data={'': ['tests', 'docs']},
      # scripts=scripts,
      cmdclass={'build_ext': build_ext},
      test_suite='nose.collector',
      # classifiers=classifiers
      )

