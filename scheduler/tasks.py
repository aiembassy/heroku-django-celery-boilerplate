from datetime import datetime

from celery import shared_task


@shared_task(name="celery_heartbeat")
def celery_heartbeat():
    return "Celery heartbeat at {}".format(datetime.now())
