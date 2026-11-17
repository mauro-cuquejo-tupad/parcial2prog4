from app.core.database import get_session
from app.modules.unidades_medida import service
from fastapi import Depends
from sqlmodel import Session
from app.modules.unidades_medida.schema import UnidadMedidaResponse
from typing_extensions import List
from fastapi import APIRouter, status


router = APIRouter(prefix="/api/v1/unidades-medida", tags=["unidades-medida"])

@router.get("", response_model=List[UnidadMedidaResponse], status_code=status.HTTP_200_OK)
def listar_unidades(session: Session = Depends(get_session)):
    return service.listar_unidades(session)