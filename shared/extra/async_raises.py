import ctypes  # C api spooky
import inspect


def async_raises(tid, exctype): # Calling C api spooky
    """
    Raises exception for specific thread. Using for interrupting thread abruptly.``
    """

    if not inspect.isclass(exctype):
        raise TypeError("exctype is not a type.")
    
    value = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))

    if value == 0:
        raise ValueError("Invalid thread's id.")
    
    elif value != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("Async raises failed. (PyThreadState_SetAsyncExc failed.)")
