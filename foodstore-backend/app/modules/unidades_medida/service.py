from fastapi import HTTPException, status
from sqlmodel import Session
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.unidades_medida import repository as repo
from app.modules.unidades_medida.schema import UnidadMedidaResponse

def listar_unidades(session: Session) -> list[UnidadMedida]:
    unidades = repo.get_all_unidades(session)
    if not unidades:
        raise HTTPException(status_code= status.HTTP_204_NO_CONTENT)
    return [UnidadMedidaResponse.model_validate(unidad) for unidad in unidades]