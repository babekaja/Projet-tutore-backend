from pydantic import BaseModel
from datetime import datetime

class SalleBase(BaseModel):
    nom_salle: str
    localisation: str | None = None
    description: str | None = None

class SalleCreate(SalleBase):
    pass

class SalleResponse(SalleBase):
    id: int


    class Config:
        orm_mode = True
