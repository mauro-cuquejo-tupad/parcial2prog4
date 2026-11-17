from sqlmodel import Session,select
from app.modules.unidades_medida.model import UnidadMedida

def get_all_unidades(session: Session) -> list[UnidadMedida]:    
   return  session.exec(select(UnidadMedida)).all()