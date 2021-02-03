import rq.cli.cli as cli

from rq.cli import worker, info, main

from rq_wrapper import __version__ as version
from rq_wrapper.cli.helpers import CliConfig
from rq_wrapper.defaults import (DEFAULT_JOB_CLASS,
                                 DEFAULT_QUEUE_CLASS, DEFAULT_WORKER_CLASS)
from rq_wrapper.registry import FailedJobRegistry, clean_registries

cli.version = version
cli.DEFAULT_JOB_CLASS = DEFAULT_JOB_CLASS
cli.DEFAULT_QUEUE_CLASS = DEFAULT_QUEUE_CLASS
cli.DEFAULT_WORKER_CLASS = DEFAULT_WORKER_CLASS
cli.FailedJobRegistry = FailedJobRegistry
cli.clean_registries = clean_registries
cli.CliConfig = CliConfig
