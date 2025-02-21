from pydantic import BaseModel

from scjn_transcripts.models.collector.index import IndexEnum

class Id(BaseModel):
    id: str
    type: IndexEnum