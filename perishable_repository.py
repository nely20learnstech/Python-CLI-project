import oracledb
from model import Expirable_grocery
import database_connection

connection = oracledb.connect(user = database_connection.USERNAME, password = database_connection.PASSWORD, 
                      encoding = "UTF-8", dsn = database_connection.dsn)

cursor = connection.cursor()

def get_all_stocks():
    cursor.execute("SELECT * FROM expirable_groceries")
    all_stocks = cursor.fetchall()
    stocks = []

    for stock in all_stocks:
        stocks.append(Expirable_grocery(stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7], stock[0]))

    return stocks

# Add to Inventory: This function will be used to insert new inventories into the database.
# It checks if the stock user wants to add to inventory is already there.
# If it is, it simply just increase the quantity of the stock by the quantity provided.

def insert_stocks(stock: Expirable_grocery):
    cursor.execute("SELECT * FROM expirable_groceries WHERE LOWER(:name)", stock.name.lower())
    results = cursor.fetchall()

    if len(results):
        # Get the product ID
        existing_stock = results[0]

        # Get the actual quantity and add to the arrival product
        new_quantity = existing_stock[3] + stock.quantity
        id = existing_stock[0]

        with connection:
            cursor.execute("UPDATE expirable_groceries SET quantity=:quantity WHERE id=:id", 
                           {'id': id, 'quantity': new_quantity})
            connection.commit()
    else:
        with connection:
            cursor.execute(
                "INSERT INTO expirable_groceries (name, category, created_at, updated_at, quantity, product_creation_date, expiration_date) \
                VALUES (:name, :category, :created_at, :updated_at, :quantity, :product_creation_date, :expiration_date)", \
                    {  
                        "name": stock.name,                 
                        "category": stock.category,
                        "created_at": stock.created_at,
                        "updated_at": stock.updated_at,
                        "quantity": stock.quantity,
                         "product_creation_date": stock.product_creation_date,
                        "expiration_date": stock.expiration_date,                      
                    }
            )
            connection.commit()

# Reduce stock quantity: This function will accept the 'stock ID' and 'stock quantity' as arguments
# and simply search the database for stock whose Id matches the provided Id and validates that the stock exist.
# It also checks that the current quantity of the stock in the inventory is more than the quantity to be reduced.

def reduce_stock_quantity(id: int, quantity: int):
    cursor.execute("SELECT * FROM expirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()
    if not stock:
        print("Stock not valid")
        return
    else:
        new_stock_quantity =  stock[3] - quantity
        if new_stock_quantity < 0:
            print("Insufficient stock")
            return
        else:
            with connection:
                cursor.execute("UPDATE expirable_groceries SET quantity=:quantity WHERE id=:id", 
                               {'id': id, 'quantity': new_stock_quantity})


# Increase stock quantity: This function will also accept the stock ID and stock quantity as arguments and
# also search the database for stock whose Id matches the provided Id and validates that the stock exists,
# then increases the stock by provided quantity.

def increase_stock_quantity(id: int, quantity: int):
    cursor.execute("SELECT * FROM expirable_groceries WHERE id=:id", {'id': id})
    stock = cursor.fetchone()

    if not stock:
        print("Stock not valid: the stock does not exist or you write it wrongly!\
              \n Please write the correct name of the product and retry")

    else:
        new_stock_quantity = stock[3] + quantity
        with connection:
            cursor.execute("UPDATE expirable_groceries SET quantity=:quantity WHERE id=:id", 
                           {'id': id, 'quantity': new_stock_quantity})
            
# Delete stock: The function will be required to clear and delete a stock from our inventory.
# It requires a stock Id as argument.
def delete_stock(id):
    with connection:
        cursor.execute("DELETE FROM expirable_groceries WHERE id=:id", {'id': id})
