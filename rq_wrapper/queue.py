from rq.queue import Queue as rqQueue

from .defaults import DEFAULT_NAMESPACE, DEFAULT_QUEUE_TIMEOUT
from .job import Job


class Queue(rqQueue):
    job_class = Job
    DEFAULT_TIMEOUT = DEFAULT_QUEUE_TIMEOUT  # Default timeout seconds.
    redis_queue_namespace_prefix = 'rq:queue{}:'.format(DEFAULT_NAMESPACE)
    redis_queues_keys = 'rq:queues{}'.format(DEFAULT_NAMESPACE)

    @property
    def failed_job_registry(self):
        """Returns this queue's FailedJobRegistry."""
        from .registry import FailedJobRegistry
        return FailedJobRegistry(queue=self, job_class=self.job_class)

    @property
    def started_job_registry(self):
        """Returns this queue's StartedJobRegistry."""
        from .registry import StartedJobRegistry
        return StartedJobRegistry(queue=self, job_class=self.job_class)

    @property
    def finished_job_registry(self):
        """Returns this queue's FinishedJobRegistry."""
        from .registry import FinishedJobRegistry
        return FinishedJobRegistry(queue=self)

    @property
    def deferred_job_registry(self):
        """Returns this queue's DeferredJobRegistry."""
        from .registry import DeferredJobRegistry
        return DeferredJobRegistry()

    @property
    def scheduled_job_registry(self):
        """Returns this queue's ScheduledJobRegistry."""
        from .registry import ScheduledJobRegistry
        return ScheduledJobRegistry(queue=self, job_class=self.job_class)

    def schedule_job(self, job, datetime, pipeline=None):
        """Puts job on ScheduledJobRegistry"""
        from .registry import ScheduledJobRegistry
        registry = ScheduledJobRegistry(queue=self)

        pipe = pipeline if pipeline is not None else self.connection.pipeline()

        # Add Queue key set
        pipe.sadd(self.redis_queues_keys, self.key)
        job.save(pipeline=pipe)
        registry.schedule(job, datetime, pipeline=pipe)
        if pipeline is None:
            pipe.execute()
        return job
