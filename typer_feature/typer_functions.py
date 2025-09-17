import typer

from database_feature.db import Database
from main import NUMBER_WARNING, console, print_summary

app = typer.Typer()


@app.command(name="add-category")
def create_category_cmd(
    category=typer.Argument(..., help="Name of new category"),
    budget=typer.Argument(..., help="Budget for new category"),
):
    """Add category to your budget tracker"""
    db = Database()
    db.create_category(category, budget)
    console.print(f"{category.title()} category has been created.")


@app.command(name="show-category")
def show_category_cmd():
    """Show all created categories"""
    db = Database()
    for category in db.get_categories():
        console.print(category)


@app.command(name="add-transaction")
def add_transaction_cmd(
    amount=typer.Argument(..., help="Transaction amount"),
    remark: str = typer.Argument(..., help="Remark about transaction"),
    category: str = typer.Argument(..., help="Category the transaction belongs to"),
    recurrence=typer.Option(False, help="Set recurring transaction"),
):
    """Add transaction to budget tracker"""
    db = Database()
    try:
        amount: float = float(amount)
        if amount < 0:
            raise ValueError
    except ValueError:
        console.print(NUMBER_WARNING)
        raise typer.Abort()
    recurrence: bool = bool(recurrence.title() == "True")
    category_id = db.get_category_id(category)
    if category_id is None:
        console.print("Invalid category.")
        return
    budget_deficit = db.add_transaction_and_check_budget_deficit(
        amount, remark, db.get_category_id(category), recurrence
    )
    if budget_deficit:
        console.print(
            f"You have exceeded the budget set for the {category.title()} category."
        )
    else:
        console.print("The transaction has been added.")


@app.command(name="print-summary")
def print_summary_cmd():
    """Print budget summary for all categories"""
    db = Database()
    print_summary(db)
