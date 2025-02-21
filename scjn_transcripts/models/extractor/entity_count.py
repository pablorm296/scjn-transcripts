from pydantic import BaseModel

from scjn_transcripts.models.extractor.index import IndexEnum

class EntityCount(BaseModel):
    entidad: IndexEnum
    resultados: int