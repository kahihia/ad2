from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from order_management.models import Order
import celery
from django.contrib.auth.models import User
from datetime import datetime
from celery.schedules import timedelta

app = Celery('IrisOnline', broker='redis://localhost:6379/0')


@app.task(bind=True, name="expire")
def expire(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.queue_id = self.request.id
        print(f"queue_id: {order.queue_id}")
        order.save()
        expire_async.apply_async(args=(order.id,), eta=datetime.utcnow() + timedelta(days=2),
                                 task_id=self.request.id)
    except:
        print(f"Failed retrieving order object of id {order_id}")
        return


@app.task(bind=True, name="expire_async")
def expire_async(self, order_id):
    print(f"the task queue id is {self.request.id}")
    try:
        order = Order.objects.get(id=order_id)
        print(f"the order status is {order.status}")
    except:
        print(f"Failed retrieving order object of id {order_id}")
        return

    if order.status != "P":
        return

    # Place products back to inventory
    line_items = order.orderlineitems_set.all()

    for line_item in line_items:
        product = line_item.product
        quantity = line_item.quantity

        product.quantity += quantity
        product.save()

    # Cancel order
    order.status = "C"
    order.save()
