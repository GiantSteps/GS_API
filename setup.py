
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

import glob

libFolder = "src/"
bindingsFolder = "python/lib/"
libSources = [f for f in glob.glob(libFolder+"*.cpp")]
bindingSources = ["sandBox/pybindGen/my-module-binding.cpp"]#[f for f in glob.glob(bindingsFolder+"*.cpp")]
cppSources = libSources+bindingSources
print cppSources


def parallelCCompile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
    # those lines are copied from distutils.ccompiler.CCompiler directly
    macros, objects, extra_postargs, pp_opts, build = self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
    # parallel code
    N=4 # number of parallel compilations
    import multiprocessing.pool
    def _single_compile(obj):
        try: src, ext = build[obj]
        except KeyError: return

        print extra_postargs
        self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
    # convert to list, imap is evaluated on-demand
    list(multiprocessing.pool.ThreadPool(N).imap(_single_compile,objects))
    return objects
import distutils.ccompiler
distutils.ccompiler.CCompiler.compile=parallelCCompile

if __name__ == '__main__':
      import sys
      toAppend = ['clean','--all']
      # toAppend = ['remove']
      toAppend = ['build']
      toAppend  = ['install']
      if len(sys.argv)==1:
            for s in toAppend:
                  sys.argv.append(s)
      print sys.argv



boost_include_dirs = "/usr/local/Cellar/boost/1.60.0_2/include"


gsapiModule = Extension('gsapi',
                    # define_macros = [('MAJOR_VERSION', '1'),
                    #                  ('MINOR_VERSION', '0')],
                    include_dirs = [libFolder,libFolder+"3rdParty/json/",boost_include_dirs],
                    libraries = ["boost_python"],
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

