from .models import Order, ProductAssociation
from entity_management.models import Product


def calculate_recommendations():
    for product in Product.objects.all():
        product_recommendations = get_recommendations(root_product=product)

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


def get_recommendations(root_product):

    recommended_products = []

    for associated_product in Product.objects.all():
        if associated_product.id == root_product.id:
            continue

        associated_product_probability = get_probability(associated_product)

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
    total_count = total_orders_count()
    if total_count == 0:
        return 0

    return count_occurrences(*products) / total_count
