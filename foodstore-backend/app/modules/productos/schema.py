from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

#### PRODUCTO ####
class ProductoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nombre: Annotated[str, StringConstraints(strip_whitespace=True), Field(min_length=3)]
    descripcion: Optional[str] = None
    precio_base: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
    stock_cantidad: Annotated[Decimal, Field(ge=0, max_digits=12, decimal_places=3)] = Decimal("0")
    unidad_venta_id: int
    disponible: bool = True

# modelos request
class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

# modelos response
class UnidadBasicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    simbolo: str

class CategoriaBasicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

class CategoriaProductoResponse(BaseModel):
    id: int
    nombre: str
    es_principal: bool
    

class ProductoResponse(ProductoBase):
    id: int
    activo: bool
    anulado_at: Optional[datetime] = None
    unidad_venta: UnidadBasicResponse
    categorias: List[CategoriaBasicResponse] = []
    hay_stock: bool


#### PRODUCTO CATEGORIA ####
# modelos request
class ProductoCategoriaCreate(BaseModel):
    categoria_id: int
    es_principal: bool = False


# modelos response
class ProductoCategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    producto_id: int
    categoria_id: int
    es_principal: bool