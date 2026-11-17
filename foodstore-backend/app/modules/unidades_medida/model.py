from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Session, select
from typing import Optional, List
from app.modules.unidades_medida.enums import TipoUnidad


class UnidadMedida(SQLModel, table=True):
    __tablename__ = "unidad_medida"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False, unique=True)
    simbolo: str = Field(nullable=False, unique=True)
    tipo: TipoUnidad = Field(nullable=False)

    productos: List["Producto"] = Relationship(back_populates="unidad_venta")


