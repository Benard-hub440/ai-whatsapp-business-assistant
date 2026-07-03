import json
import os


# ==========================================
# Load Products
# ==========================================

def load_products(filename):

    with open(f"products/{filename}") as f:
        products = json.load(f)

    return products
    

# ==========================================
# Load Business
# ==========================================

def load_business(filename):

    with open(f"businesses/{filename}") as f:
        business = json.load(f)

    return business


# ==========================================
# Find Business
# ==========================================

def find_business(phone):

    for filename in os.listdir("businesses"):

        business = load_business(filename)

        if business["phone"] == phone:
           return business

    return None

