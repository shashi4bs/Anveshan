from parallel import AsyncJob, AsyncProcess

def run_in_parallel(some_function, *params):
	job = AsyncJob(some_function, params)
	job.start()

def run_spiders_in_parallel(keep_trace, name, some_function, *params):
	job = AsyncJob(some_function, params)
	if keep_trace:
		job.keep_trace(name)
	job.start()

def run_process(some_function, *params):
	process = AsyncProcess(some_function, params)
	process.start()

def test(a, b, c):
	print(a, b, c)
