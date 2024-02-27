from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title="Currency Converter API",
    description="This API was built with FastAPI and provides functionality "
                "for converting between two currencies",
    version="1.0.0",
    docs_url='/api/docs',
    redoc_url='/api/redocs',
)

get_openapi(
    title="Currency Converter API",
    description="This API was built with FastAPI and provides functionality "
                "for converting between two currencies",
    version="1.0.0",
    routes=app.routes,
)

app.include_router(api_router, prefix="/v1")


@app.get("", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse(
        {"message": "Welcome to currency converter API service"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
