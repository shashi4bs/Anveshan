import threading
import time
import multiprocessing
import ctypes


class ThreadManager(object):
    __instance = None
    @staticmethod
    def get_instance():
        if ThreadManager.__instance is None:
            ThreadManager()
        return ThreadManager._instance
    
    def __init__(self):
        if ThreadManager.__instance is not None:
            raise Exception("More Than One Instance Not Allowed")
        else:
            ThreadManager.__instance = self
            self.threads = {}

    def keep_thread_trace(self, name, thread):
        if name not in self.threads:
            self.threads[name] = list(thread)
        else:
            self.threads[name].append(thread)
    
    def kill_thread(self, name):
        if name in self.threads:
            for thread in self.threads[name]:
                thread_id = thread.get_id()
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
                if res > 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                    print("Execution Failure")

thread_manager = ThreadManager()

def kill_thread(name):
    thread_manager.kill_thread(name)


class AsyncJob(threading.Thread):
    def __init__(self, task, params):
        threading.Thread.__init__(self, target=task, args=params)
        self.task = task
        self.params = params
        
    def keep_trace(self, name):
        thread_manager.keep_thread_trace(self, name)

    def run(self):
        try:
            #time.sleep(2)
            self.task(*self.params)
        finally:
            print("Thread Execution End")

    def get_id(self):
        if hasattr(self, 'thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
        

class AsyncProcess(multiprocessing.Process):
    def __init__(self, task, params):
        multiprocessing.Process.__init__(self, target=task, args=params)
        self.task = task
        self.params = params

    def run(self):
        try:
            self.task(*self.params)
            self.terminate()
        finally:
            print("Process Execution End")


