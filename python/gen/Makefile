

CC -fPIC  -c -o my-module.o my-module.c
gcc -shared  -o libmymodule.so my-module.o
PYTHONPATH=$PYTHONPATH:../../ python my-module.py > my-module-binding.cpp
# gcc -fPIC -I../../src/3rdParty/json -I/usr/local/Frameworks/Python.framework/Headers -c -o my-module-binding.o my-module-binding.c -std=c++11
# gcc -shared  -o MyModule.so -L. -lmymodule my-module-binding.o -lpython