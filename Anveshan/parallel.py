import threading
import time

class AsyncJob(threading.Thread):
	def __init__(self, task, params):
		threading.Thread.__init__(self, target=task, args=params)
		self.task = task
		self.params = params

	def run(self):
		#time.sleep(2)
		self.task(*self.params)
