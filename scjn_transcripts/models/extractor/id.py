from pydantic import BaseModel

from scjn_transcripts.models.extractor.index import IndexEnum

class Id(BaseModel):
    id: str
    type: IndexEnum