from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    remark: str
    transaction_time: datetime = datetime
    recurrence: bool = False
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category = Relationship(back_populates="transactions")


class category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_name: str
    transactions: list[transaction] = Relationship(back_populates="category")
