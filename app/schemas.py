import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    date: datetime.date


class ExpenseRead(ExpenseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)