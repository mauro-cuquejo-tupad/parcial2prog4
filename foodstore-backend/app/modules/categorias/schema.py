from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field, StringConstraints

#### CATEGORIA ####
class CategoriaBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True), Field(min_length=3)]    
    descripcion: Optional[str] = None

# Modelos request
class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass

# Modelos response
class CategoriaResponse(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activo: bool
    anulado_at: Optional[datetime] = None
