from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from setuptools import setup, find_packages
from distutils.extension import Extension


# legacy imports
# from Cython.Distutils import build_ext
# import distutils.ccompiler
# import utils.parallelComp
# distutils.ccompiler.CCompiler.compile = utils.parallelComp.parallelCCompile

def checkLazySetupCommands():
      # utility when compiling from IDE, last uncommented executes desired action
    toAppend = ['clean', '--all']
    toAppend = ['build']

    # remainder for pip maintainers
    # (once .pypirc edited)
    # bump the GSAPIFullVersion in GSAPIFullVersion.py then : python setup.py sdist bdist_wheel upload

    if len(sys.argv) == 1:
        for s in toAppend:
            sys.argv.append(s)
    print (sys.argv)


if __name__ == '__main__':
    import sys
    from gsapi import *
    print ("gsapi v%s"%getGSAPIFullVersion())
    checkLazySetupCommands()


# for now python-midi is not officially on pip3 so we need to install it manually and it's name become midi...
midiRequiredName = 'midi' if sys.version_info >= (3,0) else 'python-midi' 

setup(name='gsapi',
      version=getGSAPIFullVersion(),
      description='Python Symbolic Music Manipulation Tools',
      long_description="",
      author='Martin Hermant, Angel Faraldo, Pere Calopa',
      author_email='angel.faraldo@upf.edu',
      url='https://github.com/Giantsteps/gsapi',
      license='',
      packages=find_packages(exclude=['utils', 'gen', 'test', 'docs']),
      # ext_modules=[gsapiModule],
      # package_data={'gsapi': package_data},
      # exclude_package_data={'': ['tests', 'docs']},
      # scripts=scripts,
      # cmdclass={'build_ext': build_ext},
      test_suite='nose.collector',
      install_requires=[midiRequiredName],
      # dependency_links = ['https://github.com/vishnubob/python-midi.git@feature/python3#egg="midi"'],
      zip_safe=True
      # classifiers=classifiers
      )
