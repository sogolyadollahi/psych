from fastapi import FastAPI

from app.api.v1.auth import router as auth_router


app = FastAPI(
    title= "Psych API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return{
        "status": "OK",
    }


app.include_router(
    auth_router,
    prefix="/api/v1",
)