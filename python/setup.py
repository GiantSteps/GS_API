from setuptools import setup, find_packages
from distutils.extension import Extension
# from Cython.Distutils import build_ext

import glob

# libFolder = "src/"
# bindingsFolder = "generated/"
# libSources = [f for f in glob.glob(libFolder+"*.cpp")]
# bindingSources = [f for f in glob.glob(bindingsFolder+"*.cpp")]
# cppSources = libSources+bindingSources


# from gen import genBindings
# genBindings.generate(bindingsFolder)

import distutils.ccompiler
import utils.parallelComp

distutils.ccompiler.CCompiler.compile = utils.parallelComp.parallelCCompile

if __name__ == '__main__':
    import sys
    import gsapi  # TODo moved gsapi from line 44 to line 24

    toAppend = ['clean', '--all']
    toAppend = ['build']
    toAppend = ['install']
    # toAppend  = ['sdist', 'bdist_wheel', 'install']
    if len(sys.argv) == 1:
        for s in toAppend:
            sys.argv.append(s)
    print sys.argv

# gsapiModule = Extension('gsapi',
#                     # define_macros = [('MAJOR_VERSION', '1'),
#                     #                  ('MINOR_VERSION', '0')],
#                     include_dirs = [libFolder, libFolder + "3rdParty/json/"],
#                     libraries = [],
#                     extra_compile_args=['-std=c++11', '-w'],
#                     library_dirs = ['/usr/local/lib'],
#                     sources = cppSources)


setup(name='gsapi',
      version=gsapi.getGSAPIFullVersion(),
      description='Python Symbolic Music Manipulation Tools',
      long_description="",
      author='Martin Hermant, Angel Faraldo, Pere Calopa',
      author_email='angel.faraldo@upf.edu',
      url='https://github.com/Giantsteps/gsapi',
      license='',
      packages=find_packages(exclude=['utils', 'gen', 'test', 'docs']),
      # ext_modules=[gsapiModule],
      # package_data={'gsapi': package_data},
      exclude_package_data={'': ['tests', 'docs']},
      # scripts=scripts,
      # cmdclass={'build_ext': build_ext},
      test_suite='nose.collector',
      install_requires=['python-midi', 'midiutil'],
      zip_safe=True
      # classifiers=classifiers
      )
