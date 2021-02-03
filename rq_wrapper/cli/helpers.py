from rq.cli.helpers import CliConfig as rqCliConfig, DEFAULT_CONNECTION_CLASS

import rq.cli.helpers as helpers

from rq_wrapper.defaults import (DEFAULT_JOB_CLASS,
                                 DEFAULT_QUEUE_CLASS, DEFAULT_WORKER_CLASS)

helpers.DEFAULT_JOB_CLASS = DEFAULT_JOB_CLASS
helpers.DEFAULT_QUEUE_CLASS = DEFAULT_QUEUE_CLASS
helpers.DEFAULT_WORKER_CLASS = DEFAULT_WORKER_CLASS


class CliConfig(rqCliConfig):
    """A helper class to be used with click commands, to handle shared options"""

    def __init__(self, url=None, config=None, worker_class=DEFAULT_WORKER_CLASS,
                 job_class=DEFAULT_JOB_CLASS, queue_class=DEFAULT_QUEUE_CLASS,
                 connection_class=DEFAULT_CONNECTION_CLASS, path=None, *args, **kwargs):
        self.url = url
        self.config = config
        self.worker_class = worker_class
        self.job_class = job_class
        self.queue_class = queue_class
        self.connection_class = connection_class
        self.path = path
        super().__init__(url=None, config=None, worker_class=DEFAULT_WORKER_CLASS,
                         job_class=DEFAULT_JOB_CLASS, queue_class=DEFAULT_QUEUE_CLASS,
                         connection_class=DEFAULT_CONNECTION_CLASS, path=None, *args, **kwargs)
