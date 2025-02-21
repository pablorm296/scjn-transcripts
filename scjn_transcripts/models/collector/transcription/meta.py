from pydantic import BaseModel, Field
from typing import Annotated

from scjn_transcripts.models.collector.transcription.organo_jurisdiccional import OrganoJurisdiccionalEnum

class TranscriptionMetadata(BaseModel):
    organo_jurisdiccional: Annotated[OrganoJurisdiccionalEnum, Field(alias = "organoJurisdiccional")]
    instancia: str = "Suprema Corte de Justicia de la Nación"
    pos: int
    id_vt: Annotated[str, Field(alias = "idVT")]
    extractos: dict
    fecha_sesion: Annotated[str, Field(alias = "fechaSesion")]
    id: str
    type: str = "vtaquigraficas"
    anio: int