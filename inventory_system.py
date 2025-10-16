import json
import logging
from datetime import datetime

# Configure logging to show timestamps and messages for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variable for inventory
stock_data = {}

# --- FIX 1: Mutable Default Argument ---
# Previous Buggy Code:
# def addItem(item="default", qty=0, logs=[]):
#     if not item:
#         return
#     stock_data[item] = stock_data.get(item, 0) + qty
#     logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def add_item(item, qty, logs=None):
    """Adds an item to the inventory stock."""
    # FIX: The default argument was changed from logs=[] to logs=None.
    # This prevents the mutable default argument bug, where all function calls
    # would share the same list, leading to incorrect log accumulation.
    if logs is None:
        logs = []

    # [cite_start]Added input validation for robustness [cite: 79]
    if not isinstance(item, str) or not isinstance(qty, int) or not item:
        logging.error("Invalid input: Item must be a non-empty string and quantity must be an integer.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # [cite_start]Using f-string for cleaner output [cite: 78]
    log_message = f"Added {qty} of {item}"
    logs.append(f"{datetime.now()}: {log_message}")
    logging.info(log_message)


# --- FIX 2: Bare Except Clause ---
# Previous Buggy Code:
# def removeItem(item, qty):
#     try:
#         stock_data[item] -= qty
#         if stock_data[item] <= 0:
#             del stock_data[item]
#     except:
#         pass

def remove_item(item, qty):
    """Removes a specified quantity of an item from stock."""
    try:
        if stock_data[item] > qty:
            stock_data[item] -= qty
        else:
            del stock_data[item]
        logging.info(f"Removed {qty} of {item}")
    # [cite_start]FIX: Replaced the bare 'except:' with 'except KeyError:'. [cite: 77]
    # This is much safer as it only catches the specific error we expect
    # (the item not being in the dictionary) and won't hide other bugs.
    except KeyError:
        logging.warning(f"Attempted to remove '{item}', which is not in stock.")

def get_qty(item):
    """Gets the quantity of a specific item."""
    return stock_data.get(item, 0)


# --- FIX 3: Unsafe File Handling ---
# Previous Buggy Code:
# def loadData(file="inventory.json"):
#     f = open(file, "r")
#     global stock_data
#     stock_data = json.loads(f.read())
#     f.close()

def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    global stock_data
    try:
        # FIX: Switched to using a 'with' statement for file operations.
        # This ensures the file is automatically closed, even if errors occur,
        # preventing potential resource leaks.
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Inventory data loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load data: {e}")
        stock_data = {} # Start with an empty inventory if file is bad

# Previous Buggy Code:
# def saveData(file="inventory.json"):
#     f = open(file, "w")
#     f.write(json.dumps(stock_data))
#     f.close()

def save_data(file="inventory.json"):
    """Saves inventory data to a JSON file."""
    try:
        # FIX: Switched to using a 'with' statement for file operations.
        # This is the standard, safe way to handle files in Python.
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
    # This call for a non-existent item will also be handled
    remove_item("orange", 1)
    
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    print_data()
    save_data()
    
    # --- FIX 4: Dangerous Use of eval() ---
    # Previous Buggy Code:
    # eval("print('eval used')")  # dangerous
    # FIX: Removed the dangerous eval() call. This eliminates a major security
    # vulnerability (identified by Bandit) as it prevents arbitrary code execution.

if __name__ == "__main__":
    main()