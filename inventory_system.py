import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variable
stock_data = {}

def add_item(item, qty, logs=None):
    """Adds an item to the inventory stock."""
    # Initialize logs list if it's not provided
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int) or not item:
        logging.error("Invalid item or quantity provided.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"Added {qty} of {item}"
    logs.append(f"{datetime.now()}: {log_message}")
    logging.info(log_message)

def remove_item(item, qty):
    """Removes a specified quantity of an item from stock."""
    try:
        if stock_data[item] > qty:
            stock_data[item] -= qty
        else:
            del stock_data[item]
        logging.info(f"Removed {qty} of {item}")
    except KeyError:
        logging.warning(f"Attempted to remove '{item}', which is not in stock.")

def get_qty(item):
    """Gets the quantity of a specific item."""
    return stock_data.get(item, 0)

def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Inventory data loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load data: {e}")
        stock_data = {} # Start with an empty inventory if file is bad

def save_data(file="inventory.json"):
    """Saves inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Inventory data saved successfully.")
    except IOError as e:
        logging.error(f"Failed to save data: {e}")

def print_data():
    """Prints a report of all items in the inventory."""
    print("\n--- Items Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(threshold=5):
    """Checks for items with stock below a certain threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]

def main():
    """Main function to run the inventory system."""
    load_data()
    add_item("apple", 10)
    add_item("banana", 5)
    
    # This call with invalid types will now be handled gracefully
    add_item(123, "ten")
    
    remove_item("apple", 3)
    # This call for a non-existent item will be handled
    remove_item("orange", 1)
    
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    print_data()
    save_data()
    
if __name__ == "__main__":
    main()