from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import business_logic, schemas, currencybeacon
from app.database import get_db

router = APIRouter(prefix="/rates")


@router.post("/update", response_model=schemas.RateUpsertResponse)
async def update_currency_exchange_rate(db: AsyncSession = Depends(get_db)):
    """Update exchange rates in the database to current rates from CurrencyBeacon"""
    data = await currencybeacon.get_structured_currency_data()
    return await business_logic.bulk_upsert_currency_rates(db, data)


@router.get("/last-update", response_model=schemas.LastUpdate)
async def get_the_last_rate_update_datetime(db: AsyncSession = Depends(get_db)):
    """Display the date and time of the last update of rates in the database"""
    return await business_logic.get_last_rate_update(db)


@router.post(
    "/convert",
    response_model=schemas.ExchangeRateOut,
    responses={404: {"model": schemas.NoFountResponse}}
)
async def covert_currency(
    ex_request: schemas.ExchangeRateIn, db: AsyncSession = Depends(get_db)
):
    """Conversion between currencies"""
    return await business_logic.convert_currency(db, ex_request)
