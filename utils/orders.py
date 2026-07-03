import json
import os
from datetime import datetime


# ==========================================
# Create Orders File
# ==========================================

def create_orders_file(filename):

    os.makedirs("orders", exist_ok=True)

    filepath = os.path.join("orders", filename)

    if not os.path.exists(filepath):

        with open(filepath, "w") as f:

            json.dump(
                {
                    "next_order_id": 1,
                    "orders": []
                },
                f,
                indent=4
            )

        print(f"Created orders file: {filepath}")


# ==========================================
# Load Orders
# ==========================================

def load_orders(filename):

    create_orders_file(filename)

    filepath = os.path.join("orders", filename)

    try:

        with open(filepath, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:

        print("=" * 60)
        print("WARNING: Orders file is corrupted.")
        print("Creating a new empty orders file...")
        print("=" * 60)

        data = {
            "next_order_id": 1,
            "orders": []
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        return data


# ==========================================
# Save Order
# ==========================================

def save_order(filename, customer, product, quantity):
    print("=" * 60)
    print("ENTERED save_order()")
    print("=" * 60)
    
    data = load_orders(filename)
    print("Current next_order_id:", data["next_order_id"])

    # --------------------------------------
    # Ensure quantity is valid
    # --------------------------------------

    try:

        quantity = int(quantity)

        if quantity <= 0:
            quantity = 1

    except (TypeError, ValueError):

        quantity = 1

    # --------------------------------------
    # Calculate Prices
    # --------------------------------------

    unit_price = product["price"]

    total_price = unit_price * quantity

    # --------------------------------------
    # Create Order
    # --------------------------------------

    order = {

        "order_id": data["next_order_id"],

        "customer": customer,

        "product_id": product["id"],

        "product": product["name"],

        "category": product["category"],

        "quantity": quantity,

        "unit": product["unit"],

        "unit_price": unit_price,

        "currency": product["currency"],

        "total_price": total_price,

        "status": "Pending",

        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    # --------------------------------------
    # Save Order
    # --------------------------------------
    print("Appending order...")
    data["orders"].append(order)
    print("Orders after append:", len(data["orders"]))

    data["next_order_id"] += 1

    filepath = os.path.join("orders", filename)
    print("Saving to:", filepath)
    with open(filepath, "w") as f:

        json.dump(data, f, indent=4)
        print("JSON FILE UPDATED SUCCESSFULLY")

    # --------------------------------------
    # Debug
    # --------------------------------------

    print("=" * 60)
    print("ORDER SAVED SUCCESSFULLY")
    print("=" * 60)
    print(f"Order ID    : {order['order_id']}")
    print(f"Customer    : {customer}")
    print(f"Product     : {order['product']}")
    print(f"Category    : {order['category']}")
    print(f"Quantity    : {quantity} {order['unit']}")
    print(f"Unit Price  : {order['currency']} {unit_price}")
    print(f"Total Price : {order['currency']} {total_price}")
    print(f"Status      : {order['status']}")
    print(f"Created At  : {order['created_at']}")
    print("=" * 60)

    return order