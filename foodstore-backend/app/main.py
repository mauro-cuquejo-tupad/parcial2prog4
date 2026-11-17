from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from app.core.database import create_db_and_tables, reset_database
import app.modules.productos.model  # Importante: registra las tablas en SQLModel.metadata
import app.modules.categorias.model
import app.modules.unidades_medida.model
from app.modules.productos.router import router as producto_router
from app.modules.categorias.router import router as categoria_router
from app.modules.unidades_medida.router import router as unidades_medida_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.seed import seed_unidades


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    # Si se configura RESET_DB=true en el .env, trunca las tablas y reinicia los IDs
    if os.getenv("RESET_DB", "false").lower() in ("true", "1", "yes"):
        reset_database()

    seed_unidades()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Recuperatorio Parcial 2 - FastAPI + SQLModel + React + Tailwind",
        description="Conceptos: Path, Query, Body, Pydantic, Errores.",
        version="1.0.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://localhost:5173'],
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(unidades_medida_router)

    

    return app

app = create_app()


