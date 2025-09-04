from datetime import datetime

from sqlmodel import Field, SQLModel


class transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    remark: str
    transaction_time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recurrence: bool = False
    category: str = Field(foreign_key=True)


class category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_name: str
