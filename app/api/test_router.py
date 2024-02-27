import pytest
import httpx

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_update_currency_exchange_rate_success():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/v1/rates/update")
        assert response.status_code == 200
        assert "inserted_rows" in response.json()
        assert "updated_rows" in response.json()

# Add more tests here for failure scenarios,
# e.g., when the CurrencyBeacon service is unavailable


@pytest.mark.asyncio
async def test_get_last_rate_update_datetime_success():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v1/rates/last-update")
        assert response.status_code == 200
        data = response.json()
        assert "source" in data
        assert "updated_at" in data

# Consider adding tests to validate the response data thoroughly,
# including date format


@pytest.mark.asyncio
async def test_convert_currency_success():
    async with httpx.AsyncClient() as client:
        payload = {"source": "USD", "target": "EUR", "amount": 100}
        response = await client.post(
            f"{BASE_URL}/v1/rates/convert", json=payload
        )
        assert response.status_code == 200
        data = response.json()
        assert "source" in data and data["source"] == "USD"
        assert "target" in data and data["target"] == "EUR"
        assert "amount" in data and data["amount"] == 100
        assert "rate" in data
        assert "value" in data


@pytest.mark.asyncio
async def test_convert_currency_validation_error():
    async with httpx.AsyncClient() as client:
        payload = {"source": "USD", "amount": 100}  # Missing 'target'
        response = await client.post(
            f"{BASE_URL}/v1/rates/convert", json=payload
        )
        assert response.status_code == 422

# Add more tests for other scenarios,
# like unsupported currency codes or invalid amounts
