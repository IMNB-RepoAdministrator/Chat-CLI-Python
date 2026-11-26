import threading

from ._exception import Terminated
from .async_raises import async_raises


class infinite_execute_thread(threading.Thread):
    """
    Executing function in another thread with extra functionality:
    
    - Terminate thread.
    - Stop function execute.
    
    This will execute function infinitely until `stop()` is called.
    """
    
    def __init__(self, func, *a, **ka):
        
        if not callable(func):
            raise TypeError("Function doesn't have `__call__` attribute.")
        
        super().__init__(daemon=True)
        
        self.__is_shutdown = threading.Event()
        self.__is_running = False
        self.__func  = func
        self.__args  = a
        self.__kargs = ka

    #Private method
    
    def _get_tid(self):
        """
        **PRIVATE METHOD**
        
        Get thread's id from `threading._active` dict.
        """
        
        if not self.is_alive():
            raise SystemError("Thread is not alive.")
        
        if hasattr(self, "_thread_id"):
            return self._thread_id #type: ignore
        
        else:
            for tid, tobj in threading._active.items(): #type: ignore
                if tobj == self:
                    self._thread_id = tid
                    return tid
                
        raise SystemError("Could not determine thread's id.")

    def run(self):
        """
        **PRIVATE METHOD**

        **Use the `start()` method instead.**
        
        Overloaded `run()` from threading.Thread.
        """
        
        self.__is_running = True
        
        try:
            while not self.__is_shutdown.is_set():
                self.__func(*self.__args, **self.__kargs,)
        except Terminated:
            pass
        
        self.__is_running = False

    # Public method
                    
    def terminate(self):        
        """
        Force terminate thread.
        
        <b>NOTE 1</b>: This will forcefully terminate thread so no return `join()`.
        
        <b>NOTE 2</b>: Using `join()` will still wait for the function until it joinable.
        """
        
        async_raises(self._get_tid(), Terminated)
        self.__is_running = False

    def is_running(self):
        """
        Return boolean value if the thread is still running:
        
        - 1: is running
        - 0: is not running
        """
        
        return self.__is_running

    def stop(self):
        """
        Stop the program in thread. This does not force the program to stop immediately.
        To stop immediately, use `terminate()`.
        
        **NOTE**: Use this instead of `is_alive()` for better reliability especially `terminate()` due to `is_alive()`
        still return `True` after `terminate()`.
        """
        
        self.__is_shutdown.set()