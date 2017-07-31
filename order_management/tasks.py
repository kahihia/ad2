from .models import Order, ProductAssociation
from entity_management.models import Product
from celery.schedules import crontab
from celery.task import periodic_task


def get_recommended_products(product):
    associations = ProductAssociation.objects.filter(root_product=product)
    associations = associations.order_by('-probability')[:3]  # Negative sign means DESC
    products = [association.associated_product for association in associations]
    return products


@periodic_task(run_every=(crontab(hour='*/24')), name="calculate_recommendations")
def calculate_recommendations():
    products = Product.objects.filter(is_active=True)
    for product in products:
        print(f"Calculating Recommendations for {product.name}...")
        product_recommendations = calculate_recommendations_for_product(root_product=product)

        for recommendation in product_recommendations:
            association, is_created = ProductAssociation.objects.get_or_create(root_product=product,
                                                                               associated_product=recommendation.associated_product,
                                                                               defaults={"probability": 0.00})
            association.probability = recommendation.probability
            association.save()

    print("Recommendation calculation done")


def calculate_recommendations_for_product(root_product):
    recommended_products = []

    products = Product.objects.filter(is_active=True)
    for associated_product in products:
        if associated_product.id == root_product.id:
            continue

        associated_product_probability = get_probability(associated_product)

        if associated_product_probability == 0:
            probability_of_purchasing = 0
        else:
            probability_of_purchasing = get_probability(associated_product,
                                                        root_product) / associated_product_probability

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
    total_count = total_orders_count()
    if total_count == 0:
        return 0
    return count_occurrences(*products) / total_count
