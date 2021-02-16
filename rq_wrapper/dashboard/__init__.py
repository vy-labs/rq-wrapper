import rq.registry
import rq_dashboard.web as web
from rq.compat import as_text
from rq.connections import resolve_connection
from rq.registry import FailedJobRegistry, ScheduledJobRegistry, DeferredJobRegistry, FinishedJobRegistry, \
    StartedJobRegistry

import os

from rq_wrapper.rq_queue import Queue

namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID')


# class RqFailedJobRegistry(FailedJobRegistry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(name='{}:default'.format(namespace), *args, **kwargs)
#
#
# class RqScheduledJobRegistry(ScheduledJobRegistry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(name='{}:default'.format(namespace), *args, **kwargs)
#
#
# class RqDeferredJobRegistry(DeferredJobRegistry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(name='{}:default'.format(namespace), *args, **kwargs)
#
#
# class RqFinishedJobRegistry(FinishedJobRegistry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(name='{}:default'.format(namespace), *args, **kwargs)
#
#
# class RqStartedJobRegistry(StartedJobRegistry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(name='{}:default'.format(namespace), *args, **kwargs)
#
#
# class FailedQueue(Queue):
#     def __init__(self, *args, **kwargs):
#         super().__init__('{}:failed'.format(namespace), **kwargs)
#
#
# def get_queue(queue_name):
#     if queue_name == '{}:failed'.format(namespace):
#         return web.get_failed_queue()
#     else:
#         return Queue(queue_name)


def all(cls, connection=None, job_class=None, serializer=None):
    """Returns an iterable of all Queues.
    """
    import pdb
    pdb.set_trace()
    connection = resolve_connection(connection)

    def to_queue(queue_key):
        return cls.from_queue_key(as_text(queue_key),
                                  connection=connection,
                                  job_class=job_class, serializer=serializer)

    keys = [key for key in connection.smembers(cls.redis_queues_keys)
            if key.endswith("{}:default".format(namespace))]
    print(keys)

    return [to_queue(rq_key)
            for rq_key in connection.smembers(keys)
            if rq_key]


web.Queue = Queue
web.Queue.all = all
# import pdb
# pdb.set_trace()
# rq.registry.FailedJobRegistry = RqFailedJobRegistry
# rq.registry.StartedJobRegistry = RqStartedJobRegistry
# rq.registry.ScheduledJobRegistry = RqScheduledJobRegistry
# rq.registry.FinishedJobRegistry = RqFinishedJobRegistry
# rq.registry.DeferredJobRegistry = RqDeferredJobRegistry
from rq_dashboard.cli import main

main()
