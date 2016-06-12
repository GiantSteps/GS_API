# location of the Python header files
 
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/local/Frameworks/Python.framework/Headers
 
# location of the Boost Python include files and library
BOOST_ROOT=/usr/local/Cellar/boost/1.60.0_2/
BOOST_INC=$(BOOST_ROOT)include
BOOST_LIB=$(BOOST_ROOT)/lib


 
# compile mesh classes
TARGET = PyGSPattern
 

all: PyGSPattern

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic $(TARGET).o -L$(BOOST_LIB) -lboost_python-$(PYTHON_VERSION) -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so
 
$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp