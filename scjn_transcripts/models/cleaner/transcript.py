from pydantic import BaseModel
from typing import Optional
import datetime

from scjn_transcripts.models.collector.transcription.organo_jurisdiccional import OrganoJurisdiccionalEnum

class Transcript(BaseModel):
    id: str
    organo_jurisdiccional: OrganoJurisdiccionalEnum
    contenido: str
    url_video: Optional[str] = None
    url_documento: Optional[str] = None
    asuntos: Optional[list[str]] = None
    fecha_sesión: datetime.datetime