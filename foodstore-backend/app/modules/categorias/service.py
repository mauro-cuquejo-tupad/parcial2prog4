from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.categorias import repository as repo
from .model import Categoria
from .schema import CategoriaCreate, CategoriaResponse, CategoriaUpdate


# ==========================================
# Helpers
# ==========================================

def validar_nombre(session: Session, nombre: str, excluir_id: int | None = None) -> None:
    existente = repo.get_active_by_name(session, nombre)
    if existente and existente.id != excluir_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría activa con nombre '{nombre}'",
        )


def obtener_categoria(session: Session, id: int) -> Categoria:
    categoria = repo.get_by_id(session, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


def validar_activo(activo: bool, mensaje: str) -> None:
    if not activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensaje,
        )


# ==========================================
# Casos de uso
# ==========================================

def crear_categoria(session: Session, data: CategoriaCreate) -> CategoriaResponse:
    validar_nombre(session, data.nombre)
    nueva = Categoria(**data.model_dump())
    guardada = repo.save(session, nueva)
    return CategoriaResponse.model_validate(guardada)


def detalle_categoria(session: Session, id: int) -> CategoriaResponse:
    categoria = obtener_categoria(session, id)
    return CategoriaResponse.model_validate(categoria)


def listar_categorias(
    session: Session,
    activo: bool | None = None,
    search: str | None = None,
) -> list[CategoriaResponse]:
    categorias = repo.list_categorias(session, activo=activo, search=search)
    return [CategoriaResponse.model_validate(categoria) for categoria in categorias]


def actualizar_categoria(
    session: Session, id: int, data: CategoriaUpdate
) -> CategoriaResponse:
    categoria = obtener_categoria(session, id)
    validar_activo(categoria.activo, "No se puede actualizar una categoría anulada")
    validar_nombre(session, data.nombre, excluir_id=id)

    actualizado = data.model_dump()
    for key, value in actualizado.items():
        setattr(categoria, key, value)

    guardada = repo.save(session, categoria)
    return CategoriaResponse.model_validate(guardada)


def anular_categoria(session: Session, id: int) -> None:
    categoria = obtener_categoria(session, id)
    validar_activo(categoria.activo, "La categoría ya está anulada")

    categoria.activo = False
    categoria.anulado_at = datetime.now(timezone.utc)
    repo.save(session, categoria)
