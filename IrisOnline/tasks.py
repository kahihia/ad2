from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task

app = Celery('IrisOnline', broker='redis://localhost:6379/0')


@app.task
def printthis():
    print("Keiths a dolt")


@periodic_task(run_every=(crontab(hour='4', minute='3', day_of_week="*")), name="test_function", ignore_result=True)
def testfunction():
    object = "not expired"
    print(object)
