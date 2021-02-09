from rq.job import Job as rqJob

from .defaults import DEFAULT_NAMESPACE


class Job(rqJob):
    redis_job_namespace_prefix = 'rq:job{}:'.format(DEFAULT_NAMESPACE)

    @property
    def failed_job_registry(self):
        from .registry import FailedJobRegistry
        return FailedJobRegistry(self.origin, connection=self.connection,
                                 job_class=self.__class__)

    def requeue(self):
        """Requeues job."""
        return self.failed_job_registry.requeue(self)

def requeue_job(job_id, connection):
    job = Job.fetch(job_id, connection=connection)
    return job.requeue()
