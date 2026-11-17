from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, status
from sqlmodel import Session
from app.core.database import get_session
from . import schema, service

router = APIRouter(prefix="/api/v1/categorias", tags=["Categorías"])


@router.post("", response_model=schema.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    categoria: schema.CategoriaCreate,
    session: Session = Depends(get_session),
):
    return service.crear_categoria(session, categoria)


@router.get("", response_model=List[schema.CategoriaResponse])
def listar_categorias(
    activo: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    return service.listar_categorias(session, activo, search)


@router.get("/{id}", response_model=schema.CategoriaResponse)
def detalle_categoria(
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
):
    return service.detalle_categoria(session, id)


@router.put("/{id}", response_model=schema.CategoriaResponse)
def actualizar_categoria(
    categoria: schema.CategoriaUpdate,
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
):
    return service.actualizar_categoria(session, id, categoria)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_categoria(
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
):
    service.anular_categoria(session, id)
