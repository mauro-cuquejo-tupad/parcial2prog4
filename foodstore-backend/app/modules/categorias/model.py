from app.modules.productos.model import ProductoCategoria
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from typing_extensions import Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from app.modules.productos.model import Producto

class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: Optional[str] = Field(default=None)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))

    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )