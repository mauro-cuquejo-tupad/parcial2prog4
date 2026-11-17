from sqlmodel import Session, select
from app.core.database import engine
from app.modules.unidades_medida.model import UnidadMedida
from app.modules.unidades_medida.enums import TipoUnidad

def seed_unidades():
    with Session(engine) as session:
        # Nos fijamos si la tabla está vacía antes de sembrar
        if not session.exec(select(UnidadMedida)).first():
            unidades = [
                UnidadMedida(nombre="kilogramo", simbolo="kg", tipo=TipoUnidad.PESO),
                UnidadMedida(nombre="gramo", simbolo="g", tipo=TipoUnidad.PESO),
                UnidadMedida(nombre="litro", simbolo="L", tipo=TipoUnidad.VOLUMEN),
                UnidadMedida(nombre="mililitro", simbolo="mL", tipo=TipoUnidad.VOLUMEN),
                UnidadMedida(nombre="pieza", simbolo="u", tipo=TipoUnidad.CONTABLE),
                UnidadMedida(nombre="docena", simbolo="doc", tipo=TipoUnidad.CONTABLE),
            ]
            session.add_all(unidades)
            session.commit()
            print("Unidades cargadas correctamente en la base de datos.")

    