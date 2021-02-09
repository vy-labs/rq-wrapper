from rq_wrapper import Job, Queue, Worker, requeue_job, FinishedJobRegistry, FailedJobRegistry, StartedJobRegistry, ScheduledJobRegistry, DeferredJobRegistry

import rq_dashboard.web as web

web.Job = Job
web.Queue = Queue
web.Worker = Worker
web.requeue_job = requeue_job
web.FinishedJobRegistry = FinishedJobRegistry
web.FailedJobRegistry = FailedJobRegistry
web.StartedJobRegistry = StartedJobRegistry
web.ScheduledJobRegistry = ScheduledJobRegistry
web.DeferredJobRegistry = DeferredJobRegistry

from rq_dashboard.cli import main

main()
