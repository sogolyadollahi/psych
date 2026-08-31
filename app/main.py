from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.meals import router as meal_router
from app.api.v1.workout import router as workout_router
from app.api.v1.supplement import router as supplement_router



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

app.include_router(
    workout_router,
    prefix="/api/v1",
)

app.include_router(
    meal_router,
    prefix="/api/v1",
)

app.include_router(
    supplement_router,
    prefix="/api/v1",
)