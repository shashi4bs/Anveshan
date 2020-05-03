from parallel import AsyncJob


def run_in_parallel(some_function, *params):
	job = AsyncJob(some_function, params)
	job.start()


def test(a, b, c):
	print(a, b, c)
