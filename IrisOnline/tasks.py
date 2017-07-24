from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from order_management.models import Order


app = Celery('IrisOnline', broker='redis://localhost:6379/0')


# @app.task
# def printthis(*args,**kwargs):
#     order_id = args[0]
#     # Order.objects.get(id=)
#     print("Keiths a dolt")

#
# @periodic_task(run_every=(crontab(hour='4', minute='3', day_of_week="*")), name="test_function", ignore_result=True)
# def testfunction():
#     object = "not expired"
#     print(object)

@app.task(name="expire")
def expire(order_id):
    print(order_id)
    print("this works")
    try:
        order = Order.objects.get(id=order_id)
        print(order)
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
    print(order.status)
    order.save()


