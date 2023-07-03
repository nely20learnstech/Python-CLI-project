import typer
import logging
from rich.console import Console
from rich.table import Table

from unperishable_repository import get_all_stocks, insert_stocks, reduce_stock_quantity, increase_stock_quantity, delete_stock, modify_stock, out_of_stock, low_stock, search_stock
from model import Unexpirable_grocery

# Logging configuration
logging.basicConfig(filename='operation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()
app = typer.Typer()

# We create a console instance that we will later use to print to the terminal
# and an instance of typer.Typer() which will be use to accept terminal commands from the user.

# We will start with a command to display our inventory in a tabular format on the terminal.

@app.command(short_help="Show all stocks")
def add(name: str, quantity: int, category: str):
    typer.echo("Adding new stock...\n")
    new_stock = Unexpirable_grocery(name, category, quantity)
    insert_stocks(new_stock)
    out_of_stock_alert()
    low_stock_warning()
    display()

@app.command(short_help="Reduce stock quantity")
def reduce_stock(id: int, quantity: int):
    typer.echo(f"Reducing stock quantity...\n")
    reduce_stock_quantity(id, quantity)
    out_of_stock_alert()
    low_stock_warning()
    display()

@app.command(short_help="Increase stock quantity")
def increase_stock(id: int, quantity: int):
    typer.echo(f"Increasing stock quantity...\n")
    increase_stock_quantity(id, quantity)
    out_of_stock_alert()
    low_stock_warning()
    display()

@app.command(short_help="Clear stock")
def clear_stock(id: int, justification: str):
    typer.echo(f"Clearing stock...\n")
    state = delete_stock(id)   
        
    if state:
        logging.info(f'Clearing stock with id: {id} because: {justification}')
        out_of_stock_alert()
        low_stock_warning()
        display()

@app.command(short_help="Modify stock information")
def rectifying_stock_data(id: int, name: str, category: str, quantity:int, justification:str):
    typer.echo(f"Modifying stock information...\n")
    state = modify_stock(id, name, category, quantity)
    if state:
        logging.info(f'Rectifying stock data with id:{id}, name: {name}, category: {category}, quantity: {quantity}. The justification is {justification}')
        out_of_stock_alert()
        low_stock_warning()
        display()

@app.command(short_help="Out of stock...")
def out_of_stock_alert():
    stocks = out_of_stock()

    if not stocks:
        return
    else:
        console.print("[bold red]********Alert! This or those items are out[/bold red]********")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("id", style="dim", width=6)
        table.add_column("Name", min_width=20, justify='center')
        table.add_column("Category", min_width=20, justify='center')

        for _, stock in enumerate(stocks):
            table.add_row(str(stock.id), stock.name, stock.category)
        console.print(table)
        print()

@app.command(short_help="Low stock...")
def low_stock_warning():
    stocks = low_stock()

    if not stocks:
        return
    else:
        console.print("[bold yellow]********Warning! This or those items are low.********[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("id", style="dim", width=6)
        table.add_column("Name", min_width=20, justify='center')
        table.add_column("Category", min_width=20, justify='center')
        table.add_column("Quantity", max_width=12, justify='center')

        for _, stock in enumerate(stocks):
            table.add_row(str(stock.id), stock.name, stock.category, str(stock.quantity))
        
        console.print(table)
        print()

@app.command(short_help="Damaged item(s)")
def damaged_item(id: int, quantity: int, justification: str):
    typer.echo("Removing damaged item(s)...")
    state = reduce_stock_quantity(id, quantity)
    if state:
        logging.info(f"{quantity} of product with id {id} is or are damaged. Justification: {justification}")
        out_of_stock()
        low_stock_warning()
        display()

# 1. We create a new command and added the helper text which can be used to know more about the command on the terminal
# 2. We create the 'display' function which will be invoked when the command is running.
# 3. In the display function:
#  - We use the get_all_stocks method in the repository to fetch all stocks in our inventory.
#  - We create a new table instance and add several columns to represent our inventory stock information.
#  - We loop through the stocks gotten from our inventory database and each stock a row ti the table.
#  - We finally print the table to the terminal.

@app.command(short_help="Show all stocks")
def display():
    stocks = get_all_stocks()
    # print(stocks)
    console.print("[bold magenta]-=-=-=-=-=-=-=-Stock Tracker Application-=-=-=-=-=-=-=-[/bold magenta]", ":notebook_with_decorative_cover:")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("id", style="dim", width=6)
    table.add_column("Name", min_width=20, justify='center')
    table.add_column("Category", min_width=20, justify='center')
    table.add_column("Quantity", max_width=12, justify='center')
    table.add_column("Created date", min_width=20, justify='center')
    table.add_column("Updated date", min_width=20, justify='center')
    table.add_column("Status",  min_width=20, justify='center')

    for _, stock in enumerate(stocks):
        depleted = ":red_circle:" if stock.quantity < 1 else ":green_circle:"
        # elif stock.quantity < 6
        table.add_row(str(stock.id), stock.name, stock.category, str(stock.quantity), str(stock.created_at), str(stock.updated_at), depleted)

    # Print the console
    console.print(table)

@app.command(short_help="Search item(s)")
def search_item(search_key: str = typer.Argument(None, help='Product id'),                
                 by_quantity: bool = typer.Option(..., help="Search by name"),
                 ):
    """For searching particular items"""
    
    if by_quantity:
        if search_key.isnumeric():
            print(f"Those item with number of {search_key} are:")
        else:
            print(f"Please print a number, '{search_key}' is not a number.")
    else:
        print(f"Here is the items you are looking for. Search key `{search_key}`")

        # id: int = typer.Argument(None, help='Product id'), 
        #          name: str = typer.Argument(None, help='Product id'),
        #          category: str = typer.Argument(None, help='Product id'),
        #          quantity: int = typer.Argument(None, help='Product id'),



if __name__ == '__main__':
    app()
