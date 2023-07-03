import oracledb

from rich.panel import Panel
from rich.console import Console

from model import Unexpirable_grocery, Minimal_information
import database_connection

connection = oracledb.connect(user = database_connection.USERNAME, password = database_connection.PASSWORD, 
                      encoding = "UTF-8", dsn = database_connection.dsn)

cursor = connection.cursor()

console = Console()

def error_message():
    text = "Stock not valid: the stock does not exist or you write it wrongly!\
              \n Please write the correct id of the product and retry."
    panel = Panel(text, expand=False, border_style="bold red", style="bold red on white")
    console.print(panel)

def get_all_stocks():
    cursor.execute("SELECT * FROM unexpirable_groceries")
    all_stocks = cursor.fetchall()
    stocks = [] 

    for stock in all_stocks:
        stocks.append(Unexpirable_grocery(stock[1], stock[2], stock[3], stock[4], stock[5], stock[0]))
    # print(stocks)
    return stocks

# Add to Inventory: This function will be used to insert new inventories into the database.
# It checks if the stock user wants to add to inventory is already there.
# If it is, it simply just increase the quantity of the stock by the quantity provided.

def insert_stocks(stock: Unexpirable_grocery):
    # cursor.execute("SELECT * FROM unexpirable_groceries WHERE LOWER(name=:name)", {'name': stock.name.lower(),})
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE name=:name", {'name': stock.name})
    results = cursor.fetchall()

    if len(results):
        # Get the product ID
        existing_stock = results[0]

        # Get the actual quantity and add to the arrival product
        new_quantity = existing_stock[3] + stock.quantity
        id = existing_stock[0]

        # with connection:
        cursor.execute("UPDATE unexpirable_groceries SET quantity=:quantity WHERE id=:id", 
                           {'id': id, 'quantity': new_quantity})
        connection.commit()
    else:
        # with connection:
            cursor.execute(
                "INSERT INTO unexpirable_groceries (name, category, created_at, updated_at, quantity) \
                    VALUES (:name, :category, :created_at, :updated_at, :quantity)", \
                    {  
                        "name": stock.name,                 
                        "category": stock.category,
                        "created_at": stock.created_at,
                        "updated_at": stock.updated_at,
                        "quantity": stock.quantity                
                    }
            )
            connection.commit()

# Reduce stock quantity: This function will accept the 'stock ID' and 'stock quantity' as arguments
# and simply search the database for stock whose Id matches the provided Id and validates that the stock exist.
# It also checks that the current quantity of the stock in the inventory is more than the quantity to be reduced.

def reduce_stock_quantity(id: int, quantity: int):
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()
    if not stock:
        error_message()
        return False
    else:
        new_stock_quantity =  stock[3] - quantity
        if new_stock_quantity < 0:
            print("Insufficient stock: There is no sufficient quantity you are looking for😓.")
            return False
        else:
            # with connection:
            cursor.execute("UPDATE unexpirable_groceries SET quantity=:quantity WHERE id=:id", 
                               {'id': id, 'quantity': new_stock_quantity})
            connection.commit()
            return True


# Increase stock quantity: This function will also accept the stock ID and stock quantity as arguments and
# also search the database for stock whose Id matches the provided Id and validates that the stock exists,
# then increases the stock by provided quantity.

def increase_stock_quantity(id: int, quantity: int):
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()

    if not stock:
        print("Stock not valid: the stock does not exist or you write it wrongly!\
              \n Please write the correct id of the product and retry.")

    else:
        new_stock_quantity = stock[3] + quantity
        # with connection:
        cursor.execute("UPDATE unexpirable_groceries SET quantity=:quantity WHERE id=:id", 
                           {'id': id, 'quantity': new_stock_quantity})
        connection.commit()
            
# Delete stock: The function will be required to clear and delete a stock from our inventory.
# It requires a stock Id as argument.
def delete_stock(id):
    # with connection:
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()

    if not stock:
        print("Stock not valid: the stock you want to delete does not exist or you write it wrongly!\
              \n Please write the correct id of the product and retry.")
        return False
    else:
        cursor.execute("DELETE FROM unexpirable_groceries WHERE id=:id", {'id': id})
        connection.commit()
        return True


def modify_stock(id, name, category, quantity):
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()

    if not stock:
        print("Stock not valid: the stock does not exist or you write it wrongly!\
              \n Please write the correct id of the product and retry.")
        return False
    else:
        cursor.execute("UPDATE unexpirable_groceries SET name=:name, category=:category, quantity=:quantity \
                        WHERE id=:id", {'id': id, 'name': name, 'category': category, 'quantity': quantity})
        connection.commit()
        return True


def search_stock(id, name, category, quantity):
    cursor.execute("SELECT * FROM unexpirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()

    search_result = []
    if not stock:
        print("Stock not valid: the stock does not exist or you write it wrongly!\
              \n Please write the correct id of the product and retry.") 
    else:
        cursor.execute()  
    
    return search_result

def out_of_stock():
    cursor.execute("SELECT id, name, category FROM unexpirable_groceries WHERE quantity = 0")
    stocks = cursor.fetchall()

    all_out_of_stocks = []
    if not stocks:
        return
    else:
        for stock in stocks:
            
            all_out_of_stocks.append(Minimal_information(stock[0], stock[1], stock[2])) 
        return all_out_of_stocks

def low_stock():
    cursor.execute("SELECT id, name, category, quantity FROM unexpirable_groceries WHERE quantity BETWEEN 1 AND 5")
    stocks = cursor.fetchall()

    all_out_of_stocks = []
    if not stocks:
        return
    else:
        for stock in stocks:
            all_out_of_stocks.append(Minimal_information(stock[0], stock[1], stock[2], stock[3])) 
        return all_out_of_stocks

def generate_PDF():
    pass

