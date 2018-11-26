import os
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command
from rq import Queue

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from pycoins.heroku.worker import conn


def notify():
    return q.enqueue(call_command, 'notify')


if __name__ == '__main__':
    q = Queue(connection=conn)
    sched = BlockingScheduler()
    sched.scheduled_job('interval', minutes=30)(notify)
    sched.start()
