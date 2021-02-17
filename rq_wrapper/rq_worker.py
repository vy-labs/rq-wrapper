from rq import Worker as RqWorker

from rq_wrapper.rq_queue import Queue


class Worker(RqWorker):
    queue_class = Queue

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
