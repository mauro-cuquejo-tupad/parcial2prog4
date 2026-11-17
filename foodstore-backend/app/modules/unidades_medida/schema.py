from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from app.modules.unidades_medida.enums import TipoUnidad


#### UNIDAD DE MEDIDA ####
class UnidadMedidaBase(BaseModel):
    nombre: Annotated[str, StringConstraints(strip_whitespace=True)]
    simbolo: Annotated[str, StringConstraints(strip_whitespace=True)]
    tipo: TipoUnidad


# Modelos request
class UnidadMedidaCreate(UnidadMedidaBase):
    pass

class UnidadMedidaUpdate(UnidadMedidaBase):
    pass


# Modelo response
class UnidadMedidaResponse(UnidadMedidaBase):
    model_config = ConfigDict(from_attributes=True)    
    id: int