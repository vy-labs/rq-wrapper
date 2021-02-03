from rq.registry import BaseRegistry as rqBaseRegistry, StartedJobRegistry as rqStartedJobRegistry, \
    FailedJobRegistry as rqFailedJobRegistry, ScheduledJobRegistry as rqScheduledJobRegistry, \
    DeferredJobRegistry as rqDeferredJobRegistry, FinishedJobRegistry as rqFinishedJobRegistry
from rq.exceptions import InvalidJobOperation

import warnings
import rq

from .queue import Queue
from .defaults import DEFAULT_NAMESPACE

rq.registry.Queue = Queue


class BaseRegistry(rqBaseRegistry):
    key_template = 'rq:registry:{0}'+'{}'.format(DEFAULT_NAMESPACE)


class StartedJobRegistry(rqStartedJobRegistry):
    key_template = 'rq:wip:{0}'+'{}'.format(DEFAULT_NAMESPACE)


class FailedJobRegistry(rqFailedJobRegistry):
    key_template = 'rq:failed:{0}'+'{}'.format(DEFAULT_NAMESPACE)
    Queue = Queue

    def requeue(self, job_or_id):
        """Requeues the job with the given job ID."""
        if isinstance(job_or_id, self.job_class):
            job = job_or_id
        else:
            job = self.job_class.fetch(job_or_id, connection=self.connection)

        result = self.connection.zrem(self.key, job.id)
        if not result:
            raise InvalidJobOperation

        with self.connection.pipeline() as pipeline:
            queue = Queue(job.origin, connection=self.connection,
                          job_class=self.job_class)
            job.started_at = None
            job.ended_at = None
            job.save()
            job = queue.enqueue_job(job, pipeline=pipeline)
            pipeline.execute()
        return job


class DeferredJobRegistry(rqDeferredJobRegistry):
    key_template = 'rq:deferred:{0}'+'{}'.format(DEFAULT_NAMESPACE)

    def __init__(self):
        warnings.warn('rq-wrapper does not support deferred jobs')


class ScheduledJobRegistry(rqScheduledJobRegistry):
    key_template = 'rq:scheduled:{0}'+'{}'.format(DEFAULT_NAMESPACE)


class FinishedJobRegistry(rqFinishedJobRegistry):
    key_template = 'rq:finished:{0}'+'{}'.format(DEFAULT_NAMESPACE)


def clean_registries(queue):
    """Cleans StartedJobRegistry, FinishedJobRegistry and FailedJobRegistry of a queue."""
    registry = FinishedJobRegistry(name=queue.name,
                                   connection=queue.connection,
                                   job_class=queue.job_class)
    registry.cleanup()
    registry = StartedJobRegistry(name=queue.name,
                                  connection=queue.connection,
                                  job_class=queue.job_class)
    registry.cleanup()

    registry = FailedJobRegistry(name=queue.name,
                                 connection=queue.connection,
                                 job_class=queue.job_class)
    registry.cleanup()
