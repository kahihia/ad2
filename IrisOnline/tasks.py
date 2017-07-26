from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from order_management.models import Order
import celery
from django.contrib.auth.models import User


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

@app.task(bind=True, name="expire")
def expire(self,order_id):
    print(f"the task queue id is {self.request.id}")
    try:
        order = Order.objects.get(id=order_id)
        print(f"the order status is {order.status}")
    except:
        print(f"Failed retrieving order object of id {order_id}")
        return


    if order.status == "C":
        print(f"this process terminated, order status:{order.status}")
        app.control.revoke(self.request.id, terminate = True)

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

# @periodic_task(run_every=(crontab(minute=1)),name="ban the damn anime")
# def ban_kammy():
#     # kammy = User.objects.get(username="inoyamanaka")
#     # if kammy: kammy.delete()
#
#     #lets step it up
#     users = User.objects.all()
#     kams_accounts = [user for user in users if user.username.includes("kam" or "ino" or "koreanshit")]
#     for account in kams_accounts:
#         account.delete()





