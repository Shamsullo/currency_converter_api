from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.database import Base


class CurrencyRate(Base):
    """Table for storing latest currency exchange rates"""
    __tablename__ = "currency_rate"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(
        String, unique=True, index=True,
        comment="International accepted currency number (840, 978,...)"
    )
    ccy = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        comment="International accepted currency code (USD, EUR, etc.)"
    )
    rate = Column(Float, default=True, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class UpdateRateHistory(Base):
    """Table for storing the update history of a currency rates"""
    __tablename__ = "update_history"

    id = Column(Integer, primary_key=True)
    source = Column(
        String,
        index=True,
        comment="The source where the rates were fetched"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        comment="Time and date when the rate was updated"
    )
