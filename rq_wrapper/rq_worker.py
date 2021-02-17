from rq import Worker as RqWorker, get_current_connection

from rq.compat import as_text
from rq.worker import compact

from rq_wrapper.settings import namespace


class Worker(RqWorker):

    @classmethod
    def all(cls, connection=None, job_class=None, queue_class=None, queue=None, serializer=None):
        """Returns an iterable of all Workers.
        """
        if queue:
            connection = queue.connection
        elif connection is None:
            connection = get_current_connection()

        worker_keys = [key for key in connection.smembers('rq:workers:{}'.format(namespace))]
        workers = [cls.find_by_key(as_text(key),
                                   connection=connection,
                                   job_class=job_class,
                                   queue_class=queue_class, serializer=serializer)
                   for key in worker_keys]
        return compact(workers)

