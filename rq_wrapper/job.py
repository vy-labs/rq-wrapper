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

    def register_dependency(self, pipeline=None):
        """Jobs may have dependencies. Jobs are enqueued only if the job they
        depend on is successfully performed. We record this relation as
        a reverse dependency (a Redis set), with a key that looks something
        like:

            rq:job:job_id:dependents = {'job_id_1', 'job_id_2'}

        This method adds the job in its dependency's dependents set
        and adds the job to DeferredJobRegistry.
        """
        from .registry import DeferredJobRegistry

        registry = DeferredJobRegistry(self.origin,
                                       connection=self.connection,
                                       job_class=self.__class__)
        registry.add(self, pipeline=pipeline)

        connection = pipeline if pipeline is not None else self.connection

        for dependency_id in self._dependency_ids:
            dependents_key = self.dependents_key_for(dependency_id)
            connection.sadd(dependents_key, self.id)
            connection.sadd(self.dependencies_key, dependency_id)

    def delete(self, pipeline=None, remove_from_queue=True,
               delete_dependents=False):
        """Cancels the job and deletes the job hash from Redis. Jobs depending
        on this job can optionally be deleted as well."""
        if remove_from_queue:
            self.cancel(pipeline=pipeline)
        connection = pipeline if pipeline is not None else self.connection

        if self.is_finished:
            from .registry import FinishedJobRegistry
            registry = FinishedJobRegistry(self.origin,
                                           connection=self.connection,
                                           job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_deferred:
            from .registry import DeferredJobRegistry
            registry = DeferredJobRegistry(self.origin,
                                           connection=self.connection,
                                           job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_started:
            from .registry import StartedJobRegistry
            registry = StartedJobRegistry(self.origin,
                                          connection=self.connection,
                                          job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_scheduled:
            from .registry import ScheduledJobRegistry
            registry = ScheduledJobRegistry(self.origin,
                                            connection=self.connection,
                                            job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_failed:
            self.failed_job_registry.remove(self, pipeline=pipeline)

        if delete_dependents:
            self.delete_dependents(pipeline=pipeline)

        connection.delete(self.key, self.dependents_key, self.dependencies_key)


def requeue_job(job_id, connection):
    job = Job.fetch(job_id, connection=connection)
    return job.requeue()
