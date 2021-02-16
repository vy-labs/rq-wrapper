import os
from rq import Queue as RqQueue
from rq.compat import as_text
from rq.connections import resolve_connection

namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID')


class Queue(RqQueue):
    # redis_queues_keys = 'rq:queues:{}'.format(namespace)

    def __init__(self, *args , **kwargs):
        super().__init__("{}:default".format(namespace), **kwargs)

    # @classmethod
    # def all(cls, connection=None, job_class=None, serializer=None):
    #     """Returns an iterable of all Queues.
    #     """
    #     import pdb
    #     pdb.set_trace()
    #     connection = resolve_connection(connection)
    #
    #     def to_queue(queue_key):
    #         return cls.from_queue_key(as_text(queue_key),
    #                                   connection=connection,
    #                                   job_class=job_class, serializer=serializer)
    #
    #     keys = [key for key in connection.smembers(cls.redis_queues_keys)
    #             if key.endswith("{}".format(namespace))]
    #     print(keys)
    #
    #     return [to_queue(rq_key)
    #             for rq_key in connection.smembers(keys)
    #             if rq_key]
