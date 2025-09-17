from decouple import config
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, create_engine, select

from .models import Category, Transaction

SQLLITE_URL: str = config("DATABASE")


class Database:
    def __init__(self, database_url=SQLLITE_URL):
        self.engine = create_engine(database_url, echo=False)
        self.init()

    def init(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)

    def create_category(self, category_name: str, budget: int):
        with self.get_session() as session:
            new_category = Category(category_name=category_name.title(), budget=budget)
            session.add(new_category)
            session.commit()
            session.refresh(new_category)

    def add_transaction_and_check_budget_deficit(
        self,
        amount: float,
        remark: str,
        category_id: int,
        recurrence: bool,
    ) -> bool:
        with self.get_session() as session:
            new_transaction = Transaction(
                amount=amount,
                remark=remark,
                recurrence=recurrence,
                category_id=category_id,
            )
            session.add(new_transaction)
            session.commit()
            session.refresh(new_transaction)
            return self.update_used_budget(session, amount, category_id)

    def get_all_category_name_and_id(self) -> list[str, int]:
        with self.get_session() as session:
            return session.exec(select(Category.category_name, Category.id)).all()

    def get_category_id(self, category_name_input: str) -> int | None:
        """Get the category id for the corresponsing category"""
        category_name_id = self.get_all_category_name_and_id()
        category_name_input = category_name_input.strip().title()
        for category_name, category_id in category_name_id:
            if category_name == category_name_input:
                return category_id
        return None

    def get_categories(self) -> list[str]:
        """Get the list of all created categories"""
        with self.get_session() as session:
            return session.exec(select(Category.category_name)).all()

    def update_used_budget(
        self, session: Session, amount: float, category_id: int
    ) -> bool:
        category = session.exec(
            select(Category).where(Category.id == category_id)
        ).one()
        category.used_budget = category.used_budget + amount
        session.add(category)
        session.commit()
        session.refresh(category)
        return category.used_budget > category.budget

    def get_budget_info(self) -> list[Category]:
        with self.get_session() as session:
            return session.exec(
                select(Category).options(selectinload(Category.transactions))
            ).all()
