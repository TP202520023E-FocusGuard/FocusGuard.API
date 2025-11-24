from pydantic import BaseModel, Field
from datetime import datetime


class ModelClassificationInput(BaseModel):
    texto: str


class ModelClassificationOutput(BaseModel):
    probabilidad_no_ocio: float
    probabilidad_ocio: float
    etiqueta_predicha: str

