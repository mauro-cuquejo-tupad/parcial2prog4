from typing import Sequence
from sqlmodel import Session, select, col, func
from sqlalchemy.orm import selectinload
from .model import Producto, ProductoCategoria
from app.modules.categorias.model import Categoria
from app.modules.unidades_medida.model import UnidadMedida


# ==========================================
# Consultas de Producto
# ==========================================

def get_by_id(session: Session, id: int) -> Producto | None:
    return session.get(Producto, id)


def get_active_by_name(session: Session, nombre: str) -> Producto | None:
    statement = select(Producto).where(
        func.lower(Producto.nombre) == nombre.lower(),
        Producto.activo == True,
    )
    return session.exec(statement).first()


def list_productos(
    session: Session,
    skip: int,
    limit: int,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
) -> Sequence[Producto]:
    statement = select(Producto).options(
        selectinload(Producto.unidad_venta),
        selectinload(Producto.categorias),
    )
    if activo is False:
        statement = statement.where(Producto.activo == False)
    else:
        statement = statement.where(Producto.activo == True)

    if disponible is not None:
        statement = statement.where(Producto.disponible == disponible)

    if search:
        statement = statement.where(col(Producto.nombre).ilike(f"%{search}%"))

    if categoria_id is not None:
        statement = statement.join(
            ProductoCategoria, ProductoCategoria.producto_id == Producto.id
        ).where(ProductoCategoria.categoria_id == categoria_id)

    statement = statement.order_by(Producto.id).offset(skip).limit(limit)
    return session.exec(statement).all()


def save(session: Session, producto: Producto) -> Producto:
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# ==========================================
# Consultas de Entidades Relacionadas
# ==========================================

def get_unidad_by_id(session: Session, id: int) -> UnidadMedida | None:
    return session.get(UnidadMedida, id)


def get_categoria_by_id(session: Session, id: int) -> Categoria | None:
    return session.get(Categoria, id)


# ==========================================
# Consultas de ProductoCategoria (Clasificación)
# ==========================================

def get_producto_categoria(session: Session, producto_id: int, categoria_id: int) -> ProductoCategoria | None:
    return session.get(ProductoCategoria, (producto_id, categoria_id))


def unset_es_principal_by_producto(session: Session, producto_id: int) -> None:
    statement = select(ProductoCategoria).where(
        ProductoCategoria.producto_id == producto_id,
        ProductoCategoria.es_principal == True,
    )
    anteriores = session.exec(statement).all()
    for vinculo in anteriores:
        vinculo.es_principal = False


def save_producto_categoria(session: Session, producto_categoria: ProductoCategoria) -> ProductoCategoria:
    session.add(producto_categoria)
    session.commit()
    session.refresh(producto_categoria)
    return producto_categoria


def listar_categorias_por_producto(session: Session, producto_id: int):
    return session.exec(
        select(Categoria, ProductoCategoria.es_principal)
        .join(ProductoCategoria, ProductoCategoria.categoria_id == Categoria.id)
        .where(ProductoCategoria.producto_id == producto_id)
        .order_by(Categoria.id)
    ).all()
