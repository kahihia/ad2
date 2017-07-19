from .models import Order, ProductAssociation
from entity_management.models import Product


def calculate_recommendations():
    for product in Product.objects.all():
        print(f"Performing recommendations for {product.name}")
        print()
        product_recommendations = get_recommendations(root_product=product)
        print(f"Recommendations for {product.name}: {product_recommendations}")

        for recommendation in product_recommendations:
            association = ProductAssociation.objects.filter(root_product=product,
                                                            associated_product=recommendation.associated_product)

            if association:
                association = association[0]
                association.probability = recommendation.probability
                association.save()
                print(association)
            else:
                association = ProductAssociation.objects.create(root_product=product,
                                                                associated_product=recommendation.associated_product,
                                                                probability=recommendation.probability)
                print(association)


def get_recommendations(root_product):
    if total_orders_count() == 0:
        # No orders yet, there are no recommendations
        return []

    root_product_probability = get_probability(root_product)
    if root_product_probability == 0:
        # Product has not been ordered, there are no recommendations
        return []

    recommended_products = []

    for associated_product in Product.objects.all():
        if associated_product.id == root_product.id:
            continue

        probability_of_purchasing = get_probability(root_product, associated_product) / root_product_probability

        recommended_products.append(ProductAssociation(root_product=root_product, associated_product=associated_product,
                                                       probability=probability_of_purchasing))

    return recommended_products


def count_occurrences(*products):
    orders = Order.objects.all()
    # Get amount of orders that has products *products
    return len([order for order in orders if order.has_products(*products)])


def total_orders_count():
    return len(Order.objects.all())


def get_probability(*products):
    return count_occurrences(*products) / total_orders_count()
