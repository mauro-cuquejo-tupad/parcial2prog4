from sqlmodel import create_engine, SQLModel, Session, text
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL visible en consola (obligatorio en dev)
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def reset_database():
    """
    Trunca las tablas transaccionales reiniciando sus secuencias de ID,
    pero manteniendo intacta la estructura para volver a probar desde ID = 1.
    """
    with Session(engine) as session:
        session.exec(
            text("TRUNCATE TABLE producto_categoria, producto, categoria RESTART IDENTITY CASCADE;")
        )
        session.commit()
        print("Base de datos reiniciada correctamente.")


    
def get_session():
    # Cada request obtiene su propia sesión
    # No se comparte estado entre requests
    with Session(engine) as session:
        # El endpoint usa esta sesión para leer/escribir en la base
        yield session
        # Al terminar el request:
        # - se cierra la sesión
        # - se devuelve la conexión al pool