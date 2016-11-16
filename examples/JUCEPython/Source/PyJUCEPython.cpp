/*
  ==============================================================================

    PyJUCEPython.cpp
    Created: 19 Jul 2016 12:15:54pm
    Author:  Martin Hermant

  ==============================================================================
*/

#include "PyJUCEPython.h"

#include "PyJUCEAPI.h"
#include "structmember.h"

///////////////////////////////////////


static PyObject *SpamError;

#define GETOWNER() dynamic_cast<PyJUCEAPI*>((PyJUCEAPI*)PyCapsule_Import("JUCEAPI.vstOwner",0))
//#define GETOWNER() ((PyJUCEAPIRef*)PyDict_GetItem(self->tp_dict, PyString_FromString("owner")))->owner
typedef struct {
  PyObject_HEAD
  /* Type-specific fields go here. */
} PyJUCEAPIObject;


typedef struct PyJUCEAPIRef:PyObject{
  PyJUCEAPIRef(PyJUCEAPI * o){ owner = o;}
  PyJUCEAPI * owner;
}PyJUCEAPIRef;

typedef struct PyJUCEAPIRef_Type:PyTypeObject{
  PyJUCEAPIRef_Type(){
    memset(this, 0, sizeof(*this));
    tp_name="JUCEAPI.vst.ptr";           /*tp_name*/
    ob_refcnt = 1;
    tp_basicsize=sizeof(PyJUCEAPIRef);            /*tp_basicsize*/

    tp_flags=Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE; /*tp_flags*/
    tp_doc="PyJUCEAPIObject pointer objects";           /* tp_doc */
    tp_methods=0;             /* tp_methods */
    tp_members= 0;           /* tp_members */
    tp_init=  0;     /* tp_init */
    tp_new= 0;                 /* tp_new */

  }

}PyJUCEAPIRefType;



static PyObject * PyJUCEAPI_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  PyJUCEAPIObject * self = (PyJUCEAPIObject *)type->tp_alloc(type, 0);
  if (self != NULL) {}
  return (PyObject *)self;
}
static int PyJUCEAPI_init(PyJUCEAPIObject *self, PyObject *args, PyObject *kwds){return 0;}
static void PyJUCEAPI_dealloc(PyJUCEAPIObject* self){}



static PyObject * updateParam(PyTypeObject *self, PyObject *args)
{
  PyObject * param = nullptr;

  if(!PyArg_ParseTuple(args, "O",&param))
    return NULL;
  bool updated = GETOWNER()->setParam(param);
  if(updated)Py_RETURN_TRUE;
  else Py_RETURN_FALSE;

}

static PyMemberDef PyJUCEAPIObject_Members[] = {
//  {"parameters",T_OBJECT,0,0,NULL},
  {NULL}  /* Sentinel */
};
static PyMethodDef PyJUCEAPIObject_Methods[] = {
  {"updateParam", (PyCFunction)updateParam, METH_CLASS | METH_VARARGS,"update parameter value"},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};


struct PyJUCEAPIType: PyTypeObject  {
  PyJUCEAPIType(PyJUCEAPI * owner){

    memset(this, 0, sizeof(*this));
    tp_name="vst";           /*tp_name*/
    ob_refcnt = 1;
    ob_type = &PyType_Type;
    tp_basicsize=sizeof(PyJUCEAPIObject);            /*tp_basicsize*/
    tp_alloc = PyType_GenericAlloc;
    tp_new =PyType_GenericNew;
    tp_dealloc=(destructor)PyJUCEAPI_dealloc; /*tp_dealloc*/
    tp_flags=Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE; /*tp_flags*/
    tp_doc="PyJUCEAPIObject objects";           /* tp_doc */
    tp_dict = PyDict_New();
    PyObject* key = PyString_FromString("owner");
    static PyJUCEAPIRef_Type * t= new PyJUCEAPIRef_Type();
    PyJUCEAPIRef* value = PyObject_New(PyJUCEAPIRef,t);
    value->owner = owner;
    PyDict_SetItem(tp_dict, key, value);
    Py_DECREF(key);
    Py_DECREF(value);
    tp_methods=PyJUCEAPIObject_Methods;             /* tp_methods */
    tp_members= PyJUCEAPIObject_Members;           /* tp_members */
    tp_init=  (initproc)PyJUCEAPI_init;     /* tp_init */
    tp_new= PyJUCEAPI_new;                 /* tp_new */
  }

  void* operator new(size_t n) { return PyMem_Malloc(n); }
  void operator delete(void* p) { PyMem_Free(p); }
};






PyMODINIT_FUNC
initJUCEAPI(PyJUCEAPI * owner,PyObject ** m)
{

  *m= Py_InitModule("JUCEAPI", 0);
  Py_IncRef(*m);
  if (m == NULL)
    return;

  static PyJUCEAPIType * typ = new PyJUCEAPIType(owner);
  if (PyType_Ready(typ) < 0)
    return;

  PyModule_AddObject(*m, "vst", (PyObject *)typ);
  PyObject *obj = PyObject_CallObject((PyObject *) typ, NULL);

  PyModule_AddObject(*m, "API", (PyObject *)obj);
  
  PyObject * ownerCapsule =  PyCapsule_New(owner, "JUCEAPI.vstOwner", NULL);
  PyModule_AddObject(*m, "vstOwner", ownerCapsule);


  SpamError = PyErr_NewException("PyJuceAPI.error", NULL, NULL);
  Py_INCREF(SpamError);
  PyModule_AddObject(*m, "error", SpamError);
}




//////////////////////////////////////////////////////////
