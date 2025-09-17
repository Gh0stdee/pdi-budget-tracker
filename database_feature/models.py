from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float
    remark: str
    transaction_time: datetime = Field(default_factory=datetime.now)
    recurrence: bool = False
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: "Category" = Relationship(back_populates="transactions")


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_name: str
    budget: float
    used_budget: float = 0
    transactions: list[Transaction] = Relationship(back_populates="category")
