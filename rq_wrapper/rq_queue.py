from rq import Queue as RqQueue


class Queue(RqQueue):
    def __init__(self, name_prefix, **kwargs):
        super().__init__("{0}:default".format(name_prefix), **kwargs)
