from enum import IntEnum

import plotext as plt
from rich.console import Console

from database_feature.db import Database

FUNCTIONS: list[str] = ["Create Category", "Add Transaction", "Show Summary", "Quit"]
FUNCTION_SELECTION: str = "Please select a function: "
NON_NUMBER_WARNING: str = "Please enter an number."
UNAVAILABLE_CHOICE_WARNING: str = "Please choose from the above functions."
CATEGORY_NAME_INPUT: str = "Please name the category: "
QUIT = "Quit"


class Functions(IntEnum):
    CATEGORY = 1
    TRANSACTION = 2
    SUMMARY = 3
    QUIT = 4


console = Console()


def print_all_functions():
    console.print()
    for index, function in enumerate(FUNCTIONS, start=1):
        console.print(f"{index}. {function}")
    console.print()


def print_summary(db: Database):
    console.print()
    categories = []
    used_budget = []
    allocated_budget = []
    for category in db.get_budget_info():
        categories.append(category.category_name)
        allocated_budget.append(category.budget)
        used_budget.append(category.used_budget)
        console.print(f"For the {category.category_name} category:")
        console.print(
            f"You have allocated ${category.budget} and spent ${category.used_budget}[{category.used_budget / category.budget * 100:.2f}%]."
        )
        console.print("\nTransactions: ")
        if not category.transactions:
            console.print("No transaction in this category yet.")
        for transaction in category.transactions:
            console.print(
                f"- ${transaction.amount} for {transaction.remark} {'(recurring)' if transaction.recurrence else ''}"
            )
            console.print()
        console.rule()
    plt.simple_multiple_bar(
        categories,
        [allocated_budget, used_budget],
        labels=["Allocated budget", "Used budget"],
        width=plt.terminal_size()[0] - 10,
        title="Budget Usage for All Categories",
    )
    plt.show()


def main():
    db = Database()
    console.rule()
    print_all_functions()
    while True:
        try:
            choice = int(console.input(FUNCTION_SELECTION))
        except ValueError:
            console.print(NON_NUMBER_WARNING)
            console.print()
            continue
        if choice == Functions.CATEGORY:
            category_name = console.input("Please name the category: ").strip().title()
            while True:
                try:
                    budget = float(
                        console.input("What is the monthly budget for this category? ")
                    )
                    break
                except ValueError:
                    console.print(NON_NUMBER_WARNING)
                    console.print()
            db.create_category(category_name, budget)
            console.rule()
            break
        elif choice == Functions.TRANSACTION:
            categories = db.get_categories()
            categories.append(QUIT)
            for index, category in enumerate(categories, start=1):
                console.print(f"{index}. {category}")
            while True:
                try:
                    category_name = categories[
                        int(console.input("Insert the transaction category number: "))
                        - 1
                    ]
                    break
                except ValueError:
                    console.print(NON_NUMBER_WARNING)
                    console.print()
            if category_name == QUIT:
                break
            category_id = db.get_category_id(category_name)
            while True:
                try:
                    amount = float(console.input("Insert the transaction amount: $"))
                    break
                except ValueError:
                    console.print(NON_NUMBER_WARNING)
                    console.print()

            remark = console.input("Insert any remarks about the transaction: ")
            if db.add_transaction_and_check_budget_deficit(
                amount, remark, category_id, False
            ):
                console.print(
                    f"You have exceeded the budget set for the {category_name} category."
                )
            else:
                console.print("The transaction has been added.")
            console.rule()
            break
        elif choice == Functions.SUMMARY:
            print_summary(db)
            break
        elif choice == Functions.QUIT:
            break
        else:
            console.print(UNAVAILABLE_CHOICE_WARNING)
            console.print()
    console.print()


if __name__ == "__main__":
    main()
