from rq import decorators

from rq_wrapper.rq_queue import Queue


class job(decorators.job):
    queue_class = Queue
