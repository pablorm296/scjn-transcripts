from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Asunto(BaseModel):
    asunto_abordado: Annotated[Optional[str], Field(alias = "asuntoAbordado")] = None
    num_expediente: Annotated[Optional[str], Field(alias = "numExpediente")] = None
    temas_fondo_abordados: Annotated[Optional[list[str]], Field(alias = "temasFondoAbordados")] = None
    temas_procesales_abordados: Annotated[Optional[list[str]], Field(alias = "temasProcesalesAbordados")] = None