from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, status
from sqlmodel import Session
from app.core.database import get_session
from . import schema, service

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])

@router.post("", response_model=schema.ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto: schema.ProductoCreate,
    session: Session = Depends(get_session)
):
    return service.crear_producto(session, producto)


@router.get("/{id}", response_model=schema.ProductoResponse)
def detalle_producto(
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    return service.detalle_producto(session, id)


@router.get("", response_model=List[schema.ProductoResponse])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: Optional[bool] = Query(None),
    disponible: Optional[bool] = Query(None),
    categoria_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    return service.listar_productos(session, skip, limit, activo, disponible, categoria_id, search)


@router.put("/{id}", response_model=schema.ProductoResponse)
def actualizar_producto(
    producto: schema.ProductoUpdate,
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    return service.actualizar_producto(session, id, producto)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def anular_producto(
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    service.anular_producto(session, id)


@router.post("/{id}/categorias", response_model=schema.ProductoCategoriaResponse, status_code=status.HTTP_201_CREATED)
def clasificar_producto(
    datos: schema.ProductoCategoriaCreate,
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    return service.clasificar_producto(session, id, datos)


@router.get("/{id}/categorias", response_model=List[schema.CategoriaProductoResponse])
def listar_categorias_por_producto(
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session)
):
    return service.listar_categorias_por_producto(session, id)