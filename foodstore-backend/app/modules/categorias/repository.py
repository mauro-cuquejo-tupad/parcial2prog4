from typing import Sequence
from sqlmodel import Session, col, func, select
from .model import Categoria


def get_by_id(session: Session, id: int) -> Categoria | None:
    return session.get(Categoria, id)


def get_active_by_name(session: Session, nombre: str) -> Categoria | None:
    statement = select(Categoria).where(
        func.lower(Categoria.nombre) == nombre.lower(),
        Categoria.activo == True,
    )
    return session.exec(statement).first()


def list_categorias(
    session: Session,
    activo: bool | None = None,
    search: str | None = None,
) -> Sequence[Categoria]:
    statement = select(Categoria)

    if activo is False:
        statement = statement.where(Categoria.activo == False)
    elif activo is True:
        statement = statement.where(Categoria.activo == True)

    if search:
        statement = statement.where(col(Categoria.nombre).ilike(f"%{search}%"))

    return session.exec(statement.order_by(Categoria.id)).all()


def save(session: Session, categoria: Categoria) -> Categoria:
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
