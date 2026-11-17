from enum import Enum

class TipoUnidad(str, Enum):
    PESO = "peso"
    VOLUMEN = "volumen"
    CONTABLE = "contable"