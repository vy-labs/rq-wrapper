from rq import Queue as RqQueue


class Queue(RqQueue):
    def __init__(self, *args, **kwargs):
        super().__init__('1234:default', **kwargs)


