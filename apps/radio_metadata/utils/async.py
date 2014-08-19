# stdlib imports
import time

# third-party imports
import django_rq


__all__ = ['add_task']


class AsyncTask(object):
    """Wrapper for an rq Job instance that allows blocking until a result is
    available by calling .get_result()
    """

    def __init__(self, job):
        self.job = job

    def get_result(self):
        while self.job.result is None:
            time.sleep(0.01)
        return self.job.result


def add_task(*args, **kwargs):
    """Add delayed task to the default queue and return an AsyncTask instance
    """
    job = django_rq.enqueue(*args, **kwargs)
    return AsyncTask(job)
