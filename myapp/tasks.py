from celery import Celery


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def addition(a, b):
    return a + b
