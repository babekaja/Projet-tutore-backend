from pydantic import BaseModel, EmailStr
from datetime import datetime

class EtudiantBase(BaseModel):
    matricule: str
    nom: str
    prenom: str | None = None
    email: str
    uid_firebase: str

class EtudiantCreate(EtudiantBase):
    pass

class EtudiantResponse(EtudiantBase):
    id: int
    date_creation: datetime

    class Config:
        orm_mode = True
