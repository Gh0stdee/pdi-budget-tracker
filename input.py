from db import get_session
from models import transaction

# TODO:read from categories table and get the number of categories
NUM_CATEGORY = 5


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
        if category_index > NUM_CATEGORY:
            print("Please select from the given categories.")
            continue
        else:
            break
    # TODO:add category when creating the transaction
    return transaction(remark=input().strip())


def add_transactions():
    session = get_session()
    while True:
        session.add(create_transaction())
        continue_session = (
            input("Any other transactions to be added(Y/N)").strip().lower()
        )
        if continue_session == "N":
            break
    session.commit()
