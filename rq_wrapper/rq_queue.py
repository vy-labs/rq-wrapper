from rq import Queue as RqQueue
from rq.compat import as_text
from rq.connections import resolve_connection

from rq_wrapper.settings import namespace


class Queue(RqQueue):

    def __init__(self, *_args, **kwargs):
        super().__init__(name=namespace, **kwargs)

    @classmethod
    def all(cls, connection=None, job_class=None, serializer=None):
        """Returns an iterable of all Queues.
        """
        connection = resolve_connection(connection)

        def to_queue(queue_key):
            return cls.from_queue_key(as_text(queue_key),
                                      connection=connection,
                                      job_class=job_class, serializer=serializer)

        return [to_queue("{}{}".format(cls.redis_queue_namespace_prefix, namespace))]
