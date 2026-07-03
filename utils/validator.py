# ==========================================
# Find Product
# ==========================================

def find_product(products, product_name):

    if not product_name:
        return None

    product_name = product_name.strip().lower()

    for product in products:

        if product["name"].strip().lower() == product_name:
            return product

    return None