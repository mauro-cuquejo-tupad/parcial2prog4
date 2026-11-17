from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey, Relationship, DateTime
from datetime import datetime
from decimal import Decimal
from typing_extensions import Optional, List
from app.modules.unidades_medida.model import UnidadMedida

if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria

class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"
    es_principal: bool = Field(default=False)
    producto_id: int = Field(sa_column=Column(Integer, ForeignKey("producto.id", ondelete="CASCADE"), primary_key=True, nullable=False))
    categoria_id: int = Field(sa_column=Column(Integer, ForeignKey("categoria.id", ondelete="CASCADE"), primary_key=True, nullable=False))

class Producto(SQLModel, table=True):
    __tablename__ = "producto"
    id: Optional[int] = Field(default = None, primary_key = True)
    unidad_venta_id: int = Field(foreign_key="unidad_medida.id")
    nombre: str
    descripcion: Optional[str] = Field(default=None)
    precio_base: Decimal = Field(max_digits=10, decimal_places=2)
    stock_cantidad: Decimal = Field(default=0, max_digits=12, decimal_places=3)
    disponible: bool = Field(default=True, nullable=False)
    activo: bool = Field(default=True, nullable=False)
    anulado_at: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))

    categorias: List["Categoria"] = Relationship(back_populates="productos", link_model=ProductoCategoria)
    unidad_venta: Optional[UnidadMedida] = Relationship(back_populates="productos")

    @property
    def hay_stock(self) -> bool:
        return self.stock_cantidad > 0