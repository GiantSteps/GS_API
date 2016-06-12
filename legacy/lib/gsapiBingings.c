static PyMethodDef gsapi_methods[] = {
  // {"bintomidi", Py_bintomidi, METH_VARARGS, Py_bintomidi_doc},
  // {"miditobin", Py_miditobin, METH_VARARGS, Py_miditobin_doc},
  // {"bintofreq", Py_bintofreq, METH_VARARGS, Py_bintofreq_doc},
  // {"freqtobin", Py_freqtobin, METH_VARARGS, Py_freqtobin_doc},
  // {"alpha_norm", Py_alpha_norm, METH_VARARGS, Py_alpha_norm_doc},
  // {"zero_crossing_rate", Py_zero_crossing_rate, METH_VARARGS, Py_zero_crossing_rate_doc},
  // {"min_removal", Py_min_removal, METH_VARARGS, Py_min_removal_doc},
  // {"level_lin", Py_aubio_level_lin, METH_VARARGS, Py_aubio_level_lin_doc},
  // {"db_spl", Py_aubio_db_spl, METH_VARARGS, Py_aubio_db_spl_doc},
  // {"silence_detection", Py_aubio_silence_detection, METH_VARARGS, Py_aubio_silence_detection_doc},
  // {"level_detection", Py_aubio_level_detection, METH_VARARGS, Py_aubio_level_detection_doc},
  // {"window", Py_aubio_window, METH_VARARGS, Py_aubio_window_doc},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3
// Python3 module definition
static struct PyModuleDef moduledef = {
   PyModuleDef_HEAD_INIT,
   "_gsapi",          /* m_name */
   NULL,//aubio_module_doc,  /* m_doc */
   -1,                /* m_size */
   gsapi_methods,     /* m_methods */
   NULL,              /* m_reload */
   NULL,              /* m_traverse */
   NULL,              /* m_clear */
   NULL,              /* m_free */
};
#endif


static PyObject *
initgsapi (void)
{
  PyObject *m = NULL;
  int err;


  if (   (PyType_Ready (&Py_gsPatternType) < 0)
      // generated objects
      // || (generated_types_ready() < 0 )
  ) {
    return m;
  }

#if PY_MAJOR_VERSION >= 3
  m = PyModule_Create(&moduledef);
#else
  m = Py_InitModule3 ("_gsapi", gsapi_methods, NULL);
#endif

  if (m == NULL) {
    return m;
  }

  err = _import_array ();
  if (err != 0) {
    fprintf (stderr,
        "Unable to import Numpy array from gsapi module (error %d)\n", err);
  }

  Py_INCREF (&Py_gsPatternType);
  PyModule_AddObject (m, "gspattern", (PyObject *) & Py_gsPatternType);
  // Py_INCREF (&Py_filterType);
  // PyModule_AddObject (m, "digital_filter", (PyObject *) & Py_filterType);
  // Py_INCREF (&Py_filterbankType);
  // PyModule_AddObject (m, "filterbank", (PyObject *) & Py_filterbankType);
  // Py_INCREF (&Py_fftType);
  // PyModule_AddObject (m, "fft", (PyObject *) & Py_fftType);
  // Py_INCREF (&Py_pvocType);
  // PyModule_AddObject (m, "pvoc", (PyObject *) & Py_pvocType);
  // Py_INCREF (&Py_sourceType);
  // PyModule_AddObject (m, "source", (PyObject *) & Py_sourceType);
  // Py_INCREF (&Py_sinkType);
  // PyModule_AddObject (m, "sink", (PyObject *) & Py_sinkType);

  // PyModule_AddStringConstant(m, "float_type", AUBIO_NPY_SMPL_STR);

  // // add generated objects
  // add_generated_objects(m);

  // // add ufunc
  // add_ufuncs(m);

  return m;
}

#if PY_MAJOR_VERSION >= 3
    // Python3 init
    PyMODINIT_FUNC PyInit__gsapi(void)
    {
        return initgsapi();
    }
#else
    // Python 2 init
    PyMODINIT_FUNC init_gsapi(void)
    {
        initgsapi();
    }
#endif