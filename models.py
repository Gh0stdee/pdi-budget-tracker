from datetime import datetime

from sqlmodel import Field, SQLModel


class transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    remark: str
    transaction_time: datetime
    recurrence: bool = False
