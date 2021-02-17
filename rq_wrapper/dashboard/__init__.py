import rq
import rq_dashboard.compat

from rq_wrapper.rq_queue import Queue

rq.queue.Queue = Queue
rq_dashboard.web.Queue = Queue
rq_dashboard.compat.Queue = Queue

from rq_dashboard.cli import main

main()
