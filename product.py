import json

def load_products(file_path="products.json"):
    """Load products from the JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def get_store_products(store_name, file_path="products.json"):
    """Return a list of products that contain URLs for the given store."""
    products = load_products(file_path)
    return [
        {
            "name": product["name"],
            "url": product["urls"].get(store_name),
            "max_price": product["max_price"]
        }
        for product in products
        if product["auto_buy"] and store_name in product["urls"]
    ]
