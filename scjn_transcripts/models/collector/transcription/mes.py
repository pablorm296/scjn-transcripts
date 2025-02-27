from pydantic import BaseModel

class Mes(BaseModel):
    numero: int
    nombre: str