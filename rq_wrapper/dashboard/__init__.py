import rq
import rq_dashboard.compat

from rq_wrapper.rq_queue import Queue
from rq_wrapper.rq_worker import Worker

rq_dashboard.web.Queue = Queue
rq_dashboard.web.Worker = Worker
rq_dashboard.compat.Queue = Queue

from rq_dashboard.cli import main

main()
