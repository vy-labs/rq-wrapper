from rq.queue import Queue as rqQueue
from rq.compat import as_text
from redis import WatchError

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
        return DeferredJobRegistry(queue=self, job_class=self.job_class)

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

    def enqueue_dependents(self, job, pipeline=None):
        """Enqueues all jobs in the given job's dependents set and clears it.

        When called without a pipeline, this method uses WATCH/MULTI/EXEC.
        If you pass a pipeline, only MULTI is called. The rest is up to the
        caller.
        """
        from .registry import DeferredJobRegistry

        pipe = pipeline if pipeline is not None else self.connection.pipeline()
        dependents_key = job.dependents_key

        while True:
            try:
                # if a pipeline is passed, the caller is responsible for calling WATCH
                # to ensure all jobs are enqueued
                if pipeline is None:
                    pipe.watch(dependents_key)

                dependent_job_ids = [as_text(_id)
                                     for _id in pipe.smembers(dependents_key)]

                jobs_to_enqueue = [
                    dependent_job for dependent_job
                    in self.job_class.fetch_many(
                        dependent_job_ids,
                        connection=self.connection,
                        serializer=self.serializer
                    ) if dependent_job.dependencies_are_met(
                        exclude_job_id=job.id,
                        pipeline=pipe
                    )
                ]

                pipe.multi()

                for dependent in jobs_to_enqueue:
                    registry = DeferredJobRegistry(dependent.origin,
                                                   self.connection,
                                                   job_class=self.job_class)
                    registry.remove(dependent, pipeline=pipe)
                    if dependent.origin == self.name:
                        self.enqueue_job(dependent, pipeline=pipe)
                    else:
                        queue = self.__class__(name=dependent.origin, connection=self.connection)
                        queue.enqueue_job(dependent, pipeline=pipe)

                pipe.delete(dependents_key)

                if pipeline is None:
                    pipe.execute()

                break
            except WatchError:
                if pipeline is None:
                    continue
                else:
                    # if the pipeline comes from the caller, we re-raise the
                    # exception as it it the responsibility of the caller to
                    # handle it
                    raise
