from decouple import config
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, create_engine, select

from .models import Category, Transaction

SQLLITE_URL = config("DATABASE")

engine = create_engine(SQLLITE_URL, echo=False)


def init_db(engine=engine):
    SQLModel.metadata.create_all(engine)


def get_session(engine=engine) -> Session:
    return Session(engine)


def create_category(category_name: str, budget: int, engine=engine):
    with get_session(engine) as session:
        new_category = Category(category_name=category_name.title(), budget=budget)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)


def add_transaction_and_check_budget_deficit(
    amount: float, remark: str, category_id: int, recurrence: bool = False
) -> bool:
    with get_session() as session:
        new_transaction = Transaction(
            amount=amount, remark=remark, recurrence=recurrence, category_id=category_id
        )
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)
        return update_used_budget(session, amount, category_id)


def get_category_id(category_name: str) -> int:
    """Get the category id for the corresponsing category"""
    with get_session() as session:
        return session.exec(
            select(Category.id).where(Category.category_name == category_name)
        ).one()


def get_categories():
    """Get the list of all created categories"""
    with get_session() as session:
        return session.exec(select(Category.category_name)).all()


def update_used_budget(session: Session, amount: float, category_id: int) -> bool:
    category = session.exec(select(Category).where(Category.id == category_id)).one()
    category.used_budget = category.used_budget + amount
    session.add(category)
    session.commit()
    session.refresh(category)
    return category.used_budget > category.budget


def get_budget_info() -> list[Category]:
    with get_session() as session:
        return session.exec(
            select(Category).options(selectinload(Category.transactions))
        ).all()
