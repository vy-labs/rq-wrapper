from rq import Queue as RqQueue

from .settings import namespace


class Queue(RqQueue):
    redis_queue_namespace_prefix = "rq:queue:{}:".format(namespace)
    redis_queues_keys = "rq:queues:{}".format(namespace)
