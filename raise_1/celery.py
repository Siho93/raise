from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


app = Celery('celery', broker='amqp://localhost')


@app.task
def add(x, y):
    return x + y