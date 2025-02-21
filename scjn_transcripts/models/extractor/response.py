from pydantic import BaseModel, Field
from typing import Annotated

from scjn_transcripts.models.extractor.transcription.meta import TranscriptionMetadata
from scjn_transcripts.models.extractor.entity_count import EntityCount
from scjn_transcripts.models.extractor.id import Id

class BúsquedaResponse(BaseModel):
    total: int
    entidades: list[EntityCount]
    resultados: list[TranscriptionMetadata]
    ids: list[Id]
    did_you_mean: Annotated[list, Field(alias = "didyoumean")]
    pagina: int
    size: int
    skip: Annotated[int, Field(alias = "from")]
    to: Annotated[int, Field(alias = "fromTo")]
    qTranslate: str
