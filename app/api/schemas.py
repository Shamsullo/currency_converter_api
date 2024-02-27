from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExchangeRateIn(BaseModel):
    source: str
    target: str
    amount: float


class ExchangeRateOut(BaseModel):
    source: str
    target: str
    amount: float
    rate: float
    value: float


class LastUpdate(BaseModel):
    source: str
    updated_at: datetime


class RateUpsertResponse(BaseModel):
    inserted_rows: Optional[int]
    updated_rows: Optional[int]


class NoFountResponse(BaseModel):
    message: str
