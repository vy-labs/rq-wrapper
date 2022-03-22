import structlog
from rq import Worker as RqWorker, get_current_connection
from rq.compat import as_text
from rq.worker import compact
from structlog_wrapper.python import configure_struct_logging

from rq_wrapper.rq_queue import Queue
from rq_wrapper.settings import namespace, app_name, app_type, environment, log_level

configure_struct_logging(app_name, app_type, environment, log_level=log_level)
logger = structlog.getLogger(__name__)


class Worker(RqWorker):
    queue_class = Queue

    def perform_job(self, job, queue):
        result = super(Worker, self).perform_job(job, queue)
        task_duration = str((job.ended_at - job.started_at).total_seconds()) + 's'
        logger.info("task_completed", task_id=job.id, task_name=job.func_name, task_duration=task_duration,
                    task_status=job.get_status(refresh=False), queue=queue.name)
        return result

    @classmethod
    def all(cls, connection=None, job_class=None, queue_class=None, queue=None, serializer=None):
        """Returns an iterable of all Workers.
        """
        if queue:
            connection = queue.connection
        elif connection is None:
            connection = get_current_connection()

        worker_keys = [key for key in connection.smembers('rq:workers:{0}'.format(namespace))]
        workers = [cls.find_by_key(as_text(key),
                                   connection=connection,
                                   job_class=job_class,
                                   queue_class=queue_class, serializer=serializer)
                   for key in worker_keys]
        return compact(workers)
