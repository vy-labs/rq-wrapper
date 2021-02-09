# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from os.path import exists

from dotenv import load_dotenv

from .queue import Queue
from .version import VERSION
from .job import Job, requeue_job
from .registry import BaseRegistry, StartedJobRegistry, ScheduledJobRegistry, FinishedJobRegistry, FailedJobRegistry, \
    DeferredJobRegistry
from .worker import Worker

dotenv_path = '/etc/environment'
if exists(dotenv_path):
    print("loading environment variables from /etc/environment file..")
    load_dotenv(dotenv_path)

__version__ = VERSION
