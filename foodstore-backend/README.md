# Foodstore Backend

API REST construida con FastAPI y SQLModel para la gestión de productos, categorías y unidades de medida.

Alumno: Mauro Cuquejo  
Materia: Programación 4  
Evaluación: Recuperatorio Parcial 2  

## Requisitos

- Python 3.10 o superior
- PostgreSQL o Docker

## Instalación y ejecución

1. Crear y activar el entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Levantar la base de datos con Docker:
```bash
docker compose up -d
```

4. Configurar las variables en el archivo `.env`:
```env
DATABASE_URL=postgresql+psycopg://postgres:mipasswordseguro@localhost:5432/foodstore
RESET_DB=false
```

Si se establece `RESET_DB=true`, al iniciar el servidor se vacían las tablas transaccionales de productos y categorías reiniciando sus contadores de ID en 1 para facilitar la ejecución de pruebas.

5. Iniciar la aplicación:
```bash
uvicorn app.main:app --reload
```

La documentación interactiva de Swagger queda disponible en:
http://localhost:8000/docs
