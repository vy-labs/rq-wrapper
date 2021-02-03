import os

DEFAULT_JOB_CLASS = 'rq_wrapper.job.Job'
DEFAULT_QUEUE_CLASS = 'rq_wrapper.Queue'
DEFAULT_WORKER_CLASS = 'rq_wrapper.Worker'
DEFAULT_CONNECTION_CLASS = 'redis.Redis'
DEFAULT_WORKER_TTL = 420
DEFAULT_JOB_MONITORING_INTERVAL = 30
DEFAULT_RESULT_TTL = 500
DEFAULT_FAILURE_TTL = 31536000  # 1 year in seconds
DEFAULT_LOGGING_DATE_FORMAT = '%H:%M:%S'
DEFAULT_LOGGING_FORMAT = '%(asctime)s %(message)s'


namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID')
DEFAULT_NAMESPACE = ":{}".format(namespace) if namespace else ''
DEFAULT_QUEUE_TIMEOUT = int(os.getenv('RQ_QUEUE_TIMEOUT', 180))
