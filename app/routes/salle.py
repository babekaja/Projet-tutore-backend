from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import database
from .. import crud, schemas

router = APIRouter(
    prefix="/salles",
    tags=["Salles"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SalleResponse)
def create_salle(salle: schemas.SalleCreate, db: Session = Depends(get_db)):
    return crud.create_salle(db, salle)

@router.get("/", response_model=list[schemas.SalleResponse])
def list_salles(db: Session = Depends(get_db)):
    return crud.get_salles(db)

@router.get("/{salle_id}", response_model=schemas.SalleResponse)
def get_salle(salle_id: str, db: Session = Depends(get_db)):
    salle = crud.get_salle_by_id(db, salle_id)
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return salle

@router.delete("/{salle_id}")
def delete_salle(salle_id: str, db: Session = Depends(get_db)):
    salle = crud.delete_salle(db, salle_id)
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return {"message": "Salle supprimée avec succès"}
