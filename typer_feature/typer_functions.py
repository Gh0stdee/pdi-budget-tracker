import typer

from database_feature.db import (
    add_transaction_and_check_budget_deficit,
    create_category,
    get_categories,
    get_category_id,
    init_db,
)
from main import console, print_summary

app = typer.Typer()


@app.command()
def ty_create_category(
    category=typer.Argument(..., help="Name of new category"),
    budget=typer.Argument(..., help="Budget for new category"),
):
    """Add category to your budget tracker"""
    init_db()
    create_category(category, budget)


@app.command()
def ty_show_categories():
    """Show all created categories"""
    init_db()
    for category in get_categories():
        console.print(category)


@app.command()
def ty_add_transaction(
    amount=typer.Argument(..., help="Transaction amount"),
    remark=typer.Argument(..., help="Remark about transaction"),
    category=typer.Argument(..., help="Category the transaction belongs to"),
    recurrence=typer.Option(False, help="Set recurring transaction"),
):
    """Add transaction to budget tracker"""
    init_db()
    if not recurrence:
        budget_deficit = add_transaction_and_check_budget_deficit(
            amount, remark, get_category_id(category)
        )
    else:
        budget_deficit = add_transaction_and_check_budget_deficit(
            amount, remark, get_category_id(category), recurrence
        )
    if budget_deficit:
        console.print(
            f"You have exceeded the budget set for the {category.title()} category."
        )
    else:
        console.print("The transaction has been added.")


@app.command()
def ty_print_summary():
    """Print budget summary for all categories"""
    init_db()
    print_summary()
