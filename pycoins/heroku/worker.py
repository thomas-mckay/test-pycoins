import os
import sys

import redis
from django import setup
from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    setup()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
