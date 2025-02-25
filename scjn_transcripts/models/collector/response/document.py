from typing import Annotated, Optional
from pydantic import BaseModel, Field

from scjn_transcripts.models.collector.transcription.organo_jurisdiccional import OrganoJurisdiccionalEnum
from scjn_transcripts.models.collector.transcription.asunto import Asunto
from scjn_transcripts.models.collector.transcription.mes import Mes

class DocumentDetailsResponse(BaseModel):
    organo_jurisdiccional: Annotated[OrganoJurisdiccionalEnum, Field(alias = "organoJurisdiccional")]
    contenido: str
    url_video: Annotated[Optional[str], Field(alias = "urlVideo")] = None
    archivo: str
    id_vt: Annotated[Optional[str], Field(alias = "idVT")] = None
    fecha_sesion: Annotated[str, Field(alias = "fechaSesion")]
    video: Annotated[Optional[str], Field(alias = "video")] = None
    url_vt: Annotated[Optional[str], Field(alias = "urlVT")] = None
    id_original: Annotated[Optional[str], Field(alias = "idOriginal")] = None
    huella_digital: Annotated[Optional[str], Field(alias = "huellaDigital")] = None
    instancia: str = "Suprema Corte de Justicia de la Nación"
    asuntos: Optional[list[Asunto]] = None
    mes: Mes
    id: str
    dia: int
    anio: int