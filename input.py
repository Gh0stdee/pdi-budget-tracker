from sqlmodel import select

from db import get_session
from models import category, transaction


def get_number_of_categories() -> int:
    """select/read the id column from the categories table and return number of categories"""
    with get_session() as session:
        return len(session.exec(select(category.id)).all())


def create_transaction() -> transaction:
    while True:
        # TODO:read from the categories table and enumerate the categories
        try:
            category_index = int(
                input("Which category does the transaction belong to?")
            )
        except TypeError:
            print("Please input a number.")
            continue
        if category_index > get_number_of_categories():
            print("Please select from the given categories.")
            continue
        else:
            break
    # TODO:add category when creating the transaction
    return transaction(remark=input().strip())


def add_transactions():
    added_transactions = []
    with get_session() as session:
        while True:
            new_transaction = create_transaction()
            added_transactions.append(new_transaction)
            continue_session = (
                input("Any other transactions to be added(Y/N)").strip().lower()
            )
            if continue_session == "N":
                break
        session.add_all(added_transactions)
        session.commit()
        for added_transaction in added_transactions:
            session.refresh(added_transaction)
