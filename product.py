import os
import json
import subprocess
from multiprocessing import Process

def load_products(file_path):
    """Load products from the JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def run_bot(store, url, product_name, max_price):
    """Run the appropriate bot script for the given store."""
    print(f"Starting bot for {product_name} on {store} with URL: {url} and max price: {max_price}")
    try:
        # Create a unique user-data-dir for each bot instance
        user_data_dir = f"C:\\Users\\17726\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\{store}_{product_name.replace(' ', '_')}"
        os.makedirs(user_data_dir, exist_ok=True)

        # Run the appropriate bot script
        if store == "walmart":
            subprocess.Popen(
                ["cmd", "/k", "python", "Bots/walmart_bot.py", url, str(max_price), user_data_dir, store],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif store == "target":
            subprocess.Popen(
                ["cmd", "/k", "python", "Bots/target_bot.py", url, str(max_price), user_data_dir, store],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        elif store == "bestbuy":
            subprocess.Popen(
                ["cmd", "/k", "python", "Bots/bestbuy_bot.py", url, str(max_price), user_data_dir, store],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            print(f"⚠️ No bot available for store: {store}")
    except Exception as e:
        print(f"❌ Error running bot for {product_name} on {store}: {e}")

def main():
    # Kill any existing Brave processes
    print("🔁 Killing any existing Brave processes...")
    os.system("taskkill /F /IM brave.exe")

    # Load products from JSON
    products = load_products("products.json")

    # Create a list to hold processes
    processes = []

    # Iterate through products and process each one
    for product in products:
        if product["auto_buy"]:  # Only process products marked for auto-buy
            for store, url in product["urls"].items():
                if url:  # If a URL exists for the store
                    # Create a new process for each store-product combination
                    p = Process(target=run_bot, args=(store, url, product["name"], product["max_price"]))
                    processes.append(p)
                    p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()