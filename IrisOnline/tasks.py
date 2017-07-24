from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from order_management.models import Order


app = Celery('IrisOnline', broker='redis://localhost:6379/0')


@app.task
def printthis(*args,**kwargs):
    order_id = args[0]
    # Order.objects.get(id=)
    print("Keiths a dolt")

#
# @periodic_task(run_every=(crontab(hour='4', minute='3', day_of_week="*")), name="test_function", ignore_result=True)
# def testfunction():
#     object = "not expired"
#     print(object)



