from rq import Worker as RqWorker

from rq_wrapper.rq_queue import Queue
from .settings import namespace


class Worker(RqWorker):
    redis_worker_namespace_prefix = "rq:worker:{}:".format(namespace)
    queue_class = Queue

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue_class = Queue
