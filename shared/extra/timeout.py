import queue
import threading
from functools import wraps

from shared.extra.Run_only_Thread import Run_only_Thread


def timeout(time : float, action=None, *action_args, **action_kwargs):
    """
    Set timneout for functions.
    
    - <b>time</b> (float) : set time for timeout (in senconds)
    - <b>action</b> : action to run after time out (default is return None)

    <b>NOTE</b>: ONLY USE FOR SYNCHRONOUS FUNCTION ONLY, DO NOT USE FOR ASYNCHRONOUS FUNCTION AS IT BYPASS THE `__is_runnning` FLAG.
    """
    
    def helper(b : queue.Queue, f, *a, **ka):
        """
        Helper function to get return from function.
        """
        
        lock = threading.Lock()
        with lock:
            b.put(f(*a, **ka))

    
    def timeout_decorator(func):
        """
        Decorator for timeout.
        """
        
        wraps(func)
        def wrapper(*a, **ka):
            helper_queue = queue.Queue()
            lock = threading.Lock() # Prevent potential data race.
            
            new_thread = Run_only_Thread(helper, helper_queue, func, *a, **ka)
            new_thread.start()
            new_thread.join(time)
            
            if new_thread.is_running():
                new_thread.terminate()
                
                if hasattr(action, "__call__"):
                    return action(*action_args, **action_kwargs) #type: ignore
                
                else:
                    return action

            with lock:
                return helper_queue.get()

        return wrapper
    return timeout_decorator
