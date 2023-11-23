import structlog
from rq import Queue as RqQueue
from rq.compat import as_text
from rq.connections import resolve_connection

from rq_wrapper.settings import RQ_RESULT_TTL, namespace

logger = structlog.getLogger(__name__)


class Queue(RqQueue):
    def __init__(self, *_args, job_id=None, **kwargs):
        name = job_id or namespace
        super().__init__(name=name, **kwargs)

    def enqueue_call(self, func, args=None, kwargs=None, timeout=None,
                     result_ttl=RQ_RESULT_TTL, ttl=None, failure_ttl=None, description=None,
                     depends_on=None, job_id=None, at_front=False, meta=None,
                     retry=None, on_success=None, on_failure=None, pipeline=None):
        job = super(Queue, self).enqueue_call(func, args=args, kwargs=kwargs, timeout=timeout, result_ttl=result_ttl,
                                              ttl=ttl, failure_ttl=failure_ttl, description=description,
                                              depends_on=depends_on, job_id=job_id, at_front=at_front, meta=meta,
                                              retry=retry, on_success=on_success, on_failure=on_failure,
                                              pipeline=pipeline)
        context = dict(structlog.threadlocal.as_immutable(logger)._context)
        with structlog.threadlocal.tmp_bind(logger):
            if context.get('task_id') and context.get('task_name'):
                logger.unbind(*['task_id', 'task_name', 'queue'])
                logger.bind(**{'parent_task_id': context['task_id'], 'parent_task_name': context['task_name']})
            logger.info("task_enqueued", task_name=job.func_name, task_id=job.id,
                        task_status=job.get_status(refresh=False), queue=self.name)
        return job

    @classmethod
    def dequeue_any(cls, queues, timeout, connection=None, job_class=None, serializer=None):
        job, queue = super(cls, cls).dequeue_any(queues, timeout, connection, job_class, serializer)
        if job is not None and queue is not None:
            logger.new()
            logger.bind(task_id=job.id)
            logger.bind(task_name=job.func_name)
            logger.bind(queue=queue.name)
            logger.info("task_received", task_status=job.get_status(refresh=False))
        return job, queue

    @classmethod
    def all(cls, connection=None, job_class=None, serializer=None):
        """Returns an iterable of all Queues.
        """
        connection = resolve_connection(connection)

        def to_queue(queue_key):
            return cls.from_queue_key(as_text(queue_key),
                                      connection=connection,
                                      job_class=job_class, serializer=serializer)

        return [to_queue("{0}{1}".format(cls.redis_queue_namespace_prefix, namespace))]
