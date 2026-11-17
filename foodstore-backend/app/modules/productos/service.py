from datetime import datetime, timezone
from decimal import Decimal
from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.categorias.model import Categoria
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.unidades_medida.enums import TipoUnidad
from app.modules.productos import repository as repo
from .model import Producto, ProductoCategoria
from .schema import (
    CategoriaProductoResponse,
    ProductoCategoriaCreate,
    ProductoCategoriaResponse,
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
)


# ==========================================
# Helpers
# ==========================================

def obtener_producto(session: Session, id: int) -> Producto:
    producto = repo.get_by_id(session, id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


def obtener_unidad(session: Session, id: int) -> UnidadMedida:
    unidad = repo.get_unidad_by_id(session, id)
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de venta no encontrada",
        )
    return unidad


def validar_stock(unidad: UnidadMedida, stock: Decimal) -> None:
    if unidad.tipo == TipoUnidad.CONTABLE and stock != stock.to_integral_value():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"La unidad {unidad.nombre} es contable: el stock debe ser un número entero",
        )

def validar_nombre(session: Session, nombre: str, excluir_id: int | None = None) -> None:
    existente = repo.get_active_by_name(session, nombre)
    if existente and existente.id != excluir_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto activo con nombre '{nombre}'",
        )

def validar_activo(activo: bool, mensaje: str) -> None:
    if not activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensaje,
        )


# ==========================================
# Casos de uso
# ==========================================

def crear_producto(session: Session, data: ProductoCreate) -> ProductoResponse:
    validar_nombre(session, data.nombre)
    unidad = obtener_unidad(session, data.unidad_venta_id)
    validar_stock(unidad, data.stock_cantidad)

    nuevo = Producto(**data.model_dump())
    guardado = repo.save(session, nuevo)
    return ProductoResponse.model_validate(guardado)


def detalle_producto(session: Session, id: int) -> ProductoResponse:
    producto = obtener_producto(session, id)
    return ProductoResponse.model_validate(producto)


def actualizar_producto(session: Session, id: int, data: ProductoUpdate) -> ProductoResponse:
    producto = obtener_producto(session, id)

    validar_activo(producto.activo, "No se puede actualizar el producto. Ya se encuentra anulado")
    validar_nombre(session, data.nombre, excluir_id=id)

    unidad = obtener_unidad(session, data.unidad_venta_id)
    validar_stock(unidad, data.stock_cantidad)

    actualizado = data.model_dump()
    
    for key, value in actualizado.items():
        setattr(producto, key, value)

    guardado = repo.save(session, producto)
    return ProductoResponse.model_validate(guardado)


def anular_producto(session: Session, id: int) -> None:
    producto = obtener_producto(session, id)

    validar_activo(producto.activo, "No se puede volver a anular el producto. Ya se encuentra anulado")

    producto.activo = False
    producto.anulado_at = datetime.now(timezone.utc)
    repo.save(session, producto)


def listar_productos(
    session: Session,
    skip: int,
    limit: int,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
) -> list[ProductoResponse]:
    productos = repo.list_productos(
        session=session,
        skip=skip,
        limit=limit,
        activo=activo,
        disponible=disponible,
        categoria_id=categoria_id,
        search=search,
    )
    return [ProductoResponse.model_validate(producto) for producto in productos]


def clasificar_producto(session: Session, id: int, datos: ProductoCategoriaCreate) -> ProductoCategoriaResponse:
    producto = obtener_producto(session, id)
    
    validar_activo(producto.activo, "No se puede clasificar el producto. Ya se encuentra anulado")

    categoria = repo.get_categoria_by_id(session, datos.categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="La categoría especificada no existe",
        )
    validar_activo(categoria.activo, "La categoría especificada se encuentra anulada")

    existente = repo.get_producto_categoria(session, id, datos.categoria_id)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya está clasificado en esa categoría",
        )

    if datos.es_principal:
        repo.unset_es_principal_by_producto(session, id)

    nuevo = ProductoCategoria(
        producto_id=id,
        categoria_id=datos.categoria_id,
        es_principal=datos.es_principal,
    )
    guardado = repo.save_producto_categoria(session, nuevo)
    return ProductoCategoriaResponse.model_validate(guardado)


def listar_categorias_por_producto(session: Session, id: int) -> list[CategoriaProductoResponse]:
    producto = obtener_producto(session, id)
    categorias = repo.listar_categorias_por_producto(session, producto.id)
    if not categorias:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return [
        CategoriaProductoResponse(
            id=categoria.id,
            nombre=categoria.nombre,
            es_principal=es_principal,
        )
        for categoria, es_principal in categorias
    ]
