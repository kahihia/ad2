class Cart:
    def __init__(self, line_items = None):
        self.line_items = line_items if line_items else []

    def has_product(self, product):
        for line_item in self.line_items:
            if line_item.product is product:
                return True
        return False

    def product_count(self):
        return len(self.line_items)

    def get_line_item_for_product(self, product):
        for line_item in self.line_items:
            if line_item.product is product:
                return line_item

        return None


class LineItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

