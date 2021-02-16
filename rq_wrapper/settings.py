import os

namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID')
# QUEUES = ["{}:default".format(namespace)]
NAME = "{}:default".format(namespace)
RQ_QUEUE_CLASS = 'rq_wrapper.rq_queue.Queue'
QUEUE_CLASS = 'rq_wrapper.rq_queue.Queue'