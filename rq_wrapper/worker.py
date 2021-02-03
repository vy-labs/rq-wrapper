from rq.worker import Worker as rqWorker, SimpleWorker, WorkerStatus

import rq

from .defaults import DEFAULT_NAMESPACE
from .job import Job
from .queue import Queue
from .registry import StartedJobRegistry, FailedJobRegistry

rq.worker.StartedJobRegistry = StartedJobRegistry
rq.worker.FailedJobRegistry = FailedJobRegistry


class Worker(rqWorker):
    redis_worker_namespace_prefix = 'rq:worker{}:'.format(DEFAULT_NAMESPACE)
    queue_class = Queue
    job_class = Job
