import rq.compat

rq.defaults.DEFAULT_QUEUE_CLASS = 'rq_wrapper.Queue'
rq.defaults.DEFAULT_WORKER_CLASS = 'rq_wrapper.Worker'

from rq.cli import main

main()
