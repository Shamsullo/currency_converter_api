from typing import List

from sqlalchemy import bindparam, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from . import models, schemas


async def bulk_upsert_currency_rates(db: AsyncSession, data_list: List[dict]):
    existing_ccys = [data['ccy'] for data in data_list]
    result = await db.execute(
        select(models.CurrencyRate)
        .filter(models.CurrencyRate.ccy.in_(existing_ccys))
    )
    existing_records = result.scalars().all()
    existing_records_map = {record.ccy: record for record in existing_records}
    
    to_be_inserted, to_be_updated = [], []
    for data in data_list:
        if data['ccy'] in existing_records_map:
            data['id'] = existing_records_map[data['ccy']].id
            data['_ccy'] = data['ccy']
            to_be_updated.append(data)
        else:
            to_be_inserted.append(data)

    if to_be_updated:
        update_stmt = (
            update(models.CurrencyRate)
            .where(models.CurrencyRate.ccy == bindparam('_ccy'))
            .values({'rate': bindparam('rate'), 'updated_at': func.now()})
            .execution_options(synchronize_session=None)
        )
        await db.execute(update_stmt, to_be_updated)

    if to_be_inserted:
        await db.execute(insert(models.CurrencyRate), to_be_inserted)
    await db.commit()
    await record_update_history(db, "CurrencyBeacon")
    return {
        "inserted_rows": len(to_be_inserted),
        "updated_rows": len(to_be_updated)
    }


async def record_update_history(db: AsyncSession, source: str):
    await db.execute(
        insert(models.UpdateRateHistory).values(source=source)
    )
    await db.commit()
    return {"inserted_rows":  1}


async def get_last_rate_update(db: AsyncSession):
    result = await db.execute(
        select(models.UpdateRateHistory)
        .order_by(models.UpdateRateHistory.updated_at.desc())
        .limit(1)
    )
    return result.scalar()


async def convert_currency(db: AsyncSession, request: schemas.ExchangeRateIn):
    response = schemas.ExchangeRateOut(
            source=request.source,
            target=request.target,
            amount=request.amount,
            rate=1,
            value=request.amount
        )
    if request.target == request.source:
        return response

    rates_query = await db.execute(
        select(models.CurrencyRate)
        .where(models.CurrencyRate.ccy.in_([request.source, request.target]))
    )
    rates = {rate.ccy: rate for rate in rates_query.scalars().all()}

    if request.source not in rates or request.target not in rates:
        return JSONResponse(
            {"message": "Source or target currency does not exist"},
            status_code=404
        )

    source_rate = rates[request.source].rate
    target_rate = rates[request.target].rate
    response.rate = (1/source_rate)*target_rate
    response.value = request.amount * (1 / source_rate) * target_rate
    return response
