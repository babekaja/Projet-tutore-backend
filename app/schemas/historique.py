from pydantic import BaseModel
from datetime import datetime

class HistoriqueBase(BaseModel):
    etudiant_id: int | None = None
    salle_id: int | None = None
    type_acces: str
    matricule_utilise: str | None = None
    date_entree: datetime
    date_sortie: datetime | None = None

class HistoriqueCreate(HistoriqueBase):
    pass

class HistoriqueResponse(HistoriqueBase):
    id: int

    class Config:
        orm_mode = True
