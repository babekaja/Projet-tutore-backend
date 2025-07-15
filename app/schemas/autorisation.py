from pydantic import BaseModel
from datetime import datetime

class AutorisationBase(BaseModel):
    etudiant_id: int
    salle_id: int
    niveau_acces: str = "standard"
    actif: bool = True
    date_debut: datetime | None = None
    date_fin: datetime | None = None

class AutorisationCreate(AutorisationBase):
    pass

class AutorisationResponse(AutorisationBase):
    id: int

    class Config:
        orm_mode = True
