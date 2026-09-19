from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes.auth import router as auth_router
from backend.routes.trips import router as trips_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trip AI API")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(trips_router)


@app.get("/")
def root():
    return {"message": "Trip AI API is running"}