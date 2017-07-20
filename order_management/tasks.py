from .models import Order, ProductAssociation
from entity_management.models import Product
from celery.schedules import crontab
from celery.task import periodic_task

<<<<<<< HEAD:order_management/tasks.py
@periodic_task(run_every=(crontab(minute='*/1')), name="calculate_recommendations")
=======
def get_recommended_products(product):
    associations = ProductAssociation.objects.filter(root_product=product)
    associations = associations.order_by('-probability')[:3] # Negative sign means DESC
    products = [association.associated_product for association in associations]
    return products

>>>>>>> adc0b3033784b42845f8433e16f228db8ba3dbb7:order_management/recommended_items.py
def calculate_recommendations():
    print("calculate recommendations is working")
    for product in Product.objects.all():
        print(f"Calculating Recommendations for {product.name}...")
        product_recommendations = calculate_recommendations_for_product(root_product=product)

        for recommendation in product_recommendations:
            association = ProductAssociation.objects.filter(root_product=product,
                                                            associated_product=recommendation.associated_product)
            if association:
                association = association[0]
                association.probability = recommendation.probability
                association.save()
            else:
                ProductAssociation.objects.create(root_product=product,
                                                  associated_product=recommendation.associated_product,
                                                  probability=recommendation.probability)

        print()
    print("Recommendation calculation done")


def calculate_recommendations_for_product(root_product):

    recommended_products = []

    for associated_product in Product.objects.all():
        if associated_product.id == root_product.id:
            continue

        associated_product_probability = get_probability(associated_product)

        if associated_product_probability == 0:
            probability_of_purchasing = 0
        else:
            probability_of_purchasing = get_probability(associated_product, root_product) / associated_product_probability

        recommended_products.append(ProductAssociation(root_product=root_product,
                                                       associated_product=associated_product,
                                                       probability=probability_of_purchasing))

    return recommended_products


def count_occurrences(*products):
    orders = Order.objects.all()
    # Get amount of orders that has products *products
    return len([order for order in orders if order.has_products(*products)])


def total_orders_count():
    return len(Order.objects.all())


def get_probability(*products):
<<<<<<< HEAD:order_management/tasks.py
    return count_occurrences(*products) / total_orders_count()






=======
    total_count = total_orders_count()
    if total_count == 0:
        return 0

    return count_occurrences(*products) / total_count
>>>>>>> adc0b3033784b42845f8433e16f228db8ba3dbb7:order_management/recommended_items.py
