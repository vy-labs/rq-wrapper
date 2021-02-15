import rq.registry
import rq.registry
import rq_dashboard.web as web
from rq.registry import FailedJobRegistry, ScheduledJobRegistry, DeferredJobRegistry, FinishedJobRegistry, \
    StartedJobRegistry

from rq_wrapper.rq_queue import Queue


class RqFailedJobRegistry(FailedJobRegistry):
    def __init__(self, *args, **kwargs):
        super().__init__(name='123422:default', *args, **kwargs)


class RqScheduledJobRegistry(ScheduledJobRegistry):
    def __init__(self, *args, **kwargs):
        super().__init__(name='123422:default', *args, **kwargs)


class RqDeferredJobRegistry(DeferredJobRegistry):
    def __init__(self, *args, **kwargs):
        super().__init__(name='123422:default', *args, **kwargs)


class RqFinishedJobRegistry(FinishedJobRegistry):
    def __init__(self, *args, **kwargs):
        super().__init__(name='123422:default', *args, **kwargs)


class RqStartedJobRegistry(StartedJobRegistry):
    def __init__(self, *args, **kwargs):
        super().__init__(name='123422:default', *args, **kwargs)


# class FailedQueue(Queue):
#     def __init__(self, *args, **kwargs):
#         super().__init__('1234:failed', **kwargs)


# def get_queue(queue_name):
#     # prefix, q_name = queue_name.split(':')
#     if queue_name == 'failed':
#         return FailedQueue()
#     else:
#         return Queue("1234:{}".format(queue_name))


web.Queue = Queue
rq.registry.FailedJobRegistry = RqFailedJobRegistry
rq.registry.StartedJobRegistry = RqStartedJobRegistry
rq.registry.ScheduledJobRegistry = RqScheduledJobRegistry
rq.registry.FinishedJobRegistry = RqFinishedJobRegistry
rq.registry.DeferredJobRegistry = RqDeferredJobRegistry
from rq_dashboard.cli import main

main()
