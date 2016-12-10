#include <boost/python.hpp>
#include "GSPattern.h"

using namespace boost::python;

BOOST_PYTHON_MODULE(gsPattern)
{
    class_<GSPattern>("gsPattern")
        .def_readwrite("originBPM", &GSPattern::originBPM)
        .def_readwrite("duration", &GSPattern::duration)
        .def_readwrite("timeSigNumerator", &GSPattern::timeSigNumerator)
        .def_readwrite("timeSigDenominator",&GSPattern::timeSigDenominator)

    ;
};
