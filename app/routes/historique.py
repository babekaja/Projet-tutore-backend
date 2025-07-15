from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import database
from .. import crud, schemas


router = APIRouter(
    prefix="/historiques",
    tags=["Historiques d'accès"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.HistoriqueResponse)
def create_historique(historique: schemas.HistoriqueCreate, db: Session = Depends(get_db)):
    return crud.create_historique(db, historique)

@router.get("/", response_model=list[schemas.HistoriqueResponse])
def list_historiques(db: Session = Depends(get_db)):
    return crud.get_historiques(db)

@router.get("/etudiant/{etudiant_id}", response_model=list[schemas.HistoriqueResponse])
def get_historiques_etudiant(etudiant_id: str, db: Session = Depends(get_db)):
    return crud.get_historiques_by_etudiant(db, etudiant_id)

@router.get("/salle/{salle_id}", response_model=list[schemas.HistoriqueResponse])
def get_historiques_salle(salle_id: str, db: Session = Depends(get_db)):
    return crud.get_historiques_by_salle(db, salle_id)
