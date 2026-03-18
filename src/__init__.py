from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

version = "v1"

app = FastAPI(
    title = 'BOOkly',
    description = 'A REST API for BOOK review web service',
    version = version,
    lifespan = life_span
)

app.include_router(book_router, prefix = f"/api/{version}")