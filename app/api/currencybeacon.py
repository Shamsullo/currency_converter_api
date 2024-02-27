import httpx

from app.config import settings


async def make_currencybeacon_request(
        url, params=None, body=None, headers=None
):
    if not params:
        params = {
            "api_key": settings.cb_api_key
        }
    else:
        params["api_key"] = settings.cb_api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["response"]
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc}")
        except httpx.RequestError as exc:
            print(f"Request error occurred: {exc}")


async def fetch_currency_data():
    url = "https://api.currencybeacon.com/v1/latest"
    params = {"base": "USD"}
    return await make_currencybeacon_request(url, params)


async def get_currency_info():
    url = "https://api.currencybeacon.com/v1/currencies"
    return await make_currencybeacon_request(url)


async def get_structured_currency_data():
    data = await fetch_currency_data()
    rates = data["rates"]
    curr_info = await get_currency_info()

    result = []
    for currency_info in curr_info:
        code = currency_info["short_code"]
        rate = rates.get(code)
        if rate is not None:
            result.append({
                "ccy": code,
                "rate": rate,
                "name": currency_info["name"],
                "code": currency_info["code"]
            })
    return result
